"""
EJERCICIO 05: Agente Auto-Expansivo - SOLUCIÓN
==============================================

Esta es la solución completa del ejercicio de agente auto-expansivo.

El agente puede:
1. Detectar cuando no tiene las capacidades necesarias
2. Buscar skills en una biblioteca externa
3. Cargar skills dinámicamente bajo demanda
4. Reintentar la ejecución con las nuevas capacidades
"""

from instantneo import InstantNeo
import os
from pathlib import Path
import re
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
# SOLUCIÓN 1: Detectar si el agente puede procesar la tarea
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
    """
    respuesta_lower = respuesta.lower()

    # Frases que indican que el agente NO puede procesar
    frases_negativas = [
        "no puedo",
        "no tengo",
        "no dispongo",
        "no cuento con",
        "no está disponible",
        "no tengo acceso",
        "no tengo la capacidad",
        "no tengo esa habilidad",
        "no tengo esa skill",
        "no tengo esa función",
        "no es posible",
        "no me es posible"
    ]

    # Si encuentra alguna frase negativa, no puede procesar
    for frase in frases_negativas:
        if frase in respuesta_lower:
            return False

    # Si no encuentra frases negativas, asumimos que puede procesar
    return True


# ============================================================================
# SOLUCIÓN 2: Buscar skills disponibles en la biblioteca
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
    """
    nombre_lower = nombre_skill.lower()

    # Mapeo de palabras clave a archivos
    mapeo_skills = {
        "mediana": "estadisticas/mediana.py",
        "desviacion": "estadisticas/desviacion_std.py",
        "std": "estadisticas/desviacion_std.py",
        "estandar": "estadisticas/desviacion_std.py",
        "regresion": "ml/regresion_simple.py",
        "regresión": "ml/regresion_simple.py",
        "lineal": "ml/regresion_simple.py",
    }

    # Buscar coincidencia
    for palabra_clave, archivo_relativo in mapeo_skills.items():
        if palabra_clave in nombre_lower:
            ruta_completa = os.path.join(biblioteca_path, archivo_relativo)
            if os.path.exists(ruta_completa):
                return ruta_completa

    return None


# ============================================================================
# SOLUCIÓN 3: Loop de expansión automática
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
    """
    for intento in range(max_intentos):
        print(f"\n[Intento {intento + 1}/{max_intentos}]")

        # Intentar ejecutar el query
        respuesta = agente.run(query)

        # Verificar si el agente puede procesar
        if puede_procesar(respuesta):
            print("\n✓ ÉXITO: El agente completó la tarea")
            print(f"\nRespuesta: {respuesta}")
            return

        # El agente no puede procesar - necesita expansión
        print("\n⚠ DETECCIÓN: El agente no puede completar la tarea")
        print(f"Respuesta del agente: {respuesta[:200]}...")

        # Detectar qué skill necesita (BONUS: análisis automático)
        skill_necesaria = detectar_skill_necesaria(query, respuesta)

        if not skill_necesaria:
            print("\n✗ ERROR: No se pudo determinar qué skill se necesita")
            continue

        print(f"\n→ Skill necesaria detectada: {skill_necesaria}")

        # Buscar la skill en la biblioteca
        ruta_skill = buscar_skill_disponible(skill_necesaria, biblioteca_path)

        if not ruta_skill:
            print(f"\n✗ ERROR: No se encontró la skill '{skill_necesaria}' en la biblioteca")
            continue

        print(f"→ Skill encontrada en: {ruta_skill}")

        # Preguntar al usuario si desea cargar la skill
        respuesta_usuario = input("\n¿Desea cargar esta skill? (s/n): ").strip().lower()

        if respuesta_usuario != 's':
            print("\n✗ Usuario canceló la carga de la skill")
            break

        # Cargar la skill dinámicamente
        try:
            print(f"\n→ Cargando skill desde {ruta_skill}...")
            agente.load_skills.from_file(ruta_skill)
            print(f"✓ Skill cargada exitosamente")
            print(f"Skills actuales: {agente.get_skill_names()}")
        except Exception as e:
            print(f"\n✗ ERROR al cargar la skill: {e}")
            continue

        # Continuar el loop para reintentar con la nueva skill

    # Si llegamos aquí, agotamos los intentos
    print(f"\n✗ Se agotaron los {max_intentos} intentos sin completar la tarea")


# ============================================================================
# FUNCIÓN BONUS: Detección automática de skill necesaria
# ============================================================================
def detectar_skill_necesaria(query: str, respuesta_agente: str) -> str:
    """
    Analiza el query y la respuesta del agente para determinar automáticamente
    qué skill se necesita.

    Parameters
    ----------
    query : str
        El query original del usuario
    respuesta_agente : str
        La respuesta del agente indicando que no puede procesar

    Returns
    -------
    str
        Nombre de la skill necesaria, o None si no se puede determinar
    """
    texto_completo = (query + " " + respuesta_agente).lower()

    # Palabras clave en orden de prioridad
    skills_keywords = [
        ("regresion|regresión|regression", "regresion"),
        ("desviacion|desviación|std|estandar|estándar|standard deviation", "desviacion"),
        ("mediana|median", "mediana"),
        ("promedio|media|average|mean", "promedio"),
        ("suma|sum", "suma"),
    ]

    for patron, skill_name in skills_keywords:
        if re.search(patron, texto_completo):
            return skill_name

    return None


# ============================================================================
# CONFIGURACIÓN Y PRUEBAS
# ============================================================================

def main():
    """
    Función principal que prueba el sistema de auto-expansión.
    """
    # Configuración
    API_KEY = os.getenv("GROQ_API_KEY")
    if not API_KEY:
        print("ERROR: No se encontró API_KEY en las variables de entorno")
        print("Por favor, configura tu API_KEY en un archivo .env")
        return

    BIBLIOTECA_PATH = Path(__file__).parent / "skills_biblioteca"

    print("=" * 70)
    print("EJERCICIO 05: AGENTE AUTO-EXPANSIVO - SOLUCIÓN")
    print("=" * 70)

    # Crear agente con solo skills básicas
    agente = InstantNeo(
        api_key=API_KEY,
        provider="groq",
        model=GROQ_MODEL,
        role_setup="Eres un asistente experto en matemáticas y estadísticas.",
    )

    # Cargar solo skills básicas al inicio
    skills_basicas = BIBLIOTECA_PATH / "basicas"
    if skills_basicas.exists():
        agente.load_skills.from_folder(str(skills_basicas))
        print(f"\n✓ Skills básicas cargadas desde: {skills_basicas}")
    else:
        print(f"\n⚠ ADVERTENCIA: No se encontró la carpeta de skills básicas en {skills_basicas}")

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
    print(f"\nExpansión exitosa: {len(agente.get_skill_names())} skills cargadas")
    print("\n" + "=" * 70)


# ============================================================================
# EXPLICACIÓN DE LA SOLUCIÓN
# ============================================================================
"""
CÓMO FUNCIONA:

1. DETECCIÓN DE CAPACIDADES (puede_procesar):
   - Busca frases negativas en la respuesta del agente
   - Si encuentra "no puedo", "no tengo", etc., retorna False
   - Esto indica que el agente necesita expandirse

2. BÚSQUEDA DE SKILLS (buscar_skill_disponible):
   - Usa un diccionario de mapeo palabra_clave -> archivo
   - Busca coincidencias en el nombre de la skill
   - Retorna la ruta completa al archivo .py

3. LOOP DE AUTO-EXPANSIÓN (ejecutar_con_autoexpansion):
   - Intenta ejecutar el query
   - Si falla, detecta qué skill necesita
   - Busca la skill en la biblioteca
   - Pregunta al usuario si desea cargarla
   - Carga la skill con load_skills.from_file()
   - Reintenta automáticamente

4. BONUS - DETECCIÓN AUTOMÁTICA:
   - Analiza el query y la respuesta del agente
   - Usa regex para buscar palabras clave
   - Determina automáticamente qué skill se necesita

FLUJO DE EJECUCIÓN:

Query 1 (promedio):
  → Ya tiene la skill → Ejecuta exitosamente

Query 2 (desv. std):
  → Intento 1: No puede → Detecta "desviacion"
  → Busca en biblioteca → Encuentra desviacion_std.py
  → Pregunta al usuario → Usuario acepta
  → Carga skill → Intento 2: Ejecuta exitosamente

Query 3 (regresión):
  → Intento 1: No puede → Detecta "regresion"
  → Busca en biblioteca → Encuentra regresion_simple.py
  → Pregunta al usuario → Usuario acepta
  → Carga skill → Intento 2: Ejecuta exitosamente

RESULTADO:
Skills iniciales: ['sumar_lista', 'calcular_promedio']
Skills finales: ['sumar_lista', 'calcular_promedio', 'calcular_desviacion_estandar', 'regresion_lineal_simple']

El agente se expandió automáticamente de 2 skills a 4 skills!
"""


if __name__ == "__main__":
    main()
