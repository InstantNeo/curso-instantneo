"""
EJERCICIO 03: SISTEMA MULTI-AGENTE CON JSON - SOLUCIÓN
======================================================

Sistema de triaje de tickets de soporte técnico usando 3 agentes que se comunican
mediante JSON estructurado.

CONCEPTOS CLAVE IMPLEMENTADOS:
1. Prompting para JSON confiable (explícito, sin ambigüedades)
2. Manejo robusto de errores de parseo
3. Encadenamiento de agentes con datos estructurados
4. Validación de campos JSON
"""

import os
import json
from dotenv import load_dotenv
from instantneo import InstantNeo

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar (configurable desde .env)

GROQ_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.3-70b-versatile")  # Default si no está en .env

print(f"🔧 Modelo configurado: {GROQ_MODEL}")


# ============================================================================
# AGENTE 1: CLASIFICADOR DE TICKETS
# ============================================================================

# CLAVE: Role setup extremadamente explícito para garantizar JSON válido
agente_clasificador = InstantNeo(
    provider="groq",
    model=GROQ_MODEL,
    role_setup="""Eres un clasificador de tickets de soporte técnico.

IMPORTANTE: Respondes ÚNICAMENTE con JSON válido, sin texto adicional antes o después.

Tu tarea es analizar tickets y retornar un JSON con esta estructura EXACTA:
{
    "categoria": "<categoria>",
    "urgencia": "<urgencia>",
    "palabras_clave": ["palabra1", "palabra2", "palabra3"]
}

CATEGORÍAS PERMITIDAS (elige UNA):
- "hardware": Problemas físicos (servidores, computadoras, impresoras, etc.)
- "software": Problemas de aplicaciones o sistemas operativos
- "red": Problemas de conectividad o infraestructura de red
- "cuenta": Problemas de acceso, contraseñas, permisos
- "otro": Cualquier cosa que no encaje en las anteriores

URGENCIAS PERMITIDAS (elige UNA):
- "critica": Operaciones completamente detenidas, pérdida de ingresos
- "alta": Funcionalidad importante afectada, workaround difícil
- "media": Funcionalidad afectada pero hay workaround razonable
- "baja": Inconveniente menor, no afecta trabajo crítico

PALABRAS CLAVE: Extrae 2-4 términos técnicos relevantes del ticket.

EJEMPLO DE RESPUESTA:
{
    "categoria": "hardware",
    "urgencia": "critica",
    "palabras_clave": ["servidor", "no enciende", "producción"]
}

NO AGREGUES explicaciones, comentarios o texto fuera del JSON."""
)


# ============================================================================
# AGENTE 2: ASIGNADOR DE EQUIPOS
# ============================================================================

agente_asignador = InstantNeo(
    provider="groq",
    model=GROQ_MODEL,
    role_setup="""Eres un asignador de tickets a equipos técnicos.

IMPORTANTE: Respondes ÚNICAMENTE con JSON válido, sin texto adicional.

Estructura EXACTA del JSON:
{
    "equipo": "<nombre_equipo>",
    "tiempo_estimado": "<estimación>",
    "requiere_escalamiento": <true/false>,
    "prioridad_cola": <1-5>
}

EQUIPOS DISPONIBLES:
- "Hardware": Problemas físicos de equipos
- "Software": Aplicaciones y sistemas operativos
- "Redes": Conectividad e infraestructura
- "Cuentas": Accesos y permisos
- "Escalamiento": Problemas críticos que requieren atención inmediata de nivel superior

TIEMPO ESTIMADO:
- Crítica: "2-4 horas" o "inmediato"
- Alta: "4-8 horas" o "1 día"
- Media: "1-2 días"
- Baja: "2-5 días"

REQUIERE ESCALAMIENTO:
- true: Si la urgencia es crítica O si el problema parece complejo
- false: Si puede manejarse con el equipo regular

PRIORIDAD EN COLA:
- 1: Crítica (atención inmediata)
- 2: Alta urgencia
- 3: Urgencia media
- 4: Baja urgencia
- 5: Tareas de mantenimiento/mejora

EJEMPLO:
{
    "equipo": "Hardware",
    "tiempo_estimado": "2-4 horas",
    "requiere_escalamiento": true,
    "prioridad_cola": 1
}

Recibirás información de clasificación y debes asignar apropiadamente."""
)


# ============================================================================
# AGENTE 3: GENERADOR DE RESPUESTAS
# ============================================================================

agente_respuesta = InstantNeo(
    provider="groq",
    model=GROQ_MODEL,
    role_setup="""Eres un agente de soporte al cliente que genera respuestas profesionales y empáticas.

Tu tarea es crear un mensaje para el cliente confirmando la recepción de su ticket.

El mensaje debe:
1. Agradecer por contactar soporte
2. Confirmar que recibimos su solicitud
3. Informar el equipo asignado
4. Dar un tiempo estimado de resolución
5. Ser profesional pero cercano y tranquilizador

TONO: Profesional, empático, confiable, sin ser demasiado formal.

NO uses frases genéricas vacías. SÉ específico con la información que recibes.

Genera un mensaje de 3-5 líneas."""
)


# ============================================================================
# FUNCIÓN DE PROCESAMIENTO
# ============================================================================

def procesar_ticket(descripcion_ticket: str) -> dict:
    """
    Procesa un ticket a través de los 3 agentes.

    Args:
        descripcion_ticket: Descripción del problema del cliente

    Returns:
        dict con toda la información del procesamiento
    """
    resultado = {
        "ticket_original": descripcion_ticket,
        "clasificacion": None,
        "asignacion": None,
        "respuesta_cliente": None,
        "errores": []
    }

    # ====================
    # PASO 1: CLASIFICAR
    # ====================
    try:
        respuesta_clasificador = agente_clasificador.run(
            user_says=f"Clasifica este ticket de soporte:\n\n{descripcion_ticket}"
        )

        # Intentar parsear el JSON
        # Algunos LLMs pueden agregar markdown (```json ... ```), lo limpiamos
        texto_limpio = respuesta_clasificador.strip()
        if texto_limpio.startswith("```json"):
            texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
        elif texto_limpio.startswith("```"):
            texto_limpio = texto_limpio.replace("```", "").strip()

        clasificacion = json.loads(texto_limpio)

        # Validación básica de campos requeridos
        campos_requeridos = ["categoria", "urgencia", "palabras_clave"]
        if not all(campo in clasificacion for campo in campos_requeridos):
            raise ValueError(f"Faltan campos en clasificación. Esperados: {campos_requeridos}")

        resultado["clasificacion"] = clasificacion

    except json.JSONDecodeError as e:
        resultado["errores"].append(f"Error parseando JSON del clasificador: {e}")
        resultado["errores"].append(f"Respuesta recibida: {respuesta_clasificador[:200]}...")
        return resultado
    except Exception as e:
        resultado["errores"].append(f"Error en clasificador: {e}")
        return resultado

    # ====================
    # PASO 2: ASIGNAR
    # ====================
    try:
        # Construir prompt con la info de clasificación
        prompt_asignador = f"""Asigna equipo y tiempo para este ticket:

Categoría: {clasificacion['categoria']}
Urgencia: {clasificacion['urgencia']}
Palabras clave: {', '.join(clasificacion['palabras_clave'])}

Ticket original: {descripcion_ticket}"""

        respuesta_asignador = agente_asignador.run(user_says=prompt_asignador)

        # Limpiar posibles marcadores de markdown
        texto_limpio = respuesta_asignador.strip()
        if texto_limpio.startswith("```json"):
            texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
        elif texto_limpio.startswith("```"):
            texto_limpio = texto_limpio.replace("```", "").strip()

        asignacion = json.loads(texto_limpio)

        # Validación
        campos_requeridos = ["equipo", "tiempo_estimado", "requiere_escalamiento", "prioridad_cola"]
        if not all(campo in asignacion for campo in campos_requeridos):
            raise ValueError(f"Faltan campos en asignación. Esperados: {campos_requeridos}")

        resultado["asignacion"] = asignacion

    except json.JSONDecodeError as e:
        resultado["errores"].append(f"Error parseando JSON del asignador: {e}")
        resultado["errores"].append(f"Respuesta recibida: {respuesta_asignador[:200]}...")
        return resultado
    except Exception as e:
        resultado["errores"].append(f"Error en asignador: {e}")
        return resultado

    # ====================
    # PASO 3: RESPUESTA
    # ====================
    try:
        prompt_respuesta = f"""Genera un mensaje para el cliente basado en esta información:

TICKET ORIGINAL:
{descripcion_ticket}

CLASIFICACIÓN:
- Categoría: {clasificacion['categoria']}
- Urgencia: {clasificacion['urgencia']}

ASIGNACIÓN:
- Equipo: {asignacion['equipo']}
- Tiempo estimado: {asignacion['tiempo_estimado']}
- Requiere escalamiento: {'Sí' if asignacion['requiere_escalamiento'] else 'No'}

Genera un mensaje profesional y empático para el cliente."""

        respuesta_cliente = agente_respuesta.run(user_says=prompt_respuesta)
        resultado["respuesta_cliente"] = respuesta_cliente.strip()

    except Exception as e:
        resultado["errores"].append(f"Error generando respuesta al cliente: {e}")
        return resultado

    return resultado


# ============================================================================
# TICKETS DE PRUEBA
# ============================================================================

tickets_prueba = [
    # Ticket 1: CRÍTICO - Hardware
    """El servidor principal de producción (SRV-PROD-01) no enciende.
    Intentamos reiniciarlo después del mantenimiento programado de esta madrugada
    y ahora no responde. Las luces del panel frontal están apagadas.
    TODAS nuestras operaciones comerciales están detenidas.
    Tenemos clientes esperando y perdiendo ventas cada minuto.""",

    # Ticket 2: MEDIA - Software
    """Desde que actualizamos a la última versión de Excel, la aplicación
    se cierra automáticamente cuando intento abrir archivos que superan los 50MB.
    He intentado reparar Office desde el Panel de Control sin éxito.
    Puedo trabajar con archivos pequeños, pero necesito los reportes grandes
    para la reunión del viernes. No es urgente urgente, pero sí necesito
    una solución esta semana.""",

    # Ticket 3: BAJA - Cuenta
    """Hola, olvidé mi contraseña del correo corporativo.
    Intenté recuperarla con las preguntas de seguridad pero no recuerdo las respuestas.
    Puedo acceder a todo lo demás (Slack, sistema interno) y estoy trabajando normalmente,
    pero me gustaría recuperar el acceso al email cuando tengan tiempo.
    No hay apuro, cuando puedan está bien.""",

    # Ticket 4: ALTA - Red
    """Toda la oficina del piso 3 perdió conexión a internet hace 2 horas.
    Son 45 personas que no pueden acceder a los sistemas en la nube.
    Hemos verificado que el router del piso tiene luces rojas intermitentes.
    Reiniciamos el equipo 3 veces sin resultados. Los otros pisos funcionan bien.
    La gente está usando datos móviles pero necesitamos esto resuelto pronto
    porque tenemos videollamadas con clientes esta tarde."""
]


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Procesar todos los tickets de prueba."""
    print("=" * 80)
    print(" " * 20 + "SISTEMA DE TRIAJE DE TICKETS")
    print(" " * 25 + "Multi-Agente con JSON")
    print("=" * 80)
    print()

    for i, ticket in enumerate(tickets_prueba, 1):
        print(f"\n{'='*80}")
        print(f"TICKET #{i}")
        print(f"{'='*80}")

        # Mostrar ticket original (truncado si es muy largo)
        ticket_preview = ticket.replace("\n", " ").strip()
        if len(ticket_preview) > 100:
            ticket_preview = ticket_preview[:100] + "..."
        print(f"\nDESCRIPCIÓN: {ticket_preview}")
        print()

        # Procesar
        resultado = procesar_ticket(ticket)

        # Verificar errores
        if resultado["errores"]:
            print("ERROR EN PROCESAMIENTO:")
            for error in resultado["errores"]:
                print(f"  - {error}")
            continue

        # Mostrar clasificación
        print("CLASIFICACIÓN:")
        print(json.dumps(resultado["clasificacion"], indent=2, ensure_ascii=False))
        print()

        # Mostrar asignación
        print("ASIGNACIÓN:")
        print(json.dumps(resultado["asignacion"], indent=2, ensure_ascii=False))
        print()

        # Mostrar respuesta al cliente
        print("RESPUESTA AL CLIENTE:")
        print("-" * 80)
        print(resultado["respuesta_cliente"])
        print("-" * 80)
        print()


if __name__ == "__main__":
    main()


# ============================================================================
# NOTAS DE IMPLEMENTACIÓN
# ============================================================================
"""
LECCIONES CLAVE:

1. PROMPTING PARA JSON CONFIABLE:
   - Ser EXPLÍCITO: "Respondes ÚNICAMENTE con JSON válido"
   - Mostrar la estructura EXACTA esperada
   - Listar TODAS las opciones válidas para cada campo
   - Dar ejemplos concretos
   - Prohibir texto adicional

2. MANEJO DE ERRORES:
   - LLMs pueden agregar markdown (```json ... ```) → limpiarlo
   - Validar campos obligatorios después del parseo
   - Usar try/except específicos para cada etapa
   - Mostrar información útil en los errores

3. ENCADENAMIENTO DE AGENTES:
   - Cada agente tiene una responsabilidad clara
   - Los datos fluyen estructuradamente (JSON)
   - El contexto se construye progresivamente
   - El último agente sintetiza todo en lenguaje natural

4. TRADE-OFFS:
   - JSON es más confiable que lenguaje natural para datos
   - Pero requiere prompts más largos y específicos
   - Vale la pena para sistemas que necesitan procesamiento posterior
   - Para respuestas finales al usuario, texto natural es mejor

5. MEJORAS POSIBLES:
   - Implementar retry automático si JSON falla
   - Agregar campos de "confianza" en las clasificaciones
   - Validar rangos de valores (ej: prioridad_cola debe ser 1-5)
   - Usar Pydantic para validación de esquemas más robusta
   - Loggear resultados para análisis de rendimiento del sistema
"""
