"""
EJERCICIO 03: SISTEMA MULTI-AGENTE CON JSON
===========================================

Sistema de triaje de tickets de soporte técnico usando 3 agentes que se comunican
mediante JSON estructurado.

FLUJO:
1. Agente Clasificador: Analiza el ticket y retorna JSON con categoría, urgencia y palabras clave
2. Agente Asignador: Usa la clasificación para asignar equipo y estimar tiempo (retorna JSON)
3. Agente Respuesta: Genera mensaje natural para el cliente basado en la asignación

OBJETIVO: Aprender a:
- Diseñar prompts que retornen JSON confiable
- Parsear y validar respuestas JSON
- Manejar errores de formato
- Encadenar múltiples agentes con datos estructurados
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
# ESTRUCTURAS JSON ESPERADAS (para referencia)
# ============================================================================

"""
FORMATO JSON DEL CLASIFICADOR:
{
    "categoria": "hardware" | "software" | "red" | "cuenta" | "otro",
    "urgencia": "critica" | "alta" | "media" | "baja",
    "palabras_clave": ["keyword1", "keyword2", "..."]
}

FORMATO JSON DEL ASIGNADOR:
{
    "equipo": "nombre del equipo técnico",
    "tiempo_estimado": "estimación en horas/días",
    "requiere_escalamiento": true | false,
    "prioridad_cola": 1-5
}
"""


# ============================================================================
# TODO 1: CREAR AGENTE CLASIFICADOR
# ============================================================================
# INSTRUCCIONES:
# - Crear un InstantNeo con provider="groq"
# - Configurar role_setup para que SOLO retorne JSON válido (sin texto adicional)
# - El role_setup debe instruir sobre las categorías y niveles de urgencia permitidos
# - Usar modelo "llama-3.3-70b-versatile"
#
# TIPS PARA role_setup:
# - Ser EXPLÍCITO: "Respondes ÚNICAMENTE con JSON válido, sin comentarios ni texto adicional"
# - Listar las opciones válidas para cada campo
# - Dar ejemplos del formato exacto esperado

agente_clasificador = None  # TODO: Implementar


# ============================================================================
# TODO 2: CREAR AGENTE ASIGNADOR
# ============================================================================
# INSTRUCCIONES:
# - Similar al clasificador, debe retornar SOLO JSON
# - Debe conocer los equipos disponibles: "Hardware", "Software", "Redes", "Cuentas", "Escalamiento"
# - Debe poder estimar tiempos basándose en la urgencia
# - La prioridad_cola va de 1 (máxima) a 5 (mínima)

agente_asignador = None  # TODO: Implementar


# ============================================================================
# TODO 3: CREAR AGENTE RESPUESTA
# ============================================================================
# INSTRUCCIONES:
# - Este agente SÍ retorna texto natural (no JSON)
# - Debe generar un mensaje profesional y empático para el cliente
# - Debe incluir: confirmación de recepción, equipo asignado y tiempo estimado
# - Tono: profesional pero cercano

agente_respuesta = None  # TODO: Implementar


# ============================================================================
# TODO 4: FUNCIÓN DE PROCESAMIENTO DE TICKET
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

    # TODO 4.1: Ejecutar agente clasificador
    # - Usar agente_clasificador.run() con el ticket
    # - Parsear el JSON con json.loads()
    # - Manejar excepciones (JSONDecodeError)
    # - Guardar en resultado["clasificacion"]

    try:
        pass  # TODO: Implementar
    except json.JSONDecodeError as e:
        resultado["errores"].append(f"Error parseando clasificación: {e}")
        return resultado
    except Exception as e:
        resultado["errores"].append(f"Error en clasificador: {e}")
        return resultado


    # TODO 4.2: Ejecutar agente asignador
    # - Construir prompt con la clasificación obtenida
    # - Ejemplo: f"Asigna equipo para ticket {categoria}, urgencia {urgencia}"
    # - Parsear JSON y guardar en resultado["asignacion"]

    try:
        pass  # TODO: Implementar
    except json.JSONDecodeError as e:
        resultado["errores"].append(f"Error parseando asignación: {e}")
        return resultado
    except Exception as e:
        resultado["errores"].append(f"Error en asignador: {e}")
        return resultado


    # TODO 4.3: Ejecutar agente respuesta
    # - Construir prompt con toda la info disponible
    # - Este NO requiere parseo JSON
    # - Guardar en resultado["respuesta_cliente"]

    try:
        pass  # TODO: Implementar
    except Exception as e:
        resultado["errores"].append(f"Error en respuesta: {e}")
        return resultado

    return resultado


# ============================================================================
# TODO 5: TICKETS DE PRUEBA Y LOOP DE PROCESAMIENTO
# ============================================================================

# TODO 5.1: Crear 3-4 tickets de ejemplo con diferentes urgencias y categorías
# Ejemplos:
# - Crítico/Hardware: "El servidor principal no enciende, todas las operaciones están detenidas"
# - Media/Software: "Excel se cierra automáticamente al abrir archivos grandes"
# - Baja/Cuenta: "Olvidé mi contraseña del correo electrónico"

tickets_prueba = [
    # TODO: Agregar tickets aquí
]


def main():
    """Procesar todos los tickets de prueba."""
    print("=" * 80)
    print("SISTEMA DE TRIAJE DE TICKETS - MULTI-AGENTE CON JSON")
    print("=" * 80)

    # TODO 5.2: Iterar sobre tickets_prueba
    # Para cada ticket:
    # 1. Imprimir separador y número de ticket
    # 2. Llamar a procesar_ticket()
    # 3. Imprimir el ticket original
    # 4. Imprimir el JSON de clasificación (formateado con json.dumps indent=2)
    # 5. Imprimir el JSON de asignación
    # 6. Imprimir la respuesta al cliente
    # 7. Si hay errores, imprimirlos

    pass  # TODO: Implementar loop


if __name__ == "__main__":
    main()


# ============================================================================
# PUNTOS EXTRA (Opcional):
# ============================================================================
# 1. Agregar validación de campos obligatorios en los JSONs
# 2. Implementar retry automático si el JSON es inválido (máx 2 reintentos)
# 3. Agregar campo "confianza" (0-1) en la clasificación
# 4. Crear función para generar estadísticas de los tickets procesados
# 5. Guardar resultados en archivo JSON para análisis posterior
