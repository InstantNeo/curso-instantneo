"""
SOLUCIÓN EJERCICIO 02: Pipeline Multi-Agente - Análisis de Logs de Sistema
===========================================================================

Esta solución demuestra cómo:
1. Crear agentes especializados con roles específicos
2. Encadenar agentes en un pipeline de procesamiento
3. Transformar datos progresivamente a través de múltiples etapas
4. Mantener trazabilidad de las transformaciones
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
# DATOS DE PRUEBA
# ============================================================

logs_ejemplo = [
    "[2025-01-15 03:42:17] ERROR Database connection pool exhausted. Active: 100/100. Waiting: 47 queries. Timeout in 30s.",
    "[2025-01-15 10:23:45] WARNING Disk usage at 89% on /dev/sda1. Recommend cleanup or expansion.",
    "[2025-01-15 14:55:02] CRITICAL Authentication service down. Failed health checks: 15/15. Users cannot login.",
]

# ============================================================
# SOLUCIÓN 1: AGENTE EXTRACTOR
# ============================================================
# Especializado en extraer información estructurada de logs

agente_extractor = InstantNeo(
    provider="groq",
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    role_setup="""Eres un experto en parsing de logs de sistema.

Tu ÚNICA tarea es extraer información estructurada del log en formato JSON.

Debes extraer exactamente estos campos:
- timestamp: La fecha y hora del log
- nivel: El nivel de log (ERROR, WARNING, INFO, CRITICAL, etc.)
- componente: El componente del sistema afectado (database, disk, auth, etc.)
- mensaje: El mensaje principal sin el timestamp y nivel
- datos_numericos: Cualquier número relevante del log (como porcentajes, contadores)

Retorna SOLO JSON válido, sin texto adicional.
Sé preciso y no inventes información que no está en el log.""",
    temperature=0.1,  # Muy baja para extracción precisa
    max_tokens=300
)


# ============================================================
# SOLUCIÓN 2: AGENTE CLASIFICADOR
# ============================================================
# Especializado en clasificar tipo y severidad del problema

agente_clasificador = InstantNeo(
    provider="groq",
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    role_setup="""Eres un experto en clasificación de incidentes de sistemas.

Recibes un JSON con información extraída de un log.

Tu tarea es agregar estos campos de clasificación:
- tipo_problema: Categoría del problema (ej: "Recursos Agotados", "Capacidad", "Servicio Caído")
- severidad: Número del 1-5 donde:
  * 1 = Informativo
  * 2 = Advertencia menor
  * 3 = Advertencia importante
  * 4 = Error crítico
  * 5 = Emergencia (servicio caído)
- categoria: Área del sistema (Infraestructura, Aplicación, Seguridad, Red)
- requiere_accion_inmediata: true/false

Retorna el JSON completo (original + tus campos agregados).
Retorna SOLO JSON válido, sin texto adicional.""",
    temperature=0.2,
    max_tokens=400
)


# ============================================================
# SOLUCIÓN 3: AGENTE ENRIQUECEDOR
# ============================================================
# Especializado en agregar contexto y recomendaciones

agente_enriquecedor = InstantNeo(
    provider="groq",
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    role_setup="""Eres un SRE (Site Reliability Engineer) experto.

Recibes un JSON con información de un log ya clasificado.

Tu tarea es enriquecer con:
- posibles_causas: Array de 2-3 causas probables del problema
- impacto_estimado: Descripción breve del impacto en usuarios/sistema
- acciones_recomendadas: Array de 2-3 acciones concretas a tomar
- urgencia: "inmediata", "alta", "media", "baja"

Usa tu conocimiento de sistemas distribuidos, bases de datos, y DevOps.

Retorna el JSON completo (todo lo anterior + tus campos).
Retorna SOLO JSON válido, sin texto adicional.""",
    temperature=0.4,  # Un poco más de creatividad para recomendaciones
    max_tokens=500
)


# ============================================================
# SOLUCIÓN 4: AGENTE REPORTERO
# ============================================================
# Especializado en generar reportes ejecutivos legibles

agente_reportero = InstantNeo(
    provider="groq",
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    role_setup="""Eres un comunicador técnico experto.

Recibes un JSON completo con análisis técnico de un incidente.

Tu tarea es generar un REPORTE EJECUTIVO en lenguaje natural para stakeholders no-técnicos.

El reporte debe incluir:
1. Resumen del problema en 1 frase simple
2. Nivel de urgencia y por qué
3. Impacto en el negocio/usuarios
4. Qué acciones se deben tomar

Usa lenguaje claro, evita jerga técnica excesiva.
Sé conciso (máximo 4-5 líneas) pero informativo.

Retorna SOLO el texto del reporte, sin JSON.""",
    temperature=0.5,  # Más creatividad para redacción
    max_tokens=300
)


# ============================================================
# SOLUCIÓN 5: FUNCIÓN PIPELINE
# ============================================================

def procesar_log(log_bruto: str) -> dict:
    """
    Procesa un log a través del pipeline completo de 4 agentes.

    Args:
        log_bruto: String con el log original

    Returns:
        Diccionario con todos los resultados intermedios y finales
    """
    print(f"  🔍 Iniciando pipeline...")

    resultado = {
        "log_original": log_bruto,
        "etapa_1_extraccion": None,
        "etapa_2_clasificacion": None,
        "etapa_3_enriquecimiento": None,
        "etapa_4_reporte": None
    }

    try:
        # ETAPA 1: Extracción
        print(f"  ⚙️  Etapa 1/4: Extrayendo información estructurada...")
        extraccion = agente_extractor.run(f"Extrae información de este log:\n{log_bruto}")
        resultado["etapa_1_extraccion"] = extraccion

        # ETAPA 2: Clasificación
        print(f"  ⚙️  Etapa 2/4: Clasificando problema...")
        clasificacion = agente_clasificador.run(f"Clasifica este log:\n{extraccion}")
        resultado["etapa_2_clasificacion"] = clasificacion

        # ETAPA 3: Enriquecimiento
        print(f"  ⚙️  Etapa 3/4: Enriqueciendo con contexto...")
        enriquecimiento = agente_enriquecedor.run(f"Enriquece este análisis:\n{clasificacion}")
        resultado["etapa_3_enriquecimiento"] = enriquecimiento

        # ETAPA 4: Reporte
        print(f"  ⚙️  Etapa 4/4: Generando reporte ejecutivo...")
        reporte = agente_reportero.run(f"Genera reporte ejecutivo de:\n{enriquecimiento}")
        resultado["etapa_4_reporte"] = reporte

        print(f"  ✅ Pipeline completado exitosamente")

    except Exception as e:
        print(f"  ❌ Error en pipeline: {str(e)}")
        resultado["error"] = str(e)

    return resultado


# ============================================================
# SOLUCIÓN 6: LOOP DE PROCESAMIENTO
# ============================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🔄 PIPELINE MULTI-AGENTE - Análisis de Logs")
    print("=" * 80)

    resultados_completos = []

    # Procesar cada log a través del pipeline completo
    for idx, log in enumerate(logs_ejemplo, 1):
        print(f"\n{'═' * 80}")
        print(f"📋 LOG #{idx}")
        print(f"{'═' * 80}")
        print(f"Original: {log}")
        print()

        # Ejecutar pipeline completo
        resultado = procesar_log(log)
        resultados_completos.append(resultado)

        # Mostrar transformaciones
        print(f"\n{'─' * 80}")
        print(f"📊 RESULTADOS DEL PIPELINE:")
        print(f"{'─' * 80}")

        if resultado.get("etapa_4_reporte"):
            print(f"\n📄 REPORTE EJECUTIVO:")
            print(f"{resultado['etapa_4_reporte']}")

            # Mostrar etapas intermedias colapsadas
            print(f"\n🔍 Detalles técnicos (etapas intermedias):")
            print(f"  Etapa 1 - Extracción: {len(resultado['etapa_1_extraccion'])} caracteres")
            print(f"  Etapa 2 - Clasificación: {len(resultado['etapa_2_clasificacion'])} caracteres")
            print(f"  Etapa 3 - Enriquecimiento: {len(resultado['etapa_3_enriquecimiento'])} caracteres")

        print()

    print("\n" + "=" * 80)
    print(f"✅ Procesados {len(resultados_completos)} logs exitosamente")
    print("=" * 80)

    # ============================================================
    # EXPLICACIÓN DE LA SOLUCIÓN
    # ============================================================
    print("\n" + "=" * 80)
    print("💡 PUNTOS CLAVE DE ESTA SOLUCIÓN:")
    print("=" * 80)
    print("""
1. ESPECIALIZACIÓN DE AGENTES:
   - Cada agente tiene UNA responsabilidad clara
   - role_setup específico para su tarea
   - Temperature ajustada según el tipo de trabajo:
     * Extracción: 0.1 (máxima precisión)
     * Clasificación: 0.2 (determinista)
     * Enriquecimiento: 0.4 (algo de creatividad)
     * Reporte: 0.5 (creatividad en redacción)

2. TRANSFORMACIÓN PROGRESIVA:
   - Log bruto → JSON estructurado → JSON clasificado → JSON enriquecido → Reporte
   - Cada etapa agrega valor sin perder información previa

3. VENTAJAS DEL PIPELINE:
   ✅ Modularidad: Fácil agregar/quitar/modificar etapas
   ✅ Testeable: Puedes probar cada agente independientemente
   ✅ Reusable: Los agentes pueden usarse en otros pipelines
   ✅ Debuggeable: Ves exactamente dónde falla si hay error
   ✅ Mantenible: Cambios en una etapa no afectan a otras

4. TRAZABILIDAD:
   - Guardamos el resultado de cada etapa
   - Podemos auditar todo el proceso de transformación
   - Útil para debugging y mejora continua

5. APLICACIONES REALES:
   - Análisis de logs de producción
   - Pipeline de procesamiento de documentos
   - Análisis de feedback de usuarios (extrae → clasifica → resume)
   - Pipeline de ETL (Extract, Transform, Load)
   - Sistemas de monitoreo y alertas

6. COMPARACIÓN: 4 AGENTES vs 1 AGENTE

   Pipeline de 4 agentes:
   ✅ Cada uno es experto en su área
   ✅ Fácil debuggear problemas
   ✅ Puedes mejorar etapas individuales
   ✅ Reutilizar agentes en otros contextos
   ❌ Más latencia (4 llamadas al LLM)
   ❌ Más costo (4 llamadas)

   1 agente único:
   ✅ Más rápido (1 llamada)
   ✅ Menos costo
   ❌ Prompt más complejo
   ❌ Difícil debuggear
   ❌ Más difícil mantener/mejorar

7. EXTENSIONES POSIBLES:
   - Agregar agente validador entre etapas
   - Implementar reintentos con backoff exponencial
   - Paralelizar procesamiento de múltiples logs
   - Agregar agente de priorización/triaje
   - Guardar resultados en base de datos
   - Crear dashboard de visualización
   - Implementar alertas automáticas para severidad 5
    """)

    # ============================================================
    # EJERCICIO ADICIONAL
    # ============================================================
    print("\n" + "=" * 80)
    print("🎯 EJERCICIO PARA PRACTICAR:")
    print("=" * 80)
    print("""
Intenta agregar un 5to agente al pipeline:

AGENTE PRIORIZADOR:
- Recibe el reporte final
- Asigna prioridad en cola de trabajo: P0, P1, P2, P3
- Estima tiempo de resolución
- Sugiere equipo responsable (DB team, DevOps, Security, etc.)

Pista: Insértalo entre el agente_enriquecedor y agente_reportero,
o después del reportero como etapa final.
    """)
