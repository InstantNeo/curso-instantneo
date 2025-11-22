# Skills Biblioteca

Biblioteca de skills organizadas por categorías para usar con InstantNeo.

## Estructura

```
skills_biblioteca/
├── basicas/              # Operaciones matemáticas básicas
│   ├── suma.py          # sumar_lista()
│   └── promedio.py      # calcular_promedio()
├── estadisticas/        # Análisis estadístico
│   ├── mediana.py       # calcular_mediana()
│   └── desviacion_std.py # calcular_desviacion_estandar()
└── ml/                  # Machine Learning
    └── regresion_simple.py # regresion_lineal_simple()
```

## Skills Disponibles

### Básicas

**sumar_lista(numeros: List[float]) -> float**
- Calcula la suma de todos los números en una lista
- Tags: `basicas`, `matematicas`

**calcular_promedio(numeros: List[float]) -> float**
- Calcula el promedio (media aritmética) de una lista de números
- Tags: `basicas`, `matematicas`, `estadisticas`

### Estadísticas

**calcular_mediana(numeros: List[float]) -> float**
- Calcula la mediana de una lista de números
- Tags: `estadisticas`, `matematicas`

**calcular_desviacion_estandar(numeros: List[float], muestral: bool = True) -> float**
- Calcula la desviación estándar de una lista de números
- Parámetros:
  - `muestral=True`: desviación estándar muestral (n-1)
  - `muestral=False`: desviación estándar poblacional (n)
- Tags: `estadisticas`, `matematicas`

### Machine Learning

**regresion_lineal_simple(x: List[float], y: List[float]) -> Dict[str, float]**
- Calcula la regresión lineal simple (y = mx + b) usando mínimos cuadrados
- Retorna:
  - `pendiente`: coeficiente m
  - `intercepto`: coeficiente b
  - `r_cuadrado`: coeficiente de determinación R²
- Tags: `ml`, `machine_learning`, `estadisticas`, `regresion`

## Uso

### Cargar una skill individual

```python
from instantneo import InstantNeo

agente = InstantNeo(api_key="...", provider="openai")

# Cargar una skill específica
agente.load_skills.from_file("skills_biblioteca/basicas/promedio.py")
```

### Cargar todas las skills de una categoría

```python
# Cargar todas las skills básicas
agente.load_skills.from_folder("skills_biblioteca/basicas")

# Cargar todas las skills de estadística
agente.load_skills.from_folder("skills_biblioteca/estadisticas")
```

### Cargar bajo demanda (Ejercicio 05)

El ejercicio 05 demuestra cómo cargar skills dinámicamente cuando el agente
detecta que las necesita:

```python
# El agente empieza solo con skills básicas
agente.load_skills.from_folder("skills_biblioteca/basicas")

# Cuando necesita una skill de estadística, la carga dinámicamente
agente.load_skills.from_file("skills_biblioteca/estadisticas/desviacion_std.py")
```

## Pruebas

Ejecuta el script de pruebas para verificar que todas las skills funcionan:

```bash
cd skills_biblioteca
python test_skills.py
```

## Notas

- Todas las skills están decoradas con `@skill`
- Todas usan type hints para parámetros y retorno
- Todas tienen docstrings en formato NumPy/Google
- Las skills NO requieren dependencias externas (numpy, scipy, etc.)
- Implementaciones puras en Python para máxima compatibilidad
