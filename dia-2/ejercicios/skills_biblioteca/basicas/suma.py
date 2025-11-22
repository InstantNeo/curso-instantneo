"""
Skill básica: Suma de números en una lista
"""
from instantneo.skills import skill
from typing import List


@skill(
    name="sumar_lista",
    description="Calcula la suma de todos los números en una lista",
    tags=["basicas", "matematicas"]
)
def sumar_lista(numeros: List[float]) -> float:
    """
    Calcula la suma de todos los números en una lista.

    Parameters
    ----------
    numeros : List[float]
        Lista de números a sumar

    Returns
    -------
    float
        La suma de todos los números
    """
    if not numeros:
        return 0.0
    return sum(numeros)
