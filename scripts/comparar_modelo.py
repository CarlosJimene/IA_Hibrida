from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import numpy as np

# 📍 Ruta del nuevo modelo entrenado con corpus validado por la API
MODEL_DIR = "models/t5_integrador_api"

# Casos de prueba: (entrada → salida esperada)
test_cases = [
    ("x**2 from 0 to 1", "0.333333"),
    ("x from 0 to 2", "2.0"),
    ("cos(x) from 0 to 3.1416", "0.0"),
    ("sin(x) from 0 to 3.1416", "2.0"),
    ("exp(x) from 0 to 1", "1.718281"),
    ("x**3 from -1 to 1", "0.0"),
    ("1/(1 + x**2) from 0 to 1", "0.785398"),
    ("x**2 + 2*x + 1 from 0 to 1", "2.333333"),
    ("ln(x) from 1 to 2", "0.386294"),
    ("tan(x) from 0 to 0.5", "0.255412"),
]

# Cargar modelo entrenado
tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Evaluar predicciones
aciertos = 0
print("\n📊 RESULTADOS DEL MODELO t5_integrador_api:\n")

for entrada, esperado in test_cases:
    inputs = tokenizer(entrada, return_tensors="pt", padding=True).to(device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=32
        )

    pred = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

    try:
        esperado_float = float(esperado)
        pred_float = float(pred)
        diff = abs(pred_float - esperado_float)
        correcto = diff <= 0.01
    except:
        correcto = False

    estado = "✅" if correcto else "❌"
    print(f"{estado} Input: {entrada}")
    print(f"   → Esperado: {esperado}")
    print(f"   → Modelo:   {pred}\n")
    aciertos += int(correcto)

# Resumen
porcentaje = (aciertos / len(test_cases)) * 100
print(f"🎯 Aciertos: {aciertos} de {len(test_cases)} ({porcentaje:.1f}%)")
