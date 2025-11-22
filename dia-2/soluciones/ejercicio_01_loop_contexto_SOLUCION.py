"""
SOLUCIÓN EJERCICIO 01: Loop con Contexto - Detector de Fraude en Transacciones
===============================================================================

Esta solución demuestra cómo:
1. Mantener contexto acumulativo en un loop
2. Usar ese contexto para mejorar el análisis
3. Detectar patrones y anomalías con información histórica
"""

from instantneo import InstantNeo
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar (configurable desde .env)

GROQ_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.3-70b-versatile")  # Default si no está en .env

print(f"🔧 Modelo configurado: {GROQ_MODEL}")

# ============================================================
# CONFIGURACIÓN
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ Error: No se encontró GROQ_API_KEY en .env")
    exit(1)

# ============================================================
# DATOS DE PRUEBA
# ============================================================

transacciones = [
    {"id": 1, "monto": 45.50, "comercio": "Supermercado Local", "ubicacion": "Madrid", "hora": "10:30"},
    {"id": 2, "monto": 120.00, "comercio": "Gasolinera Shell", "ubicacion": "Madrid", "hora": "14:15"},
    {"id": 3, "monto": 35.20, "comercio": "Farmacia Cruz Verde", "ubicacion": "Madrid", "hora": "18:45"},
    {"id": 4, "monto": 2500.00, "comercio": "Electronics Store", "ubicacion": "Bangkok", "hora": "19:00"},  # ¡SOSPECHOSA!
    {"id": 5, "monto": 15.80, "comercio": "Cafetería Starbucks", "ubicacion": "Madrid", "hora": "20:30"},
    {"id": 6, "monto": 89.99, "comercio": "Restaurante Italiano", "ubicacion": "Madrid", "hora": "21:00"},
]

# ============================================================
# AGENTE CONFIGURADO
# ============================================================

agente_fraude = InstantNeo(
    provider="groq",
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    role_setup="""Eres un sistema experto en detección de fraude bancario.

Tu tarea es analizar cada transacción considerando:
1. El historial de transacciones previas del usuario
2. Patrones de comportamiento normales vs anómalos
3. Cambios geográficos repentinos
4. Montos inusuales comparados con el historial

Para cada transacción, proporciona:
- Nivel de riesgo: BAJO, MEDIO, ALTO
- Razón: Explicación breve del análisis
- Alerta: Si hay algo que requiere atención

Sé conciso pero preciso en tu análisis.""",
    temperature=0.3,
    max_tokens=200
)

# ============================================================
# SOLUCIÓN 1: VARIABLE DE HISTORIAL
# ============================================================
# Usamos una lista de strings para mantener el historial legible
historial_transacciones = []


# ============================================================
# SOLUCIÓN 2: FUNCIÓN PARA AGREGAR TRANSACCIONES
# ============================================================
def agregar_transaccion(transaccion: dict) -> None:
    """
    Agrega una transacción al historial en formato legible.

    Args:
        transaccion: Diccionario con datos de la transacción
    """
    # Formatear la transacción de forma legible y clara
    entrada = (
        f"Transacción #{transaccion['id']}: "
        f"€{transaccion['monto']} en {transaccion['comercio']} "
        f"({transaccion['ubicacion']}) a las {transaccion['hora']}"
    )
    historial_transacciones.append(entrada)


# ============================================================
# SOLUCIÓN 3: FUNCIÓN PARA CONSTRUIR EL PROMPT
# ============================================================
def construir_prompt_analisis(transaccion: dict, historial: list) -> str:
    """
    Construye el prompt para el agente incluyendo contexto del historial.

    Args:
        transaccion: Transacción actual a analizar
        historial: Lista con historial de transacciones previas

    Returns:
        Prompt completo para el agente
    """
    prompt = "ANÁLISIS DE TRANSACCIÓN\n\n"

    # Incluir historial si existe
    if historial:
        prompt += "HISTORIAL DE TRANSACCIONES PREVIAS:\n"
        for entrada in historial:
            prompt += f"- {entrada}\n"
        prompt += "\n"
    else:
        prompt += "HISTORIAL: Esta es la primera transacción.\n\n"

    # Incluir transacción actual
    prompt += "TRANSACCIÓN ACTUAL A ANALIZAR:\n"
    prompt += f"- ID: {transaccion['id']}\n"
    prompt += f"- Monto: €{transaccion['monto']}\n"
    prompt += f"- Comercio: {transaccion['comercio']}\n"
    prompt += f"- Ubicación: {transaccion['ubicacion']}\n"
    prompt += f"- Hora: {transaccion['hora']}\n\n"

    prompt += "Proporciona tu análisis de riesgo."

    return prompt


# ============================================================
# SOLUCIÓN 4: LOOP DE PROCESAMIENTO
# ============================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🔍 SISTEMA DE DETECCIÓN DE FRAUDE - Loop con Contexto")
    print("=" * 80)

    # Procesar cada transacción manteniendo contexto
    for transaccion in transacciones:
        print(f"\n{'─' * 80}")
        print(f"📊 Analizando Transacción #{transaccion['id']}")
        print(f"{'─' * 80}")

        # Construir prompt con el contexto acumulado hasta ahora
        prompt = construir_prompt_analisis(transaccion, historial_transacciones)

        # Mostrar cuánto contexto tenemos
        print(f"📚 Contexto disponible: {len(historial_transacciones)} transacción(es) previa(s)")

        # Analizar la transacción con el agente
        print(f"🤖 Analizando...\n")
        analisis = agente_fraude.run(prompt)

        # Mostrar resultado
        print(f"💬 ANÁLISIS:")
        print(f"{analisis}")

        # Agregar esta transacción al historial para las próximas iteraciones
        agregar_transaccion(transaccion)

        # Pausa visual entre transacciones
        print()

    print("\n" + "=" * 80)
    print("✅ Análisis completado")
    print("=" * 80)

    # Mostrar resumen del historial final
    print(f"\n📚 HISTORIAL FINAL ({len(historial_transacciones)} transacciones):")
    for entrada in historial_transacciones:
        print(f"  • {entrada}")

    # ============================================================
    # EXPLICACIÓN DE LA SOLUCIÓN
    # ============================================================
    print("\n" + "=" * 80)
    print("💡 PUNTOS CLAVE DE ESTA SOLUCIÓN:")
    print("=" * 80)
    print("""
1. CONTEXTO ACUMULATIVO:
   - historial_transacciones se construye iteración por iteración
   - Cada análisis tiene más información que el anterior

2. MEJOR DETECCIÓN CON MÁS CONTEXTO:
   - Transacción #1: Sin contexto previo
   - Transacción #4: Con 3 transacciones previas para comparar
   - El patrón de Madrid hace que Bangkok destaque como anómalo

3. ORDEN IMPORTA:
   - El análisis secuencial permite detectar cambios bruscos
   - La transacción #4 es claramente anómala vs el patrón establecido

4. APLICACIONES REALES:
   - Detección de fraude bancario
   - Análisis de logs secuenciales
   - Monitoreo de comportamiento de usuarios
   - Detección de intrusiones en seguridad

5. EXTENSIONES POSIBLES:
   - Agregar timestamp de análisis
   - Calcular estadísticas (monto promedio, ubicación más común)
   - Implementar ventanas deslizantes (solo últimas N transacciones)
   - Agregar skills para consultar bases de datos de fraude conocido
    """)
