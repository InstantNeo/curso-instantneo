"""
Skill estadística: Desviación estándar
"""
from instantneo.skills import skill
from typing import List
import math


@skill(
    name="calcular_desviacion_estandar",
    description="Calcula la desviación estándar de una lista de números",
    tags=["estadisticas", "matematicas"]
)
def calcular_desviacion_estandar(numeros: List[float], muestral: bool = True) -> float:
    """
    Calcula la desviación estándar de una lista de números.

    La desviación estándar es una medida de dispersión que indica cuánto
    se alejan los valores de la media.

    Parameters
    ----------
    numeros : List[float]
        Lista de números para calcular la desviación estándar
    muestral : bool, optional
        Si True, calcula la desviación estándar muestral (n-1).
        Si False, calcula la desviación poblacional (n).
        Por defecto True.

    Returns
    -------
    float
        La desviación estándar de los números

    Raises
    ------
    ValueError
        Si la lista está vacía o tiene un solo elemento cuando muestral=True
    """
    if not numeros:
        raise ValueError("No se puede calcular la desviación estándar de una lista vacía")

    if muestral and len(numeros) == 1:
        raise ValueError("No se puede calcular la desviación estándar muestral de un solo valor")

    # Calcular la media
    media = sum(numeros) / len(numeros)

    # Calcular la suma de las diferencias al cuadrado
    suma_cuadrados = sum((x - media) ** 2 for x in numeros)

    # Dividir por n-1 (muestral) o n (poblacional)
    divisor = len(numeros) - 1 if muestral else len(numeros)

    # Calcular la varianza y luego la desviación estándar
    varianza = suma_cuadrados / divisor
    desviacion = math.sqrt(varianza)

    return desviacion
