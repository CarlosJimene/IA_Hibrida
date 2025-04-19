"""
Script comparar_hibrido_final.py
----------------------------------
Evalúa la precisión del sistema híbrido (modelo formateador + API) sobre 10 casos clásicos de integración.
"""


from transformers import T5Tokenizer, T5ForConditionalGeneration
import requests
import torch

# Configuración
# Modelo entrenado para convertir lenguaje natural a formato estructurado: "f(x) from a to b"
MODEL_PATH = "models/t5_formateador"
API_URL = "http://127.0.0.1:8080/resolver-integral-light"
TOLERANCIA = 0.01

# Casos de prueba
test_cases = [
    ("Calcula la integral de x**2 entre 0 y 1", "0.333333"),
    ("Calcula la integral de x entre 0 y 2", "2.0"),
    ("Calcula la integral de cos(x) entre 0 y 3.1416", "0.0"),
    ("Calcula la integral de sin(x) entre 0 y 3.1416", "2.0"),
    ("Calcula la integral de exp(x) entre 0 y 1", "1.718281"),
    ("Calcula la integral de x**3 entre -1 y 1", "0.0"),
    ("Calcula la integral de 1/(1 + x**2) entre 0 y 1", "0.785398"),
    ("Calcula la integral de x**2 + 2*x + 1 entre 0 y 1", "2.333333"),
    ("Calcula la integral de ln(x) entre 1 y 2", "0.386294"),
    ("Calcula la integral de tan(x) entre 0 y 0.5", "0.255412"),
]

# Cargar modelo y tokenizador
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print("\n📊 RESULTADOS DEL SISTEMA HÍBRIDO:\n")

aciertos = 0

for pregunta, esperado in test_cases:
    inputs = tokenizer(pregunta, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=32
        )

    formato = tokenizer.decode(output[0], skip_special_tokens=True).strip()

    # Extraer función y límites de integracion e intentar interpretar el formato generado
    try:
        funcion, intervalo = formato.split(" from ")
        a_str, b_str = intervalo.split(" to ")
        payload = {
            "funcion": funcion.strip(),
            "a": float(a_str.strip()),
            "b": float(b_str.strip())
        }
    except Exception as e:
        print(f"❌ {pregunta}")
        print(f"   → Error al interpretar '{formato}': {e}\n")
        continue

    # Llamada a la API para calcular la integral
    try:
        res = requests.post(API_URL, json=payload, timeout=10)
        if res.status_code != 200:
            raise Exception(f"API error {res.status_code}")

        data = res.json()
        resultado = float(data.get("resultado_numerico", "nan"))
        esperado_f = float(esperado)
        acierto = abs(resultado - esperado_f) <= TOLERANCIA

        estado = "✅" if acierto else "❌"
        print(f"{estado} Pregunta: {pregunta}")
        print(f"   → Esperado: {esperado}")
        print(f"   → Formato IA: {formato}")
        print(f"   → Resultado API: {resultado:.6f}\n")
        aciertos += int(acierto)

    except Exception as e:
        print(f"❌ Error consultando API para: {pregunta}")
        print(f"   → {e}\n")

# Mostrar resumen
total = len(test_cases)
print(f"🎯 Aciertos: {aciertos} de {total} ({aciertos/total*100:.1f}%)")
