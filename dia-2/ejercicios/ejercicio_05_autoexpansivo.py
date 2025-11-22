"""
EJERCICIO 05: Agente Auto-Expansivo
====================================

OBJETIVO:
Crear un agente que puede expandir sus capacidades de forma dinámica
cargando skills bajo demanda desde una biblioteca externa cuando detecta
que no puede completar una tarea.

CONCEPTO:
Un agente auto-expansivo detecta cuando no tiene las capacidades necesarias
para completar una tarea, busca en una biblioteca de skills disponibles,
y se auto-expande cargando las skills necesarias dinámicamente.

SKILLS DISPONIBLES EN LA BIBLIOTECA:
- skills_biblioteca/basicas/suma.py - Sumar lista de números
- skills_biblioteca/basicas/promedio.py - Calcular promedio
- skills_biblioteca/estadisticas/mediana.py - Calcular mediana
- skills_biblioteca/estadisticas/desviacion_std.py - Desviación estándar
- skills_biblioteca/ml/regresion_simple.py - Regresión lineal simple

TU TAREA:
Implementar las tres funciones marcadas con TODO para crear un sistema
de expansión automática de capacidades.
"""

from instantneo import InstantNeo
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar (configurable desde .env)

GROQ_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.3-70b-versatile")  # Default si no está en .env

print(f"🔧 Modelo configurado: {GROQ_MODEL}")


# ============================================================================
# TODO 1: Implementar función que detecta si el agente puede procesar la tarea
# ============================================================================
def puede_procesar(respuesta: str) -> bool:
    """
    Analiza la respuesta del agente para determinar si puede procesar la tarea
    o si necesita expandir sus capacidades.

    Parameters
    ----------
    respuesta : str
        La respuesta del agente

    Returns
    -------
    bool
        True si el agente puede procesar (respuesta normal)
        False si el agente indica que no puede (necesita expansión)

    PISTAS:
    - Busca frases como "no puedo", "no tengo", "no dispongo"
    - Busca frases como "no cuento con", "no está disponible"
    - Considera minúsculas con .lower()
    """
    # TODO: Tu código aquí
    pass


# ============================================================================
# TODO 2: Implementar búsqueda de skills disponibles en la biblioteca
# ============================================================================
def buscar_skill_disponible(nombre_skill: str, biblioteca_path: str) -> str:
    """
    Busca un archivo de skill en la biblioteca que coincida con el nombre.

    Parameters
    ----------
    nombre_skill : str
        Nombre o descripción de la skill buscada
    biblioteca_path : str
        Ruta a la carpeta skills_biblioteca

    Returns
    -------
    str
        Ruta completa al archivo .py que contiene la skill, o None si no se encuentra

    PISTAS:
    - Busca en las subcarpetas: estadisticas/, ml/
    - Mapea palabras clave a archivos:
      * "mediana" -> estadisticas/mediana.py
      * "desviacion" o "std" -> estadisticas/desviacion_std.py
      * "regresion" -> ml/regresion_simple.py
    - Usa os.path.join() o Path() para construir rutas
    """
    # TODO: Tu código aquí
    pass


# ============================================================================
# TODO 3: Implementar el loop de expansión automática
# ============================================================================
def ejecutar_con_autoexpansion(agente: InstantNeo, query: str, biblioteca_path: str, max_intentos: int = 3):
    """
    Ejecuta un query con capacidad de auto-expansión.

    Si el agente no puede procesar la tarea:
    1. Detecta qué skill necesita
    2. Busca la skill en la biblioteca
    3. Pregunta al usuario si desea cargarla
    4. Carga la skill dinámicamente
    5. Reintenta la ejecución

    Parameters
    ----------
    agente : InstantNeo
        El agente a expandir
    query : str
        La consulta del usuario
    biblioteca_path : str
        Ruta a la biblioteca de skills
    max_intentos : int
        Número máximo de intentos de expansión

    PISTAS:
    - Usa un loop for con range(max_intentos)
    - Llama a agente.run(query) en cada intento
    - Usa puede_procesar() para verificar la respuesta
    - Si no puede procesar:
      * Analiza la respuesta para detectar qué skill necesita
      * Usa buscar_skill_disponible() para encontrarla
      * Pregunta al usuario con input()
      * Carga con agente.load_skills.from_file(ruta)
    - Si puede procesar, imprime la respuesta y termina
    """
    # TODO: Tu código aquí
    pass


# ============================================================================
# CONFIGURACIÓN Y PRUEBAS
# ============================================================================

def main():
    """
    Función principal que prueba el sistema de auto-expansión.
    """
    # Configuración
    API_KEY = os.getenv("API_KEY", "tu-api-key-aqui")
    BIBLIOTECA_PATH = Path(__file__).parent.parent / "soluciones" / "skills_biblioteca"

    print("=" * 70)
    print("EJERCICIO 05: AGENTE AUTO-EXPANSIVO")
    print("=" * 70)

    # Crear agente con solo skills básicas
    agente = InstantNeo(
        api_key=API_KEY,
        provider="groq",
        model=GROQ_MODEL
    )

    # Cargar solo skills básicas al inicio
    skills_basicas = BIBLIOTECA_PATH / "basicas"
    agente.load_skills.from_folder(str(skills_basicas))

    print(f"\nSkills iniciales: {agente.get_skill_names()}")
    print("\n" + "=" * 70)

    # ========================================================================
    # QUERY 1: Promedio (debe funcionar - ya tiene la skill)
    # ========================================================================
    print("\n[QUERY 1] Calcular promedio de [10, 20, 30, 40, 50]")
    print("-" * 70)
    ejecutar_con_autoexpansion(
        agente,
        "Calcula el promedio de estos números: 10, 20, 30, 40, 50",
        str(BIBLIOTECA_PATH)
    )

    # ========================================================================
    # QUERY 2: Desviación estándar (requiere expansión)
    # ========================================================================
    print("\n" + "=" * 70)
    print("\n[QUERY 2] Calcular desviación estándar de [10, 20, 30, 40, 50]")
    print("-" * 70)
    ejecutar_con_autoexpansion(
        agente,
        "Calcula la desviación estándar de estos números: 10, 20, 30, 40, 50",
        str(BIBLIOTECA_PATH)
    )

    # ========================================================================
    # QUERY 3: Regresión lineal (requiere expansión)
    # ========================================================================
    print("\n" + "=" * 70)
    print("\n[QUERY 3] Regresión lineal simple")
    print("-" * 70)
    ejecutar_con_autoexpansion(
        agente,
        "Calcula la regresión lineal simple para x=[1,2,3,4,5] y y=[2,4,6,8,10]",
        str(BIBLIOTECA_PATH)
    )

    # Mostrar skills finales
    print("\n" + "=" * 70)
    print(f"\nSkills finales: {agente.get_skill_names()}")
    print("\n" + "=" * 70)


# ============================================================================
# CRITERIOS DE ÉXITO
# ============================================================================
"""
Tu implementación debe cumplir con:

1. DETECCIÓN DE CAPACIDADES:
   - puede_procesar() identifica correctamente cuando el agente no puede procesar
   - Detecta frases negativas en la respuesta

2. BÚSQUEDA DE SKILLS:
   - buscar_skill_disponible() encuentra archivos en la biblioteca
   - Mapea palabras clave a archivos correctamente

3. AUTO-EXPANSIÓN:
   - El agente comienza con solo skills básicas
   - Al detectar que no puede hacer una tarea, busca la skill necesaria
   - Pregunta al usuario antes de cargar
   - Carga la skill dinámicamente con from_file()
   - Reintenta la ejecución exitosamente

4. EJECUCIÓN CORRECTA:
   - Query 1 (promedio) funciona inmediatamente
   - Query 2 (desv. std) se expande y luego funciona
   - Query 3 (regresión) se expande y luego funciona
   - Skills finales > Skills iniciales

BONUS:
- Detección automática del nombre de skill desde el query
- Manejo de errores si la skill no existe
- Evitar cargar la misma skill múltiples veces
"""


if __name__ == "__main__":
    main()
