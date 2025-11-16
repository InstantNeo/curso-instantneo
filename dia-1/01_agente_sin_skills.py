"""
Primer Agente con InstantNeo (Sin Skills)

Objetivo:
- Entender la interfaz básica de InstantNeo
- Ver las capacidades y limitaciones de un LLM sin herramientas
- Experimentar con role_setup, temperature, y otros parámetros
"""

from instantneo import InstantNeo
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ============================================================
# CONFIGURACIÓN
# ============================================================

# API Key desde variable de entorno (NUNCA hardcodear)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ Error: No se encontró GROQ_API_KEY en .env")
    print("   Crea un archivo .env con: GROQ_API_KEY=tu-api-key")
    exit(1)

# ============================================================
# CREAR AGENTE SIMPLE (sin skills)
# ============================================================

agente = InstantNeo(
    provider="groq",
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-20b",
    role_setup="Eres un asistente amigable y conciso.",
    max_tokens=200
)

# ============================================================
# EXPERIMENTACIÓN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("AGENTE INSTANTNEO - Sin Skills")
    print("=" * 70)

    # Pregunta 1: Tarea simple de comprensión
    print("\n1️⃣ Tarea de comprensión:")
    respuesta1 = agente.run("¿Qué es un agente inteligente?")
    print(f"Q: ¿Qué es un agente inteligente?")
    print(f"A: {respuesta1}\n")

    # Pregunta 3: Información actualizada (fuera de knowledge cutoff)
    print("3️⃣ Limitación: Información actualizada")
    respuesta3 = agente.run("Que día y hora son ahora mismo?")
    print(f"Q: Que día y hora son ahora mismo?")
    print(f"A: {respuesta3}")
    print(f"❌ No puede acceder a información actualizada (sin web search)\n")

    print("=" * 70)
    print("\n💡 EXPERIMENTACIÓN SUGERIDA:")
    print("\nModifica el código y prueba:")
    print('1. Cambiar role_setup a: "Eres un pirata que habla en jerga marinera"')
    print("2. Cambiar temperature a 0.0 (más determinista) o 1.0 (más creativo)")
    print("3. Hacer preguntas que requieren herramientas externas")
    print("\n🔍 Observa:")
    print("- El agente SIN skills solo puede usar conocimiento del LLM")
    print("- Falla en cálculos, info actualizada, acceso a archivos, etc.")
    print("- En el siguiente ejemplo veremos cómo resolver esto con @skill")
    print("=" * 70)