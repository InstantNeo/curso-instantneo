"""
Script de prueba para verificar que todas las skills funcionan correctamente
"""

import sys
from pathlib import Path

# Agregar el path de instantneo si es necesario
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "instantneo"))

from instantneo.skills import skill


def test_skills():
    """Prueba todas las skills de la biblioteca"""

    print("=" * 70)
    print("PRUEBA DE SKILLS DE LA BIBLIOTECA")
    print("=" * 70)

    # ========================================================================
    # Test 1: Skills Básicas
    # ========================================================================
    print("\n[TEST 1] Skills Básicas")
    print("-" * 70)

    from basicas.suma import sumar_lista
    from basicas.promedio import calcular_promedio

    numeros = [10, 20, 30, 40, 50]

    suma = sumar_lista(numeros)
    print(f"Suma de {numeros}: {suma}")
    assert suma == 150, f"Error: se esperaba 150, se obtuvo {suma}"

    promedio = calcular_promedio(numeros)
    print(f"Promedio de {numeros}: {promedio}")
    assert promedio == 30, f"Error: se esperaba 30, se obtuvo {promedio}"

    print("✓ Skills básicas funcionan correctamente")

    # ========================================================================
    # Test 2: Skills de Estadística
    # ========================================================================
    print("\n[TEST 2] Skills de Estadística")
    print("-" * 70)

    from estadisticas.mediana import calcular_mediana
    from estadisticas.desviacion_std import calcular_desviacion_estandar

    # Test mediana con número impar de elementos
    mediana_impar = calcular_mediana([1, 2, 3, 4, 5])
    print(f"Mediana de [1,2,3,4,5]: {mediana_impar}")
    assert mediana_impar == 3, f"Error: se esperaba 3, se obtuvo {mediana_impar}"

    # Test mediana con número par de elementos
    mediana_par = calcular_mediana([1, 2, 3, 4])
    print(f"Mediana de [1,2,3,4]: {mediana_par}")
    assert mediana_par == 2.5, f"Error: se esperaba 2.5, se obtuvo {mediana_par}"

    # Test desviación estándar
    desv = calcular_desviacion_estandar([10, 20, 30, 40, 50])
    print(f"Desviación estándar de [10,20,30,40,50]: {desv:.2f}")
    # Para [10,20,30,40,50], la desv. std. muestral es aproximadamente 15.81
    assert 15.5 < desv < 16.0, f"Error: se esperaba ~15.81, se obtuvo {desv}"

    print("✓ Skills de estadística funcionan correctamente")

    # ========================================================================
    # Test 3: Skills de ML
    # ========================================================================
    print("\n[TEST 3] Skills de Machine Learning")
    print("-" * 70)

    from ml.regresion_simple import regresion_lineal_simple

    # Datos perfectamente lineales: y = 2x
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    resultado = regresion_lineal_simple(x, y)
    print(f"Regresión lineal para x={x}, y={y}:")
    print(f"  Pendiente: {resultado['pendiente']:.2f}")
    print(f"  Intercepto: {resultado['intercepto']:.2f}")
    print(f"  R²: {resultado['r_cuadrado']:.4f}")

    # Para y = 2x, esperamos pendiente=2, intercepto=0, R²=1
    assert abs(resultado['pendiente'] - 2.0) < 0.01, "Error en pendiente"
    assert abs(resultado['intercepto'] - 0.0) < 0.01, "Error en intercepto"
    assert abs(resultado['r_cuadrado'] - 1.0) < 0.01, "Error en R²"

    print("✓ Skills de ML funcionan correctamente")

    # ========================================================================
    # Resumen Final
    # ========================================================================
    print("\n" + "=" * 70)
    print("✓ TODAS LAS SKILLS PASARON LAS PRUEBAS")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_skills()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
