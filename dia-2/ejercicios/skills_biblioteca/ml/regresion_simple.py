"""
Skill de Machine Learning: Regresión lineal simple
"""
from instantneo.skills import skill
from typing import List, Dict


@skill(
    name="regresion_lineal_simple",
    description="Calcula la regresión lineal simple (y = mx + b) dados dos conjuntos de datos",
    tags=["ml", "machine_learning", "estadisticas", "regresion"]
)
def regresion_lineal_simple(x: List[float], y: List[float]) -> Dict[str, float]:
    """
    Calcula la regresión lineal simple utilizando el método de mínimos cuadrados.

    La regresión lineal simple encuentra la mejor línea recta (y = mx + b) que
    se ajusta a un conjunto de puntos de datos.

    Parameters
    ----------
    x : List[float]
        Lista de valores de la variable independiente
    y : List[float]
        Lista de valores de la variable dependiente

    Returns
    -------
    Dict[str, float]
        Diccionario con las claves:
        - 'pendiente': El coeficiente m (pendiente)
        - 'intercepto': El coeficiente b (intercepto)
        - 'r_cuadrado': El coeficiente de determinación R²

    Raises
    ------
    ValueError
        Si las listas están vacías, tienen diferentes longitudes,
        o tienen menos de 2 puntos
    """
    if not x or not y:
        raise ValueError("Las listas no pueden estar vacías")

    if len(x) != len(y):
        raise ValueError("Las listas x e y deben tener la misma longitud")

    if len(x) < 2:
        raise ValueError("Se necesitan al menos 2 puntos para calcular la regresión")

    n = len(x)

    # Calcular medias
    media_x = sum(x) / n
    media_y = sum(y) / n

    # Calcular la pendiente (m) usando mínimos cuadrados
    numerador = sum((x[i] - media_x) * (y[i] - media_y) for i in range(n))
    denominador = sum((x[i] - media_x) ** 2 for i in range(n))

    if denominador == 0:
        raise ValueError("Todos los valores de x son iguales, no se puede calcular la regresión")

    pendiente = numerador / denominador

    # Calcular el intercepto (b)
    intercepto = media_y - pendiente * media_x

    # Calcular R² (coeficiente de determinación)
    # R² = 1 - (SS_res / SS_tot)
    y_pred = [pendiente * x[i] + intercepto for i in range(n)]
    ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y[i] - media_y) ** 2 for i in range(n))

    r_cuadrado = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

    return {
        'pendiente': pendiente,
        'intercepto': intercepto,
        'r_cuadrado': r_cuadrado
    }
