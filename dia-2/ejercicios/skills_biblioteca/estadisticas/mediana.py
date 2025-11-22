"""
Skill estadística: Mediana de una lista de números
"""
from instantneo.skills import skill
from typing import List


@skill(
    name="calcular_mediana",
    description="Calcula la mediana de una lista de números",
    tags=["estadisticas", "matematicas"]
)
def calcular_mediana(numeros: List[float]) -> float:
    """
    Calcula la mediana de una lista de números.

    La mediana es el valor que separa la mitad superior de la mitad inferior
    de una muestra de datos. Si hay un número par de observaciones, la mediana
    es el promedio de los dos valores centrales.

    Parameters
    ----------
    numeros : List[float]
        Lista de números para calcular la mediana

    Returns
    -------
    float
        La mediana de los números

    Raises
    ------
    ValueError
        Si la lista está vacía
    """
    if not numeros:
        raise ValueError("No se puede calcular la mediana de una lista vacía")

    sorted_nums = sorted(numeros)
    n = len(sorted_nums)

    if n % 2 == 0:
        # Si hay número par de elementos, promedio de los dos del medio
        return (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
    else:
        # Si hay número impar, el elemento del medio
        return sorted_nums[n // 2]
