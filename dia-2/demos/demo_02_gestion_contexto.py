"""
Demo 02: Gestión de Contexto - Memoria entre Llamadas
=====================================================

Conceptos clave:
- Diferencia entre llamadas sin historial vs con historial
- Cómo el agente "olvida" sin gestión de contexto
- Implementación manual de historial de conversación
- Funciones helper para gestionar contexto
- Comparación lado a lado de ambos enfoques

Autor: Curso InstantNeo - Día 2
"""

import os
from dotenv import load_dotenv
from instantneo import InstantNeo

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar en demos (configurable desde .env)
# Usa un modelo más liviano para demos rápidas
LLAMA_8B_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.1-8b-instant")  # Default: modelo rápido

print(f"🔧 Modelo configurado: {LLAMA_8B_MODEL}")


def separador(titulo):
    """Imprime un separador visual con título."""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def agregar_al_historial(historial, rol, contenido):
    """
    Helper function: Agrega un mensaje al historial.

    Args:
        historial (list): Lista de mensajes del historial
        rol (str): 'user' o 'assistant'
        contenido (str): Contenido del mensaje

    Returns:
        list: Historial actualizado
    """
    historial.append({
        "rol": rol,
        "contenido": contenido
    })
    return historial


def construir_prompt_con_contexto(historial, nuevo_mensaje):
    """
    Helper function: Construye un prompt que incluye el historial completo.

    Args:
        historial (list): Lista de mensajes del historial
        nuevo_mensaje (str): Nuevo mensaje del usuario

    Returns:
        str: Prompt formateado con todo el contexto
    """
    # Construir el prompt con todo el historial
    contexto_completo = "Conversación anterior:\n\n"

    for mensaje in historial:
        if mensaje["rol"] == "user":
            contexto_completo += f"Usuario: {mensaje['contenido']}\n"
        else:
            contexto_completo += f"Asistente: {mensaje['contenido']}\n"

    contexto_completo += f"\nUsuario: {nuevo_mensaje}\nAsistente:"

    return contexto_completo


def escenario_sin_historial():
    """ESCENARIO A: Interacciones SIN historial - El agente olvida"""
    separador("ESCENARIO A: SIN Gestión de Historial")

    print("🔴 En este escenario, cada llamada es independiente.")
    print("   El agente NO recuerda información previa.\n")

    # Crear agente
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un asistente amigable que recuerda lo que te dicen.",
        max_tokens=150
    )

    # Interacción 1: Decir el nombre
    print("Interacción 1:")
    mensaje1 = "Me llamo Juan"
    print(f"  👤 Usuario: {mensaje1}")

    respuesta1 = agente.run(prompt=mensaje1)
    print(f"  🤖 Agente: {respuesta1}\n")

    # Interacción 2: Decir la edad
    print("Interacción 2:")
    mensaje2 = "Tengo 30 años"
    print(f"  👤 Usuario: {mensaje2}")

    respuesta2 = agente.run(prompt=mensaje2)
    print(f"  🤖 Agente: {respuesta2}\n")

    # Interacción 3: Preguntar por información previa
    print("Interacción 3:")
    mensaje3 = "¿Cómo me llamo y cuántos años tengo?"
    print(f"  👤 Usuario: {mensaje3}")

    respuesta3 = agente.run(prompt=mensaje3)
    print(f"  🤖 Agente: {respuesta3}\n")

    print("⚠️  RESULTADO: El agente NO puede responder correctamente")
    print("    porque no tiene acceso al historial de la conversación.\n")


def escenario_con_historial():
    """ESCENARIO B: Mismas interacciones CON historial - El agente recuerda"""
    separador("ESCENARIO B: CON Gestión de Historial")

    print("🟢 En este escenario, mantenemos un historial manual.")
    print("   Incluimos todo el contexto en cada llamada.\n")

    # Crear agente
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un asistente amigable que recuerda lo que te dicen.",
        max_tokens=150
    )

    # Inicializar historial vacío
    historial = []

    # Interacción 1: Decir el nombre
    print("Interacción 1:")
    mensaje1 = "Me llamo Juan"
    print(f"  👤 Usuario: {mensaje1}")

    # Construir prompt con contexto (primera vez, historial vacío)
    prompt1 = construir_prompt_con_contexto(historial, mensaje1)
    respuesta1 = agente.run(prompt=prompt1)
    print(f"  🤖 Agente: {respuesta1}")

    # Agregar al historial
    historial = agregar_al_historial(historial, "user", mensaje1)
    historial = agregar_al_historial(historial, "assistant", respuesta1)
    print(f"  📝 Historial actualizado: {len(historial)} mensajes\n")

    # Interacción 2: Decir la edad
    print("Interacción 2:")
    mensaje2 = "Tengo 30 años"
    print(f"  👤 Usuario: {mensaje2}")

    # Construir prompt con todo el contexto previo
    prompt2 = construir_prompt_con_contexto(historial, mensaje2)
    respuesta2 = agente.run(prompt=prompt2)
    print(f"  🤖 Agente: {respuesta2}")

    # Agregar al historial
    historial = agregar_al_historial(historial, "user", mensaje2)
    historial = agregar_al_historial(historial, "assistant", respuesta2)
    print(f"  📝 Historial actualizado: {len(historial)} mensajes\n")

    # Interacción 3: Preguntar por información previa
    print("Interacción 3:")
    mensaje3 = "¿Cómo me llamo y cuántos años tengo?"
    print(f"  👤 Usuario: {mensaje3}")

    # Construir prompt con TODO el contexto
    prompt3 = construir_prompt_con_contexto(historial, mensaje3)
    respuesta3 = agente.run(prompt=prompt3)
    print(f"  🤖 Agente: {respuesta3}")

    # Agregar al historial
    historial = agregar_al_historial(historial, "user", mensaje3)
    historial = agregar_al_historial(historial, "assistant", respuesta3)
    print(f"  📝 Historial final: {len(historial)} mensajes\n")

    print("✅ RESULTADO: El agente responde correctamente porque")
    print("   cada prompt incluye todo el historial previo.\n")

    # Mostrar el historial completo
    print("Historial completo de la conversación:")
    print("-" * 70)
    for i, mensaje in enumerate(historial, 1):
        rol = "Usuario" if mensaje["rol"] == "user" else "Agente"
        print(f"{i}. {rol}: {mensaje['contenido']}")
    print("-" * 70)


def ejemplo_tecnico_prompt_contexto():
    """Muestra cómo se ve un prompt con contexto"""
    separador("EJEMPLO: Construcción de Prompt con Contexto")

    # Simular un historial
    historial = [
        {"rol": "user", "contenido": "Me llamo Juan"},
        {"rol": "assistant", "contenido": "¡Hola Juan! Encantado de conocerte."},
        {"rol": "user", "contenido": "Tengo 30 años"},
        {"rol": "assistant", "contenido": "Entendido, Juan. Tienes 30 años."}
    ]

    nuevo_mensaje = "¿Cómo me llamo y cuántos años tengo?"

    print("Historial actual:")
    for msg in historial:
        rol = "Usuario" if msg["rol"] == "user" else "Agente"
        print(f"  {rol}: {msg['contenido']}")

    print(f"\nNuevo mensaje del usuario:")
    print(f"  {nuevo_mensaje}")

    print("\nPrompt COMPLETO enviado al LLM:")
    print("-" * 70)
    prompt_completo = construir_prompt_con_contexto(historial, nuevo_mensaje)
    print(prompt_completo)
    print("-" * 70)

    print("\n💡 LECCIÓN: El prompt incluye toda la conversación,")
    print("   permitiendo al LLM 'recordar' el contexto completo.")


def comparacion_lado_a_lado():
    """Comparación visual de ambos enfoques"""
    separador("COMPARACIÓN: Sin Historial vs Con Historial")

    print("┌─────────────────────────────────┬─────────────────────────────────┐")
    print("│     SIN GESTIÓN DE HISTORIAL    │     CON GESTIÓN DE HISTORIAL    │")
    print("├─────────────────────────────────┼─────────────────────────────────┤")
    print("│ ❌ Cada llamada es independiente│ ✅ Mantiene contexto completo    │")
    print("│ ❌ No recuerda conversaciones   │ ✅ Recuerda toda la conversación│")
    print("│ ❌ Prompt simple sin contexto   │ ✅ Prompt incluye historial     │")
    print("│ ✅ Más simple de implementar    │ ⚠️  Requiere gestión manual     │")
    print("│ ✅ Menos tokens consumidos      │ ⚠️  Más tokens por prompt       │")
    print("│ ❌ No apto para chatbots        │ ✅ Ideal para conversaciones    │")
    print("└─────────────────────────────────┴─────────────────────────────────┘")

    print("\nCUÁNDO USAR CADA ENFOQUE:")
    print("\n  SIN HISTORIAL:")
    print("    • Tareas independientes")
    print("    • Procesamiento de datos en lote")
    print("    • Análisis de documentos únicos")
    print("    • Cuando el agente no necesita más contexto para resolver la tarea")

    print("\n  CON HISTORIAL:")
    print("    • Chatbots y asistentes conversacionales")
    print("    • Sesiones interactivas con usuario")
    print("    • Cuando se necesita continuidad")
    print("    • Respuestas que dependen de info previa")


if __name__ == "__main__":
    print("\n" + "#"*70)
    print("  DEMO 02: Gestión de Contexto - Memoria entre Llamadas")
    print("#"*70)

    # Verificar API key
    if not os.getenv("GROQ_API_KEY"):
        print("\n⚠️  ERROR: GROQ_API_KEY no encontrada en .env")
        print("    Por favor, configura tu API key en el archivo .env")
        exit(1)

    # Ejecutar demos
    escenario_sin_historial()
    escenario_con_historial()
    ejemplo_tecnico_prompt_contexto()
    comparacion_lado_a_lado()

    print("\n" + "#"*70)
    print("  FIN DEL DEMO 02")
    print("#"*70 + "\n")
