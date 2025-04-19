import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta del CSV (ajusta si es necesario)
CSV_PATH = "resultados_benchmark.csv"

def visualizar_resultados():
    if not os.path.exists(CSV_PATH):
        print(f"❌ No se encontró el archivo {CSV_PATH}")
        return

    # Leer el CSV
    df = pd.read_csv(CSV_PATH)

    # Contadores para gráficas
    estado_counts = df["Estado"].value_counts()
    errores_formato = estado_counts.get("Formato inválido", 0)
    errores_api = estado_counts.get("Error API", 0)
    aciertos = sum("Correcto" in str(e) for e in df["Estado"])
    incorrectos = sum("Incorrecto" in str(e) for e in df["Estado"])

    # -------- Gráfico 1: Aciertos y errores --------
    fig1, ax1 = plt.subplots()
    ax1.bar(["Correctos", "Incorrectos", "Formato inválido", "Error API"],
            [aciertos, incorrectos, errores_formato, errores_api],
            edgecolor='black')
    ax1.set_ylabel("Cantidad")
    ax1.set_title("Resultados del Benchmark")
    ax1.grid(axis="y")

    # -------- Gráfico 2: Tiempo por consulta --------
    fig2, ax2 = plt.subplots()
    df_validos = df[df["Tiempo (s)"].notna()]
    ax2.plot(df_validos.index, df_validos["Tiempo (s)"], marker='o', linestyle='-')
    ax2.set_title("Tiempo por Consulta")
    ax2.set_xlabel("Consulta #")
    ax2.set_ylabel("Tiempo (s)")
    ax2.grid(True)

    # Mostrar todo
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualizar_resultados()
