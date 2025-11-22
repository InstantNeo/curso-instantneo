"""Skills para análisis de crashes en aplicaciones móviles"""

from instantneo.skills import skill
import re


@skill(
    description="Analiza stack traces de crashes móviles y sugiere causas probables",
    tags=["mobile", "debugging", "crash", "troubleshooting"]
)
def analizar_crash_log(stack_trace: str, plataforma: str = "Android") -> dict:
    """
    Analiza un stack trace de crash y proporciona diagnóstico.

    Args:
        stack_trace: Texto del stack trace del crash
        plataforma: Plataforma móvil (Android o iOS)

    Returns:
        Diccionario con análisis del crash y soluciones sugeridas
    """
    analisis = {
        "tipo_crash": "Desconocido",
        "causa_probable": "",
        "lineas_relevantes": [],
        "soluciones": []
    }

    if plataforma.lower() == "android":
        # Detectar tipo de excepción
        if "NullPointerException" in stack_trace or "NPE" in stack_trace:
            analisis["tipo_crash"] = "NullPointerException"
            analisis["causa_probable"] = "Intento de acceder a un objeto o variable que es null"
            analisis["soluciones"] = [
                "Agregar null checks antes de usar objetos",
                "Usar safe call operator (?.) en Kotlin",
                "Inicializar variables antes de usarlas",
                "Revisar lifecycle de Activities/Fragments"
            ]

        elif "OutOfMemoryError" in stack_trace or "OOM" in stack_trace:
            analisis["tipo_crash"] = "OutOfMemoryError"
            analisis["causa_probable"] = "La aplicación se quedó sin memoria disponible"
            analisis["soluciones"] = [
                "Optimizar carga de imágenes (usar Glide/Picasso)",
                "Implementar paginación en listas grandes",
                "Liberar recursos en onDestroy()",
                "Revisar memory leaks con LeakCanary",
                "Reducir tamaño de bitmaps antes de cargar"
            ]

        elif "ClassCastException" in stack_trace:
            analisis["tipo_crash"] = "ClassCastException"
            analisis["causa_probable"] = "Intento de cast inválido entre tipos incompatibles"
            analisis["soluciones"] = [
                "Verificar tipos antes de hacer cast",
                "Usar 'is' operator en Kotlin para verificar tipo",
                "Revisar generics en colecciones",
                "Validar datos de Intent extras"
            ]

        elif "IndexOutOfBoundsException" in stack_trace:
            analisis["tipo_crash"] = "IndexOutOfBoundsException"
            analisis["causa_probable"] = "Acceso a índice inválido en array o lista"
            analisis["soluciones"] = [
                "Verificar tamaño de lista antes de acceder",
                "Usar getOrNull() en Kotlin",
                "Validar índices en loops",
                "Comprobar que la lista no esté vacía"
            ]

        elif "IllegalStateException" in stack_trace:
            analisis["tipo_crash"] = "IllegalStateException"
            analisis["causa_probable"] = "Operación llamada en momento o estado inválido"
            analisis["soluciones"] = [
                "Revisar lifecycle de componentes",
                "No llamar UI operations después de onSaveInstanceState()",
                "Verificar estado de Fragment antes de transactions",
                "Usar commitAllowingStateLoss() con precaución"
            ]

        # Extraer líneas relevantes del stack trace
        lines = stack_trace.split('\n')
        for line in lines[:10]:  # Primeras 10 líneas son generalmente las más relevantes
            if 'at ' in line and ('com.', 'java.', 'android.') in line:
                analisis["lineas_relevantes"].append(line.strip())

    elif plataforma.lower() == "ios":
        # Detectar tipo de crash en iOS
        if "SIGSEGV" in stack_trace or "SEGV" in stack_trace:
            analisis["tipo_crash"] = "SIGSEGV (Segmentation Fault)"
            analisis["causa_probable"] = "Acceso a memoria inválida o liberada"
            analisis["soluciones"] = [
                "Revisar strong/weak references",
                "Verificar acceso a objetos deallocated",
                "Usar Address Sanitizer en Xcode",
                "Revisar crashes en background threads"
            ]

        elif "EXC_BAD_ACCESS" in stack_trace:
            analisis["tipo_crash"] = "EXC_BAD_ACCESS"
            analisis["causa_probable"] = "Acceso a memoria que ya fue liberada (zombie object)"
            analisis["soluciones"] = [
                "Habilitar Zombie Objects en Xcode",
                "Revisar retain cycles con Instruments",
                "Verificar delegates como weak",
                "Comprobar acceso a self en closures"
            ]

        elif "NSInvalidArgumentException" in stack_trace:
            analisis["tipo_crash"] = "NSInvalidArgumentException"
            analisis["causa_probable"] = "Argumento inválido pasado a un método"
            analisis["soluciones"] = [
                "Validar parámetros antes de llamar métodos",
                "Verificar tipos de datos en Objective-C",
                "Comprobar que objetos no sean nil",
                "Revisar configuración de xibs/storyboards"
            ]

        elif "fatal error: unexpectedly found nil" in stack_trace:
            analisis["tipo_crash"] = "Unwrapping nil Optional"
            analisis["causa_probable"] = "Force unwrap (!) de un Optional que es nil"
            analisis["soluciones"] = [
                "Usar optional binding (if let / guard let)",
                "Evitar force unwrapping (!)",
                "Usar nil coalescing operator (??)",
                "Inicializar optionals correctamente"
            ]

        # Extraer líneas relevantes
        lines = stack_trace.split('\n')
        for line in lines[:10]:
            if any(keyword in line for keyword in ['Thread', 'libsystem', 'Foundation', 'UIKit']):
                analisis["lineas_relevantes"].append(line.strip())

    # Intentar extraer archivo y línea donde ocurrió
    archivo_crash = None
    linea_crash = None

    if plataforma.lower() == "android":
        match = re.search(r'at\s+[\w.]+\(([\w.]+):(\d+)\)', stack_trace)
        if match:
            archivo_crash = match.group(1)
            linea_crash = match.group(2)
    elif plataforma.lower() == "ios":
        match = re.search(r'([\w.]+)\s+(\d+)\s+[\w.]+', stack_trace)
        if match:
            archivo_crash = match.group(1)
            linea_crash = match.group(2)

    return {
        "plataforma": plataforma,
        "tipo_crash": analisis["tipo_crash"],
        "causa_probable": analisis["causa_probable"],
        "archivo": archivo_crash,
        "linea": linea_crash,
        "stack_trace_relevante": analisis["lineas_relevantes"][:5],
        "soluciones_recomendadas": analisis["soluciones"],
        "herramientas_debugging": [
            "Android Studio Debugger" if plataforma.lower() == "android" else "Xcode Debugger",
            "Crashlytics/Firebase para tracking",
            "LeakCanary" if plataforma.lower() == "android" else "Instruments",
            "Logs del sistema (logcat/Console)"
        ],
        "siguiente_paso": "Reproducir el crash localmente usando el debugger y breakpoints"
    }


@skill(
    description="Sugiere herramientas y técnicas para debugging de crashes específicos",
    tags=["mobile", "debugging", "crash", "tools"]
)
def sugerir_herramientas_debugging(tipo_problema: str, plataforma: str = "Android") -> dict:
    """
    Sugiere herramientas específicas para debugging según el tipo de problema.

    Args:
        tipo_problema: Tipo de problema a debuggear (memory, ui, network, crash, etc.)
        plataforma: Plataforma móvil (Android o iOS)

    Returns:
        Diccionario con herramientas y técnicas recomendadas
    """
    herramientas = {
        "Android": {
            "memory": {
                "herramientas": [
                    "Android Profiler (Memory Profiler)",
                    "LeakCanary - detecta memory leaks automáticamente",
                    "MAT (Memory Analyzer Tool)",
                    "Android Studio Heap Dump"
                ],
                "tecnicas": [
                    "Tomar heap dumps en momentos específicos",
                    "Monitorear uso de memoria en tiempo real",
                    "Identificar objetos que no se liberan",
                    "Revisar lifecycle de Activities/Fragments"
                ]
            },
            "ui": {
                "herramientas": [
                    "Layout Inspector - analiza jerarquía de vistas",
                    "GPU Overdraw - detecta sobredibujo",
                    "Profile GPU Rendering",
                    "Espresso para UI testing"
                ],
                "tecnicas": [
                    "Reducir niveles de jerarquía de vistas",
                    "Usar ConstraintLayout para layouts complejos",
                    "Optimizar RecyclerView con ViewHolder pattern",
                    "Evitar operaciones pesadas en UI thread"
                ]
            },
            "network": {
                "herramientas": [
                    "Network Profiler en Android Studio",
                    "Charles Proxy / Fiddler",
                    "Stetho - debugging con Chrome DevTools",
                    "OkHttp Interceptors para logging"
                ],
                "tecnicas": [
                    "Interceptar y analizar requests/responses",
                    "Verificar códigos de estado HTTP",
                    "Revisar timeouts y reintentos",
                    "Simular conexiones lentas"
                ]
            },
            "crash": {
                "herramientas": [
                    "Firebase Crashlytics",
                    "Android Vitals (Play Console)",
                    "Bugsnag / Sentry",
                    "Android Studio Debugger"
                ],
                "tecnicas": [
                    "Analizar stack traces completos",
                    "Reproducir crashes localmente",
                    "Usar breakpoints condicionales",
                    "Habilitar strict mode para detectar problemas"
                ]
            }
        },
        "iOS": {
            "memory": {
                "herramientas": [
                    "Instruments - Leaks y Allocations",
                    "Memory Graph Debugger en Xcode",
                    "Debug Memory Graph",
                    "View Memory Graph Hierarchy"
                ],
                "tecnicas": [
                    "Detectar retain cycles con Instruments",
                    "Usar weak self en closures",
                    "Monitorear allocations y deallocations",
                    "Habilitar Address Sanitizer"
                ]
            },
            "ui": {
                "herramientas": [
                    "View Debugger en Xcode",
                    "Instruments - Core Animation",
                    "Time Profiler",
                    "XCUITest para testing"
                ],
                "tecnicas": [
                    "Analizar jerarquía de vistas 3D",
                    "Optimizar Auto Layout constraints",
                    "Reducir blending y offscreen rendering",
                    "Usar rasterization para vistas complejas"
                ]
            },
            "network": {
                "herramientas": [
                    "Network Link Conditioner",
                    "Charles Proxy / Proxyman",
                    "Instruments - Network template",
                    "URLSession debugging"
                ],
                "tecnicas": [
                    "Simular conexiones 3G/4G",
                    "Interceptar requests con proxy",
                    "Monitorear consumo de datos",
                    "Implementar cache estratégico"
                ]
            },
            "crash": {
                "herramientas": [
                    "Firebase Crashlytics",
                    "Xcode Organizer - Crashes",
                    "TestFlight Crash Reports",
                    "LLDB Debugger"
                ],
                "tecnicas": [
                    "Symbolicate crash reports",
                    "Usar symbolic breakpoints",
                    "Exception breakpoints",
                    "Habilitar Zombie Objects para EXC_BAD_ACCESS"
                ]
            }
        }
    }

    tipo_lower = tipo_problema.lower()
    plataforma_tools = herramientas.get(plataforma, {})
    info = plataforma_tools.get(tipo_lower)

    if not info:
        return {
            "error": f"Tipo de problema '{tipo_problema}' no encontrado",
            "tipos_disponibles": list(plataforma_tools.keys()),
            "plataforma": plataforma
        }

    return {
        "plataforma": plataforma,
        "tipo_problema": tipo_problema,
        "herramientas_recomendadas": info["herramientas"],
        "tecnicas_debugging": info["tecnicas"],
        "recursos_adicionales": [
            f"Documentación oficial de {'Android' if plataforma == 'Android' else 'Apple'}",
            "Stack Overflow - busca errores específicos",
            "Medium/Dev.to - artículos de debugging",
            "Comunidad de desarrolladores en Discord/Slack"
        ],
        "mejores_practicas": [
            "Debuggear en múltiples dispositivos y versiones de OS",
            "Mantener logs detallados pero no excesivos",
            "Usar analytics para detectar patrones",
            "Implementar feature flags para rollback rápido"
        ]
    }
