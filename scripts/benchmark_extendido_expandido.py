import time
import csv
from predict_hibrido_expandido import predecir_integral_hibrida

# Preguntas más variadas y naturales
preguntas = [
    ("Calcula la integral de x**2 entre 0 y 1", 0.333333),
    ("Calcula la integral de x entre 0 y 2", 2.0),
    ("Integral de cos(x) entre 0 y 3.1416", 0.0),
    ("Integral de sin(x) desde 0 hasta pi", 2.0),
    ("Integral de e**x entre 0 y 1", 1.718281),
    ("¿Cuál es la integral de x**3 entre -1 y 1?", 0.0),
    ("Evalúa ∫ 1/(1 + x**2) entre 0 y 1", 0.785398),
    ("Integral definida de ln(x) entre 1 y 2", 0.386294),
    ("Calcula la integral de x**2 + 2*x + 1 entre 0 y 1", 2.333333),
    ("Integral de tan(x) entre 0 y 0.5", 0.255412),
    ("Integra x^4 de -1 a 1", 0.4),
    ("Calcula ∫ cos(x**2) desde -1 hasta 1", 1.329340),
    ("Integral de sqrt(x) entre 0 y 4", 5.333330),
    ("¿Cuál es la integral de exp(-x**2) de -1 a 1?", 1.49365),
    ("Calcula la integral de 1/x entre 1 y e", 1.0),
    ("Evalúa ∫ sec(x)**2 entre 0 y 0.5", 0.255412),
    ("Integral de sin(x**2) entre 0 y 1", 0.310270),
    ("Integral de 1/(x+1) entre 0 y 1", 0.693147),
    ("Integral definida de 3*x**3 - x**2 + 2*x + 1 entre -1 y 1", 2.0),
    ("Calcula la integral de x*cos(x) entre 0 y pi", -2.0),
]

def evaluar():
    aciertos = 0
    errores_api = 0
    errores_formato = 0
    total = len(preguntas)
    tiempos = []

    print("\n📊 EVALUACIÓN EXTENDIDA AVANZADA DEL SISTEMA HÍBRIDO (formateador expandido)\n")

    with open("resultados_benchmark_expandido.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Pregunta", "Esperado", "Obtenido", "Diferencia", "Tiempo (s)"])

        for pregunta, esperado in preguntas:
            print(f"🧠 {pregunta}")
            start = time.time()
            respuesta = predecir_integral_hibrida(pregunta)
            duracion = time.time() - start
            tiempos.append(duracion)

            try:
                if respuesta is None:
                    raise ValueError("Error al consultar la API o formato inválido")

                obtenido = float(respuesta)
                diferencia = abs(obtenido - esperado)

                correcto = diferencia < 1e-3
                resultado_str = "✅ Correcto" if correcto else "❌ Incorrecto"

                print(f"{resultado_str} | Esperado: {esperado:.6f} | Obtenido: {obtenido:.6f} | Δ: {diferencia:.2e} | ⏱ {duracion:.2f}s")
                print("-" * 70)

                writer.writerow([pregunta, esperado, obtenido, diferencia, f"{duracion:.2f}"])

                if correcto:
                    aciertos += 1
                else:
                    errores_formato += 1

            except Exception as e:
                print(f"⚠️  {e}")
                if "API" in str(e):
                    errores_api += 1
                else:
                    errores_formato += 1

    print(f"\n🎯 Aciertos: {aciertos}/{total} ({100*aciertos/total:.1f}%)")
    print(f"📉 Errores de formato: {errores_formato}")
    print(f"⚠️ Errores de API: {errores_api}")
    print(f"⏱ Tiempo promedio por consulta: {sum(tiempos)/len(tiempos):.2f} segundos")
    print("📁 Resultados guardados en: resultados_benchmark_expandido.csv")

if __name__ == "__main__":
    evaluar()
