"""
Agente con Skills Básicas

Objetivo:
- Entender el decorador @skill
- Ver cómo el agente usa skills automáticamente
"""

from instantneo import InstantNeo, skill
import os
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ Error: No se encontró GROQ_API_KEY en .env")
    exit(1)

# ============================================================
# DEFINIR SKILLS
# ============================================================

@skill(description="Calcula la suma de dos números")
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b


@skill(description="Calcula la multiplicación de dos números")
def multiplicar(a: int, b: int) -> int:
    """Multiplica dos números enteros."""
    return a * b


# ============================================================
# CREAR AGENTE CON SKILLS
# ============================================================

agente = InstantNeo(
    provider="groq",
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-20b",
    role_setup="Eres un asistente matemático. Usa tus tools cuando sea necesario.",
    skills=[sumar, multiplicar]  # Pasar las funciones decoradas directamente
)

# ============================================================
# DEMOSTRACIÓN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("AGENTE INSTANTNEO - Con Skills")
    print("=" * 70)

    # Ejemplo 1: Multiplicación (ahora SÍ funciona correctamente)
    print("\n1️⃣ Agente con skill de multiplicación:")
    resultado1 = agente.run("¿Cuánto es 847 * 921?")
    print(f"Q: ¿Cuánto es 847 * 921?")
    print(f"A: {resultado1}")
    print(f"✅ Correcto: {847 * 921}")

    # Ejemplo 2: Suma
    print("\n2️⃣ Agente con skill de suma:")
    resultado2 = agente.run("Suma 45 y 67")
    print(f"Q: Suma 45 y 67")
    print(f"A: {resultado2}")
    print(f"✅ Correcto: {45 + 67}")

    print("\n" + "=" * 70)
    print("💡 ¿Cómo funciona internamente?")
    print("=" * 70)
    print("1. El agente recibe el prompt")
    print("2. El LLM decide llamar a una skill (ej: multiplicar(847, 921))")
    print("3. La función se ejecuta → retorna resultado")
    print("=" * 70)


    print("\n" + "=" * 70)
    print("🎯 Puntos clave:")
    print("  - El decorador @skill hace que una función sea 'visible' para el LLM")
    print("  - El LLM decide CUÁNDO y CÓMO usar cada skill")
    print("  - Las skills extienden las capacidades del agente")
    print("  - Puedes crear skills para: APIs, bases de datos, archivos, etc.")
    print("=" * 70)

    # ============================================================
    # EXPERIMENTACIÓN
    # ============================================================

    # # Crear una nueva skill


    # # Registrar la nueva skill en el agente existente
    # agente.register_skill(<nombre_de_la_nueva_skill>)
    
    # Probar la nueva skill
