"""
Script predict_hibrido_final.py
--------------------------------
Este script utiliza un modelo T5 entrenado para interpretar lenguaje natural
y convertirlo en formato estructurado compatible con una API de integración.
Posteriormente, realiza la consulta a la API y muestra el resultado numérico de la integral.
"""

import sys
import requests
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Ruta del modelo formateador entrenado
MODEL_PATH = "models/t5_formateador"

# URL de la API ligera que resuelve la integral
API_URL = "http://127.0.0.1:8080/resolver-integral-light"

# Verificar argumento
if len(sys.argv) < 2:
    print("❌ Uso: python scripts/predict_hibrido.py \"<pregunta>\"")
    print("   Ejemplo: python scripts/predict_hibrido.py \"Calcula la integral de x**2 entre 0 y 1\"")
    sys.exit(1)

pregunta = sys.argv[1]

# Carga del modelo y tokenizador
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Paso 1: El modelo T5 convierte la pregunta a formato estructurado
inputs = tokenizer(pregunta, return_tensors="pt").to(device)
with torch.no_grad():
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=32
    )

formato = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# Paso 2: Extraer función e intervalos [a,b] del formato
try:
    funcion, resto = formato.split(" from ")
    a_str, b_str = resto.split(" to ")
    payload = {
        "funcion": funcion.strip(),
        "a": float(a_str.strip()),
        "b": float(b_str.strip())
    }
except Exception as e:
    print(f"❌ El modelo no generó un formato válido: '{formato}'")
    print(f"🔍 Error al extraer función y límites: {e}")
    sys.exit(1)

# Paso 3: Envío a la API y obtención del resultado
try:
    res = requests.post(API_URL, json=payload, timeout=10)
    if res.status_code == 200:
        data = res.json()
        resultado = data.get("resultado_numerico", "Sin respuesta")
        print("\n📨 Pregunta:", pregunta)
        print("🧠 Formato generado por IA:", formato)
        print("🧮 Resultado exacto vía API:", resultado)
    else:
        print(f"❌ Error en respuesta de la API (código {res.status_code})")
except Exception as e:
    print("❌ Error al consultar la API:", e)
