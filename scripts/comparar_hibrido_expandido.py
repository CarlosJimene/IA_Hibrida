from transformers import T5Tokenizer, T5ForConditionalGeneration
import requests

# Modelo actualizado
MODEL_PATH = "models/t5_formateador_expandido"
API_URL = "http://127.0.0.1:8080/resolver-integral-light"

# Preguntas de prueba
benchmark = [
    {"pregunta": "Calcula la integral de x**2 entre 0 y 1", "esperado": 0.333333},
    {"pregunta": "Integral definida de ln(x) entre 1 y 2", "esperado": 0.386294},
    {"pregunta": "Evalúa ∫ sin(x) entre 0 y pi", "esperado": 2.0},
    {"pregunta": "¿Cuál es la integral de e**x entre 0 y 1?", "esperado": 1.718281},
    {"pregunta": "Integral de x**3 entre -1 y 1", "esperado": 0.0},
]

# Cargar modelo
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

def formatear(texto):
    inputs = tokenizer(texto, return_tensors="pt", padding=True)
    output = model.generate(**inputs, max_length=64, num_beams=2, early_stopping=True)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def consultar_api(formato):
    try:
        funcion, limites = formato.split(" from ")
        a, b = limites.strip().split(" to ")
        payload = {"funcion": funcion.strip(), "a": a.strip(), "b": b.strip()}
        response = requests.post(API_URL, json=payload, timeout=10)
        return float(response.json().get("resultado_numerico"))
    except:
        return None

# Evaluación
print("\n📊 RESULTADOS DEL SISTEMA HÍBRIDO (formateador expandido):\n")
aciertos = 0

for item in benchmark:
    pregunta = item["pregunta"]
    esperado = item["esperado"]
    print(f"🧠 {pregunta}")
    
    formato = formatear(pregunta)
    resultado = consultar_api(formato)

    if resultado is not None:
        diferencia = abs(resultado - esperado)
        if diferencia < 0.01:
            print(f"✅ Esperado: {esperado} | Obtenido: {resultado:.6f} | Δ: {diferencia:.2e}")
            aciertos += 1
        else:
            print(f"❌ Incorrecto | Esperado: {esperado} | Obtenido: {resultado:.6f} | Δ: {diferencia:.2e}")
    else:
        print(f"⚠️  Error consultando API o formato inválido")

    print("-" * 70)

print(f"\n🎯 Aciertos: {aciertos}/{len(benchmark)} ({100*aciertos/len(benchmark):.1f}%)")
