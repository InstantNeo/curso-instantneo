"""Skills para verificación de endpoints de API"""

from instantneo.skills import skill
import json


@skill(
    description="Verifica el estado y disponibilidad de un endpoint de API",
    tags=["api", "debugging", "monitoring"]
)
def verificar_endpoint(url: str, metodo: str = "GET") -> dict:
    """
    Verifica si un endpoint de API está respondiendo correctamente.

    Args:
        url: URL del endpoint a verificar
        metodo: Método HTTP a usar (GET, POST, PUT, DELETE)

    Returns:
        Diccionario con el estado del endpoint
    """
    # Simulación de verificación de endpoint
    endpoints_validos = {
        "https://api.ejemplo.com/usuarios": {"status": 200, "tiempo_respuesta": "45ms"},
        "https://api.ejemplo.com/productos": {"status": 200, "tiempo_respuesta": "32ms"},
        "https://api.ejemplo.com/pedidos": {"status": 503, "tiempo_respuesta": "timeout"},
    }

    resultado = endpoints_validos.get(url, {"status": 404, "tiempo_respuesta": "N/A"})

    return {
        "url": url,
        "metodo": metodo,
        "status_code": resultado["status"],
        "tiempo_respuesta": resultado["tiempo_respuesta"],
        "disponible": resultado["status"] == 200
    }


@skill(
    description="Analiza los códigos de respuesta HTTP de una API y sugiere soluciones",
    tags=["api", "debugging", "troubleshooting"]
)
def diagnosticar_error_http(status_code: int, endpoint: str = "") -> dict:
    """
    Analiza un código de error HTTP y proporciona diagnóstico y soluciones.

    Args:
        status_code: Código de estado HTTP recibido
        endpoint: URL del endpoint que generó el error (opcional)

    Returns:
        Diccionario con diagnóstico y soluciones recomendadas
    """
    diagnosticos = {
        400: {
            "tipo": "Bad Request",
            "causa": "La solicitud tiene sintaxis incorrecta o parámetros inválidos",
            "soluciones": [
                "Verificar formato JSON del body",
                "Validar parámetros de query string",
                "Revisar headers requeridos"
            ]
        },
        401: {
            "tipo": "Unauthorized",
            "causa": "Falta autenticación o las credenciales son inválidas",
            "soluciones": [
                "Verificar token de autenticación",
                "Comprobar que el token no haya expirado",
                "Validar API key en headers"
            ]
        },
        403: {
            "tipo": "Forbidden",
            "causa": "El usuario no tiene permisos para acceder al recurso",
            "soluciones": [
                "Verificar roles y permisos del usuario",
                "Comprobar políticas de acceso",
                "Validar scope del token"
            ]
        },
        404: {
            "tipo": "Not Found",
            "causa": "El recurso solicitado no existe",
            "soluciones": [
                "Verificar la URL del endpoint",
                "Comprobar que el ID del recurso sea válido",
                "Revisar documentación de la API"
            ]
        },
        500: {
            "tipo": "Internal Server Error",
            "causa": "Error en el servidor al procesar la solicitud",
            "soluciones": [
                "Revisar logs del servidor",
                "Verificar conexión a base de datos",
                "Comprobar configuración de servicios externos"
            ]
        },
        503: {
            "tipo": "Service Unavailable",
            "causa": "El servicio no está disponible temporalmente",
            "soluciones": [
                "Verificar estado de los servicios",
                "Comprobar límites de rate limiting",
                "Revisar health checks del sistema"
            ]
        }
    }

    diagnostico = diagnosticos.get(
        status_code,
        {
            "tipo": f"Error {status_code}",
            "causa": "Error HTTP no catalogado",
            "soluciones": ["Consultar documentación de códigos HTTP estándar"]
        }
    )

    return {
        "status_code": status_code,
        "endpoint": endpoint,
        "tipo_error": diagnostico["tipo"],
        "causa_probable": diagnostico["causa"],
        "soluciones_recomendadas": diagnostico["soluciones"]
    }
