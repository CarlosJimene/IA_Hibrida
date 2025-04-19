# 🧠 IA Híbrida para Resolución de Integrales Definidas

Este proyecto implementa una **IA híbrida** capaz de interpretar enunciados matemáticos escritos en lenguaje natural y calcular de forma precisa **integrales definidas**, combinando un modelo **T5 formateador entrenado a medida** con una **API simbólica-numérica** basada en `SymPy` y `Scipy`.

> 🎓 *Proyecto desarrollado como Trabajo de Fin de Grado (TFG).*  
> 🏛 *Facultad de Ciencias – Universidad Autónoma (2025)*

---

## 🚀 ¿Cómo funciona?

El sistema se basa en dos componentes principales:

### 1. 🧠 Modelo T5 Formateador
Un modelo **T5 small** entrenado específicamente para:

- Interpretar preguntas ambiguas o en lenguaje natural.  
  Ejemplo: _"¿Cuál es la integral de e^x entre 0 y 1?"_
- Devolver una **expresión formateada estándar**.  
  Ejemplo: `exp(x) from 0 to 1`

Esto permite separar la comprensión lingüística del razonamiento matemático.

---

### 2. 🔢 API Numérica Ligera (FastAPI)
Una API desarrollada en FastAPI que:

- **Valida y evalúa** la integral simbólicamente con `SymPy`.
- **Calcula el resultado numérico** con `scipy.integrate.quad`.
- Informa sobre discontinuidades, errores o dominios no válidos.

---

## 📈 Resultados

Evaluado con un benchmark de 20 preguntas naturales:

- ✅ **Precisión híbrida final:** 65%
- 🧠 Entiende formatos como:  
  - `desde ... hasta ...`  
  - `∫ ... de ... a ...`  
  - `¿Cuál es la integral de ...?`

---

## 📁 Estructura del Proyecto

```
IA_Hibrida/
│
├── data/
│   └── corpus_integrales.jsonl               # Corpus reducido
│
├── models/
│   └── t5_formateador/                       # Carpeta del modelo T5 entrenado
│
├── scripts/
│   ├── train_t5_formateador.py               # Entrenamiento del modelo
│   ├── predict_hibrido.py                    # Predicción híbrida (T5 + API)
│   ├── comparar_hibrido.py                   # Evaluación de precisión
│   ├── benchmark_extendido.py                # Pruebas con preguntas variadas
│   └── visualizar_benchmark.py               # Gráficos de resultados
│
├── main_ligero.py                            # API local de cálculo simbólico
├── requirements.txt                          # Dependencias del proyecto
├── README.md                                 # Este documento
└── .gitignore                                # Exclusiones para el repositorio
```

---

## 🧩 Requisitos

- Python 3.9+
- Bibliotecas:
  - `transformers`
  - `datasets`
  - `scipy`
  - `sympy`
  - `fastapi`
  - `uvicorn`
  - `matplotlib` (para visualizaciones opcionales)

Instalación rápida:

```bash
pip install -r requirements.txt
```

---

## 🔧 ¿Cómo usar?

### 1. Lanzar la API

```bash
python main_ligero.py
```

Verás:

```
✅ API ligera lista en http://127.0.0.1:8080/resolver-integral-light
```

---

### 2. Probar predicción híbrida

```bash
python scripts/predict_hibrido.py "Calcula la integral de x**2 entre 0 y 1"
```

Resultado esperado:

```
✅ Resultado: 0.333333
```

---

### 3. Ejecutar benchmark extendido

```bash
python scripts/benchmark_extendido.py
```

Los resultados se guardarán en `resultados_benchmark.csv`.

---

## 🤖 ¿Por qué una IA híbrida?

| Técnica               | Ventaja                              | Desventaja                          |
|----------------------|---------------------------------------|-------------------------------------|
| Modelo LLM puro      | Entiende lenguaje natural             | Baja precisión matemática           |
| Motor simbólico puro | Precisión total con input válido      | Requiere entrada exacta             |
| **Híbrido (este)**   | Comprensión + exactitud matemática    | Necesita entrenamiento intermedio   |

---

## 🧑‍🎓 Autor

**Carlos [Apellido]**  
Estudiante de Grado en Matemáticas / Ingeniería  
Universidad Autónoma · 2025  
Contacto: carlo@email.com

---

## 📝 Licencia

Distribuido bajo licencia MIT.  
Puedes reutilizar, modificar y adaptar este código libremente.

---

✅ *¿Quieres integrar esta IA en tu web? Consulta el archivo `main_ligero.py` o contáctame para más detalles.*