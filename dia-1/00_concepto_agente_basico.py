"""
Concepto: ¿Qué es un Agente? (Filosofía Minsky - Society of Mind)

Según Marvin Minsky:
- Un agente es algo simple que PERCIBE → DECIDE → ACTÚA
- NO necesita loops, memoria, ni chat
- Puede ser usado como componente en software normal (APIs, pipelines, etc.)
- La inteligencia emerge de COMBINAR agentes simples
"""

# ============================================================
# EJEMPLO: Agente Simple de Clasificación
# ============================================================

def agente_clasificador_sentimiento(texto: str) -> str:
    """
    Agente simple que clasifica sentimiento.

    - PERCIBE: Recibe el texto
    - DECIDE: Analiza palabras clave
    - ACTÚA: Retorna la clasificación

    Uso: Puede ser parte de un sistema de análisis de comentarios,
         moderación de contenido, dashboard de satisfacción, etc.
    """
    # PERCEPCIÓN
    texto_lower = texto.lower()

    # DECISIÓN
    palabras_positivas = ["bien", "genial", "excelente", "feliz", "amor"]
    palabras_negativas = ["mal", "terrible", "horrible", "triste", "odio"]

    score = 0
    for palabra in palabras_positivas:
        if palabra in texto_lower:
            score += 1

    for palabra in palabras_negativas:
        if palabra in texto_lower:
            score -= 1

    # ACCIÓN
    if score > 0:
        return "POSITIVO"
    elif score < 0:
        return "NEGATIVO"
    else:
        return "NEUTRAL"


# ============================================================
# DEMOSTRACIÓN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("AGENTE SIMPLE: Clasificador de Sentimiento")
    print("=" * 60)

    # Casos de prueba
    textos = [
        "Me siento muy feliz y genial hoy",
        "Esto es terrible y horrible",
        "El clima está normal"
    ]

    print("\nInput → Agente → Output:")
    for texto in textos:
        resultado = agente_clasificador_sentimiento(texto)
        print(f"  '{texto}'")
        print(f"  → {resultado}\n")

    print("=" * 60)
    print("💡 Puntos clave:")
    print("  - El agente es una función simple: Input → Output")
    print("  - Percibe, decide, actúa (sin loops ni memoria), pero no razona!")
    print("  - Puede ser usado en cualquier sistema")
    print("\n🔄 Con InstantNeo:")
    print("  - Usamos un LLM en lugar de lógica manual")
    print("  - El agente se vuelve mucho más potente")
    print("  - Veremos esto en el siguiente ejemplo")
    print("=" * 60)
