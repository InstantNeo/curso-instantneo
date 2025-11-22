"""Skills para análisis de logs de API"""

from instantneo.skills import skill
from datetime import datetime
import re


@skill(
    description="Analiza logs de API en busca de patrones de error y anomalías",
    tags=["api", "debugging", "logs"]
)
def analizar_logs_api(log_texto: str, buscar_errores: bool = True) -> dict:
    """
    Analiza texto de logs de API buscando errores, warnings y patrones anómalos.

    Args:
        log_texto: Texto del log a analizar
        buscar_errores: Si True, enfoca el análisis en errores

    Returns:
        Diccionario con análisis de logs y hallazgos
    """
    # Patrones comunes en logs
    patrones = {
        "error": r"(ERROR|error|Error).*",
        "warning": r"(WARNING|warning|Warning).*",
        "timeout": r".*(timeout|timed out|TIMEOUT).*",
        "connection": r".*(connection refused|connection failed|cannot connect).*",
        "rate_limit": r".*(rate limit|too many requests|429).*"
    }

    hallazgos = {
        "errores": [],
        "warnings": [],
        "timeouts": [],
        "problemas_conexion": [],
        "rate_limits": []
    }

    lineas = log_texto.split('\n')

    for linea in lineas:
        if re.search(patrones["error"], linea):
            hallazgos["errores"].append(linea.strip())
        if re.search(patrones["warning"], linea):
            hallazgos["warnings"].append(linea.strip())
        if re.search(patrones["timeout"], linea):
            hallazgos["timeouts"].append(linea.strip())
        if re.search(patrones["connection"], linea):
            hallazgos["problemas_conexion"].append(linea.strip())
        if re.search(patrones["rate_limit"], linea):
            hallazgos["rate_limits"].append(linea.strip())

    total_problemas = sum(len(v) for v in hallazgos.values())

    return {
        "lineas_analizadas": len(lineas),
        "problemas_encontrados": total_problemas,
        "errores_count": len(hallazgos["errores"]),
        "warnings_count": len(hallazgos["warnings"]),
        "timeouts_count": len(hallazgos["timeouts"]),
        "hallazgos_detallados": hallazgos,
        "severidad": "ALTA" if len(hallazgos["errores"]) > 5 else "MEDIA" if len(hallazgos["errores"]) > 0 else "BAJA"
    }


@skill(
    description="Extrae métricas de rendimiento de logs de API (tiempos de respuesta, throughput)",
    tags=["api", "monitoring", "performance"]
)
def extraer_metricas_rendimiento(log_texto: str) -> dict:
    """
    Extrae métricas de rendimiento de logs de API.

    Args:
        log_texto: Texto del log con información de tiempos de respuesta

    Returns:
        Diccionario con métricas calculadas
    """
    # Buscar patrones de tiempo de respuesta (ej: "response_time: 123ms")
    patron_tiempo = r"response[_\s]time[:\s]+(\d+)ms"
    tiempos = [int(t) for t in re.findall(patron_tiempo, log_texto)]

    if not tiempos:
        return {
            "error": "No se encontraron métricas de tiempo de respuesta en los logs",
            "metricas_disponibles": False
        }

    promedio = sum(tiempos) / len(tiempos)
    tiempos_ordenados = sorted(tiempos)
    p50 = tiempos_ordenados[len(tiempos_ordenados) // 2]
    p95 = tiempos_ordenados[int(len(tiempos_ordenados) * 0.95)]
    p99 = tiempos_ordenados[int(len(tiempos_ordenados) * 0.99)]

    return {
        "metricas_disponibles": True,
        "total_requests": len(tiempos),
        "tiempo_promedio_ms": round(promedio, 2),
        "tiempo_minimo_ms": min(tiempos),
        "tiempo_maximo_ms": max(tiempos),
        "p50_ms": p50,
        "p95_ms": p95,
        "p99_ms": p99,
        "requests_lentos": len([t for t in tiempos if t > 1000]),
        "rendimiento": "EXCELENTE" if promedio < 100 else "BUENO" if promedio < 500 else "NECESITA_OPTIMIZACION"
    }
