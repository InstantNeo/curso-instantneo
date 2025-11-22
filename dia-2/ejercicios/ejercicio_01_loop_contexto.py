"""
EJERCICIO 01: Loop con Contexto - Detector de Fraude en Transacciones
=======================================================================

OBJETIVO:
---------
Construir un sistema que procesa transacciones bancarias una por una,
manteniendo contexto del historial para detectar patrones de fraude.

CONCEPTO CLAVE:
---------------
Un "loop con contexto" significa:
1. Procesar múltiples elementos uno por uno (en un loop)
2. Mantener información acumulativa entre iteraciones
3. Usar ese contexto acumulado para mejorar el análisis

CASO DE USO:
------------
Detector de fraude bancario que:
- Analiza transacciones en secuencia
- Mantiene historial de transacciones previas
- Usa el contexto del historial para identificar anomalías

CRITERIOS DE ÉXITO:
-------------------
✅ El agente analiza cada transacción usando el historial previo
✅ El contexto se acumula correctamente con cada iteración
✅ El agente detecta la transacción sospechosa (#4)
✅ El análisis mejora con más contexto disponible
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

# Lista de transacciones a analizar
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
    temperature=0.3,  # Baja temperatura para análisis consistente
    max_tokens=200
)

# ============================================================
# TODO 1: VARIABLE DE HISTORIAL
# ============================================================
# Crea una variable para almacenar el historial de transacciones
# Pista: Usa una lista o string que se vaya construyendo

# TODO: Crear variable historial_transacciones
historial_transacciones = None  # REEMPLAZAR


# ============================================================
# TODO 2: FUNCIÓN PARA AGREGAR TRANSACCIONES AL HISTORIAL
# ============================================================
# Crea una función que tome una transacción y la agregue al historial
# en formato legible

def agregar_transaccion(transaccion: dict) -> None:
    """
    Agrega una transacción al historial en formato legible.

    Args:
        transaccion: Diccionario con datos de la transacción
    """
    # TODO: Implementar función
    # Pistas:
    # - Formatear la transacción de forma legible
    # - Agregarla a la variable historial_transacciones
    # - Ejemplo de formato: "Transacción #1: €45.50 en Supermercado Local (Madrid) a las 10:30"
    pass


# ============================================================
# TODO 3: FUNCIÓN PARA CONSTRUIR EL PROMPT DE ANÁLISIS
# ============================================================
# Crea una función que construya el prompt incluyendo:
# - El historial de transacciones previas
# - La transacción actual a analizar

def construir_prompt_analisis(transaccion: dict, historial: str) -> str:
    """
    Construye el prompt para el agente incluyendo contexto del historial.

    Args:
        transaccion: Transacción actual a analizar
        historial: String con historial de transacciones previas

    Returns:
        Prompt completo para el agente
    """
    # TODO: Implementar función
    # Pistas:
    # - Incluir el historial (si existe)
    # - Incluir los detalles de la transacción actual
    # - Pedir análisis de riesgo

    prompt = ""  # REEMPLAZAR
    return prompt


# ============================================================
# TODO 4: LOOP DE PROCESAMIENTO
# ============================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🔍 SISTEMA DE DETECCIÓN DE FRAUDE - Loop con Contexto")
    print("=" * 80)

    # TODO: Implementar loop que:
    # 1. Itere sobre cada transacción
    # 2. Construya el prompt con el contexto del historial
    # 3. Llame al agente para analizar la transacción
    # 4. Muestre el resultado
    # 5. Agregue la transacción al historial para la próxima iteración

    # Pistas:
    # - Usar un for loop sobre la lista 'transacciones'
    # - Llamar a construir_prompt_analisis()
    # - Usar agente_fraude.run()
    # - Llamar a agregar_transaccion()
    # - Imprimir resultados de forma clara

    # TODO: Implementar loop aquí


    print("\n" + "=" * 80)
    print("✅ Análisis completado")
    print("=" * 80)

    # ============================================================
    # REFLEXIÓN
    # ============================================================
    print("\n💡 PREGUNTAS PARA REFLEXIONAR:")
    print("1. ¿El agente detectó la transacción sospechosa (#4)?")
    print("2. ¿Cómo cambió el análisis con más contexto disponible?")
    print("3. ¿Qué pasaría si procesamos las transacciones en orden aleatorio?")
    print("4. ¿Qué otras características podrías agregar al historial?")
