"""
EJERCICIO 02: Pipeline Multi-Agente - Análisis de Logs de Sistema
===================================================================

OBJETIVO:
---------
Construir un pipeline de análisis de logs donde múltiples agentes especializados
trabajan en secuencia, cada uno transformando la salida del anterior.

CONCEPTO CLAVE:
---------------
Un "pipeline multi-agente" es una cadena de procesamiento donde:
1. Cada agente tiene una responsabilidad específica
2. La salida de un agente es la entrada del siguiente
3. El resultado final es la combinación de todas las etapas

ARQUITECTURA DEL PIPELINE:
--------------------------

    LOG BRUTO
       ↓
 [Agente 1: Extractor]
   → Extrae datos estructurados del log
       ↓
 [Agente 2: Clasificador]
   → Clasifica tipo y severidad
       ↓
 [Agente 3: Enriquecedor]
   → Agrega contexto y explicaciones
       ↓
 [Agente 4: Reportero]
   → Genera reporte ejecutivo
       ↓
    REPORTE FINAL

CRITERIOS DE ÉXITO:
-------------------
✅ Cada agente tiene un role_setup especializado
✅ Los datos fluyen correctamente entre etapas
✅ El resultado final es útil y bien estructurado
✅ Se pueden rastrear las transformaciones en cada etapa
"""

from instantneo import InstantNeo
import os
from dotenv import load_dotenv
import json

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
# DATOS DE PRUEBA - LOGS REALES DE SISTEMA
# ============================================================

logs_ejemplo = [
    "[2025-01-15 03:42:17] ERROR Database connection pool exhausted. Active: 100/100. Waiting: 47 queries. Timeout in 30s.",
    "[2025-01-15 10:23:45] WARNING Disk usage at 89% on /dev/sda1. Recommend cleanup or expansion.",
    "[2025-01-15 14:55:02] CRITICAL Authentication service down. Failed health checks: 15/15. Users cannot login.",
]

# ============================================================
# TODO 1: CREAR AGENTE EXTRACTOR
# ============================================================
# Crea un agente cuya responsabilidad es extraer información estructurada
# del log en formato JSON

# TODO: Crear agente_extractor
agente_extractor = None  # REEMPLAZAR

# Pistas para el role_setup:
# - Debe extraer: timestamp, nivel, componente, mensaje, datos_relevantes
# - Debe retornar JSON válido
# - Debe ser preciso y no agregar información que no está en el log


# ============================================================
# TODO 2: CREAR AGENTE CLASIFICADOR
# ============================================================
# Crea un agente que clasifica el tipo de problema y su severidad

# TODO: Crear agente_clasificador
agente_clasificador = None  # REEMPLAZAR

# Pistas para el role_setup:
# - Recibe JSON del extractor
# - Agrega campos: tipo_problema, severidad (1-5), categoria
# - Retorna JSON actualizado


# ============================================================
# TODO 3: CREAR AGENTE ENRIQUECEDOR
# ============================================================
# Crea un agente que agrega contexto y posibles causas/soluciones

# TODO: Crear agente_enriquecedor
agente_enriquecedor = None  # REEMPLAZAR

# Pistas para el role_setup:
# - Recibe JSON del clasificador
# - Agrega: posibles_causas, impacto, acciones_recomendadas
# - Usa su conocimiento del dominio de sistemas


# ============================================================
# TODO 4: CREAR AGENTE REPORTERO
# ============================================================
# Crea un agente que genera un reporte ejecutivo legible

# TODO: Crear agente_reportero
agente_reportero = None  # REEMPLAZAR

# Pistas para el role_setup:
# - Recibe JSON enriquecido
# - Genera reporte en lenguaje natural para no-técnicos
# - Debe ser conciso pero informativo


# ============================================================
# TODO 5: FUNCIÓN PIPELINE
# ============================================================
# Crea la función que ejecuta todo el pipeline

def procesar_log(log_bruto: str) -> dict:
    """
    Procesa un log a través del pipeline completo de 4 agentes.

    Args:
        log_bruto: String con el log original

    Returns:
        Diccionario con todos los resultados intermedios y finales
    """
    resultado = {
        "log_original": log_bruto,
        "etapa_1_extraccion": None,
        "etapa_2_clasificacion": None,
        "etapa_3_enriquecimiento": None,
        "etapa_4_reporte": None
    }

    # TODO: Implementar pipeline
    # Pistas:
    # 1. Pasar log_bruto al agente_extractor
    # 2. Pasar resultado al agente_clasificador
    # 3. Pasar resultado al agente_enriquecedor
    # 4. Pasar resultado al agente_reportero
    # 5. Guardar cada resultado intermedio en el diccionario

    return resultado


# ============================================================
# TODO 6: LOOP DE PROCESAMIENTO
# ============================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🔄 PIPELINE MULTI-AGENTE - Análisis de Logs")
    print("=" * 80)

    # TODO: Implementar loop que:
    # 1. Itere sobre logs_ejemplo
    # 2. Procese cada log con procesar_log()
    # 3. Muestre los resultados de cada etapa
    # 4. Visualice la transformación del dato

    # Pistas:
    # - Mostrar cada etapa del pipeline claramente
    # - Usar print() con formato para visualizar el flujo
    # - Separar visualmente cada log procesado


    print("\n" + "=" * 80)
    print("✅ Pipeline completado")
    print("=" * 80)

    # ============================================================
    # REFLEXIÓN
    # ============================================================
    print("\n💡 PREGUNTAS PARA REFLEXIONAR:")
    print("1. ¿Qué ventaja tiene separar el procesamiento en 4 agentes vs 1 solo?")
    print("2. ¿Qué etapa fue más crítica para el resultado final?")
    print("3. ¿Cómo manejarías errores en una etapa intermedia?")
    print("4. ¿Qué otros agentes podrías agregar al pipeline?")
    print("\n💡 EXTENSIONES POSIBLES:")
    print("- Agregar agente de validación entre etapas")
    print("- Implementar reintentos si una etapa falla")
    print("- Paralelizar logs independientes")
    print("- Agregar agente de priorización al final")
