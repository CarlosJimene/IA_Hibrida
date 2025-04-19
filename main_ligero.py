from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from sympy import symbols, sympify, denom, solveset, S
from sympy.calculus.util import singularities
from scipy.integrate import quad
import numpy as np
import uvicorn

app = FastAPI()
x = symbols('x')

class InputDatos(BaseModel):
    funcion: str
    a: Union[str, float]
    b: Union[str, float]

def es_segura_en_intervalo(expr, a_val, b_val):
    """
    Verifica que no haya discontinuidades reales en el intervalo [a_val, b_val].
    Comprueba denominadores y singularidades simbólicas.
    """
    try:
        d = denom(expr)
        raices = solveset(d, x, domain=S.Reals)
        for r in raices:
            if r.is_real:
                r_val = float(r.evalf())
                if a_val < r_val < b_val:
                    return False
        sing_points = singularities(expr, x)
        for s in sing_points:
            if s.is_real:
                s_val = float(s.evalf())
                if a_val < s_val < b_val:
                    return False
        return True
    except:
        return False

@app.post("/resolver-integral-light")
def resolver_integral_light(datos: InputDatos):
    try:
        # Procesamiento de entrada
        f_str = datos.funcion.replace("^", "**").strip()
        f = sympify(f_str)

        a_val = float(sympify(str(datos.a)).evalf())
        b_val = float(sympify(str(datos.b)).evalf())
        if a_val >= b_val:
            raise ValueError("El límite inferior debe ser menor que el superior.")

        # Verificar que sea segura en el intervalo
        if not es_segura_en_intervalo(f, a_val, b_val):
            return {"error": "La función tiene discontinuidades en el intervalo."}

        # Crear función evaluable
        def f_lambda(v):
            return float(f.subs(x, v))

        # Calcular integral numérica
        resultado, error = quad(f_lambda, a_val, b_val)

        # LaTeX simple
        integral_repr = f"\u222b_{{{datos.a}}}^{{{datos.b}}} {datos.funcion} dx"

        # Respuesta JSON
        return {
            "funcion": datos.funcion,
            "a": datos.a,
            "b": datos.b,
            "integral_definida": integral_repr,
            "resultado_numerico": resultado,
            "error_estimado": error
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("✅ API ligera lista en http://127.0.0.1:8080/resolver-integral-light")
    uvicorn.run(app, host="127.0.0.1", port=8080)
