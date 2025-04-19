from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import sys
from pathlib import Path

# ✅ Nuevo modelo entrenado con datos confirmados por la API
MODEL_DIR = Path("models/t5_integrador_api")

# Verificar uso correcto
if len(sys.argv) < 2:
    print("❌ Uso: python scripts/predict_t5.py \"<input del modelo>\"")
    print("   Ejemplo: python scripts/predict_t5.py \"x**2 from 0 to 1\"")
    sys.exit(1)

# Entrada desde línea de comandos
input_text = sys.argv[1]

# Cargar tokenizer y modelo
tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Preparar entrada
inputs = tokenizer(input_text, return_tensors="pt", padding=True).to(device)

# Generar salida
with torch.no_grad():
    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=32
    )

# Decodificar y mostrar
respuesta = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("\n📥 Entrada:", input_text)
print("📤 Salida del modelo:", respuesta)
