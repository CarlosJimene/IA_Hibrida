import sys
import requests
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Configuración del modelo formateador expandido
MODEL_PATH = "models/t5_formateador_expandido"
API_URL = "http://127.0.0.1:8080/resolver-integral-light"

# Cargar modelo formateador expandido
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

def formatear_pregunta(pregunta):
    inputs = tokenizer(pregunta, return_tensors="pt", padding=True)
    output = model.generate(**inputs, max_length=64, num_beams=2, early_stopping=True)
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded

def consultar_api(formato):
    try:
        funcion, limites = formato.split(" from ")
        a, b = limites.strip().split(" to ")
        payload = {"funcion": funcion.strip(), "a": a.strip(), "b": b.strip()}
        response = requests.post(API_URL, json=payload, timeout=10)
        return response.json().get("resultado_numerico")
    except Exception as e:
        return f"⚠️ Error: {e}"

# ✅ Esta es la función que usará el benchmark
def predecir_integral_hibrida(pregunta: str):
    try:
        formato = formatear_pregunta(pregunta)
        resultado = consultar_api(formato)
        if isinstance(resultado, str) and resultado.startswith("⚠️"):
            return None
        return resultado
    except Exception as e:
        return None

# Modo interactivo si se ejecuta manualmente
def main():
    pregunta = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Pregunta: ")
    print(f"\n🧠 Pregunta: {pregunta}")
    
    formato = formatear_pregunta(pregunta)
    print(f"🔄 Interpretación: {formato}")

    resultado = consultar_api(formato)
    print(f"📐 Resultado: {resultado}")

if __name__ == "__main__":
    main()
