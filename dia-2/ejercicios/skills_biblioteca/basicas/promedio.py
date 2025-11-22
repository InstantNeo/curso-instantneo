"""
Skill básica: Promedio de números en una lista
"""
from instantneo.skills import skill
from typing import List


@skill(
    name="calcular_promedio",
    description="Calcula el promedio (media aritmética) de una lista de números",
    tags=["basicas", "matematicas", "estadisticas"]
)
def calcular_promedio(numeros: List[float]) -> float:
    """
    Calcula el promedio (media aritmética) de una lista de números.

    Parameters
    ----------
    numeros : List[float]
        Lista de números para calcular el promedio

    Returns
    -------
    float
        El promedio de los números

    Raises
    ------
    ValueError
        Si la lista está vacía
    """
    if not numeros:
        raise ValueError("No se puede calcular el promedio de una lista vacía")
    return sum(numeros) / len(numeros)
