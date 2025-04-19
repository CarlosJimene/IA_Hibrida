import json
from pathlib import Path

INPUT_FILE = "data/integrales_confirmadas_por_api.jsonl"
OUTPUT_FILE = "data/integrales_formato_semantico.jsonl"

Path("data").mkdir(exist_ok=True)

# Cargar corpus validado
with open(INPUT_FILE, "r", encoding="utf-8") as f_in:
    lineas = [json.loads(line) for line in f_in]

# Transformar al nuevo formato semántico
nuevos_ejemplos = []
for entrada in lineas:
    try:
        raw = entrada["input"]
        if "from" not in raw:
            continue

        funcion, intervalo = raw.split(" from ")
        a, b = intervalo.split(" to ")

        pregunta = f"Calcula la integral de {funcion.strip()} entre {a.strip()} y {b.strip()}"
        salida = f"{funcion.strip()} from {a.strip()} to {b.strip()}"

        nuevos_ejemplos.append({
            "input": pregunta,
            "output": salida
        })

    except Exception as e:
        continue  # Saltar errores aislados

# Guardar nuevo corpus
with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    for ejemplo in nuevos_ejemplos:
        json.dump(ejemplo, f_out)
        f_out.write("\n")

print(f"✅ Corpus semántico generado: {len(nuevos_ejemplos)} muestras en {OUTPUT_FILE}")
