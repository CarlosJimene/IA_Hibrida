import requests

API_URL = "http://127.0.0.1:8080/resolver-integral-light"

# Casos de prueba conocidos
test_cases = [
    ("x**2", 0, 1, 0.333333),
    ("x", 0, 2, 2.0),
    ("cos(x)", 0, 3.1416, 0.0),
    ("sin(x)", 0, 3.1416, 2.0),
    ("exp(x)", 0, 1, 1.718281),
    ("x**3", -1, 1, 0.0),
    ("1/(1 + x**2)", 0, 1, 0.785398),
    ("x**2 + 2*x + 1", 0, 1, 2.333333),
    ("ln(x)", 1, 2, 0.386294),
    ("tan(x)", 0, 0.5, 0.255412),
]

aciertos = 0
tolerancia = 0.01  # Error numérico tolerable

print("\n📊 RESULTADOS DE LA API NUMÉRICA:\n")

for funcion, a, b, esperado in test_cases:
    payload = {
        "funcion": funcion,
        "a": float(a),
        "b": float(b)
    }

    try:
        res = requests.post(API_URL, json=payload, timeout=5)
        if res.status_code == 200:
            data = res.json()
            resultado = data.get("resultado_numerico")
            if resultado is not None:
                diff = abs(resultado - esperado)
                correcto = diff <= tolerancia
                estado = "✅" if correcto else "❌"
                print(f"{estado} {funcion} from {a} to {b}")
                print(f"   → Esperado: {esperado}")
                print(f"   → API:      {round(resultado, 6)}\n")
                aciertos += int(correcto)
            else:
                print(f"❌ Sin resultado para {funcion} de {a} a {b}")
        else:
            print(f"❌ Error {res.status_code} para {funcion} [{a}, {b}]")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

print(f"🎯 Aciertos: {aciertos} de {len(test_cases)}")
