import requests
import time
import csv
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Configuración
MODEL_PATH = "models/t5_formateador"
API_URL = "http://127.0.0.1:8080/resolver-integral-light"
TOLERANCIA = 1e-3
CSV_OUTPUT = "resultados_benchmark.csv"

# Preguntas de prueba
PRUEBAS = [
    ("Calcula la integral de x**2 entre 0 y 1", 0.333333),
    ("Calcula la integral de x entre 0 y 2", 2.0),
    ("Integral de cos(x) entre 0 y 3.1416", 0.0),
    ("Integral de sin(x) desde 0 hasta pi", 2.0),
    ("Integral de e**x entre 0 y 1", 1.718281),
    ("¿Cuál es la integral de x**3 entre -1 y 1?", 0.0),
    ("Evalúa ∫ 1/(1 + x**2) entre 0 y 1", 0.785398),
    ("Calcula la integral de x**2 + 2*x + 1 entre 0 y 1", 2.333333),
    ("Integral definida de ln(x) entre 1 y 2", 0.386294),
    ("Integral de tan(x) entre 0 y 0.5", 0.255412),
    ("Integra x^4 de -1 a 1", 0.4),
    ("Calcula ∫ cos(x**2) desde -1 hasta 1", 1.32934),
    ("Integral de sqrt(x) entre 0 y 4", 5.33333),
    ("¿Cuál es la integral de exp(-x**2) de -1 a 1?", 1.49365),
    ("Calcula la integral de 1/x entre 1 y e", 1.0),
    ("Evalúa ∫ sec(x)**2 entre 0 y 0.5", 0.255341),
    ("Integral de sin(x**2) entre 0 y 1", 0.31027),
    ("Integral de 1/(x+1) entre 0 y 1", 0.693147),
    ("Integral definida de 3*x**3 - x**2 + 2*x + 1 entre -1 y 1", 2.0),
    ("Calcula la integral de x*cos(x) entre 0 y pi", -2.0),
]

# Cargar modelo
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def verificar_api():
    try:
        r = requests.post(API_URL, json={"funcion": "x", "a": 0, "b": 1}, timeout=5)
        if r.status_code == 200:
            print("✅ API en línea.\n")
            return True
        print(f"❌ La API respondió con código {r.status_code}")
        return False
    except Exception as e:
        print(f"❌ Error de conexión con la API: {e}")
        return False

def interpretar_pregunta(texto):
    inputs = tokenizer(texto, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_new_tokens=32)
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()

def limpiar_formato(formato):
    limpio = (
        formato.lower()
        .replace("?", "")
        .replace("desde", "from")
        .replace("de", "from")
        .replace("hasta", "to")
        .replace("a", "to")
        .replace("^", "**")
        .replace("π", "3.1416")
        .replace("e", "2.71828")
    )
    return limpio.strip()

def extraer_funcion_y_limites(formato):
    try:
        partes = formato.split("from")
        funcion = partes[0].strip()
        a_str, b_str = partes[1].strip().split("to")
        return funcion, float(a_str.strip()), float(b_str.strip())
    except:
        return None, None, None

def consultar_api(funcion, a, b):
    try:
        r = requests.post(API_URL, json={"funcion": funcion, "a": a, "b": b}, timeout=10)
        if r.status_code == 200:
            return r.json().get("resultado_numerico", None)
    except:
        return None
    return None

def evaluar():
    if not verificar_api():
        print("🛑 Cancela el benchmark hasta que la API esté en ejecución.")
        return

    aciertos = 0
    errores_formato = 0
    errores_api = 0
    tiempos = []
    resultados_csv = []

    print("📊 EVALUACIÓN EXTENDIDA DEL SISTEMA HÍBRIDO\n")

    for pregunta, esperado in PRUEBAS:
        print(f"🧠 Pregunta: {pregunta}")
        inicio = time.time()

        bruto = interpretar_pregunta(pregunta)
        formato = limpiar_formato(bruto)
        funcion, a, b = extraer_funcion_y_limites(formato)

        if None in (funcion, a, b):
            print(f"❌ Formato inválido: '{formato}'")
            errores_formato += 1
            resultados_csv.append([pregunta, esperado, "-", "-", "-", "Formato inválido"])
            continue

        resultado = consultar_api(funcion, a, b)
        if resultado is None:
            print(f"⚠️  Error al consultar la API.")
            errores_api += 1
            resultados_csv.append([pregunta, esperado, "-", "-", "-", "Error API"])
            continue

        tiempo = time.time() - inicio
        tiempos.append(tiempo)
        diferencia = abs(resultado - esperado)
        correcto = diferencia <= TOLERANCIA

        estado = "✅ Correcto" if correcto else "❌ Incorrecto"
        if correcto:
            aciertos += 1

        print(f"{estado} | Esperado: {esperado:.6f} | Obtenido: {resultado:.6f} | Δ: {diferencia:.2e} | ⏱ {tiempo:.2f}s")
        print("-" * 70)

        resultados_csv.append([
            pregunta, esperado, resultado, f"{diferencia:.2e}", f"{tiempo:.2f}", estado
        ])

    # Guardar CSV
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Pregunta", "Esperado", "Obtenido", "Diferencia", "Tiempo (s)", "Estado"])
        writer.writerows(resultados_csv)

    total = len(PRUEBAS)
    media_tiempo = sum(tiempos) / len(tiempos) if tiempos else 0
    print(f"\n🎯 Aciertos: {aciertos}/{total} ({aciertos/total:.1%})")
    print(f"📉 Errores de formato: {errores_formato}")
    print(f"⚠️ Errores de API: {errores_api}")
    print(f"⏱ Tiempo promedio por consulta: {media_tiempo:.2f} segundos")
    print(f"📁 Resultados guardados en: {CSV_OUTPUT}\n")

if __name__ == "__main__":
    evaluar()
