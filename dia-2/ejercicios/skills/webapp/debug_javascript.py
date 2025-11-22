"""Skills para debugging de JavaScript"""

from instantneo.skills import skill
import re


@skill(
    description="Analiza código JavaScript en busca de errores comunes y malas prácticas",
    tags=["webapp", "debugging", "javascript"]
)
def analizar_codigo_javascript(js_codigo: str) -> dict:
    """
    Analiza código JavaScript buscando errores comunes y code smells.

    Args:
        js_codigo: Código JavaScript a analizar

    Returns:
        Diccionario con análisis de código y problemas encontrados
    """
    errores = []
    warnings = []
    sugerencias = []

    # Verificar uso de var en lugar de let/const
    var_usage = re.findall(r'\bvar\s+\w+', js_codigo)
    if var_usage:
        warnings.append(f"Uso de 'var' encontrado ({len(var_usage)} veces). Considera usar 'let' o 'const'")

    # Verificar console.log olvidados
    console_logs = re.findall(r'console\.log\(', js_codigo)
    if console_logs:
        sugerencias.append(f"Encontrados {len(console_logs)} console.log() - considera removerlos en producción")

    # Verificar == en lugar de ===
    loose_equality = re.findall(r'[^=!<>]==[^=]', js_codigo)
    if loose_equality:
        warnings.append(f"Uso de '==' encontrado ({len(loose_equality)} veces). Usa '===' para comparación estricta")

    # Verificar funciones sin nombre (difíciles de debuggear)
    anonymous_funcs = re.findall(r'function\s*\(', js_codigo)
    if anonymous_funcs:
        sugerencias.append(f"{len(anonymous_funcs)} funciones anónimas - considera nombrarlas para mejor debugging")

    # Verificar callbacks anidados (callback hell)
    lineas = js_codigo.split('\n')
    max_indentation = 0
    for linea in lineas:
        if linea.strip():
            espacios = len(linea) - len(linea.lstrip())
            max_indentation = max(max_indentation, espacios)

    if max_indentation > 16:  # 4 niveles de indentación
        warnings.append("Indentación muy profunda detectada - posible 'callback hell'. Considera usar Promises o async/await")

    # Verificar try/catch sin manejo
    try_blocks = re.findall(r'try\s*{[^}]*}\s*catch\s*\([^)]*\)\s*{([^}]*)}', js_codigo, re.DOTALL)
    for catch_block in try_blocks:
        if not catch_block.strip() or catch_block.strip() == '':
            errores.append("Bloque catch vacío encontrado - los errores están siendo silenciados")

    # Verificar uso de eval (peligroso)
    if re.search(r'\beval\s*\(', js_codigo):
        errores.append("Uso de eval() detectado - esto es un riesgo de seguridad")

    return {
        "codigo_limpio": len(errores) == 0 and len(warnings) == 0,
        "total_errores": len(errores),
        "total_warnings": len(warnings),
        "total_sugerencias": len(sugerencias),
        "errores": errores,
        "warnings": warnings,
        "sugerencias": sugerencias,
        "calidad_codigo": "ALTA" if len(errores) == 0 and len(warnings) <= 2 else "MEDIA" if len(errores) == 0 else "BAJA"
    }


@skill(
    description="Explica errores comunes de JavaScript y cómo solucionarlos",
    tags=["webapp", "debugging", "javascript", "troubleshooting"]
)
def explicar_error_javascript(tipo_error: str, mensaje_error: str = "") -> dict:
    """
    Proporciona explicación y soluciones para errores comunes de JavaScript.

    Args:
        tipo_error: Tipo de error (TypeError, ReferenceError, SyntaxError, etc.)
        mensaje_error: Mensaje de error completo (opcional)

    Returns:
        Diccionario con explicación y soluciones
    """
    errores_comunes = {
        "TypeError": {
            "explicacion": "Ocurre cuando un valor no es del tipo esperado",
            "causas_comunes": [
                "Intentar llamar a algo que no es una función",
                "Acceder a propiedades de null o undefined",
                "Operaciones inválidas en tipos de datos"
            ],
            "soluciones": [
                "Verificar que la variable esté definida antes de usarla",
                "Usar optional chaining (?.) para acceso seguro",
                "Validar tipos con typeof antes de operaciones"
            ]
        },
        "ReferenceError": {
            "explicacion": "Se intenta acceder a una variable que no existe",
            "causas_comunes": [
                "Variable no declarada",
                "Typo en el nombre de la variable",
                "Variable fuera de scope"
            ],
            "soluciones": [
                "Verificar que la variable esté declarada con let/const/var",
                "Revisar el scope de la variable",
                "Comprobar ortografía del nombre de variable"
            ]
        },
        "SyntaxError": {
            "explicacion": "El código tiene sintaxis inválida que el parser no puede interpretar",
            "causas_comunes": [
                "Paréntesis, llaves o corchetes sin cerrar",
                "Comas o puntos y comas faltantes o extras",
                "Uso incorrecto de palabras reservadas"
            ],
            "soluciones": [
                "Usar un linter (ESLint) para detectar errores de sintaxis",
                "Verificar que todas las llaves estén balanceadas",
                "Revisar el código línea por línea desde donde marca el error"
            ]
        },
        "RangeError": {
            "explicacion": "Un valor numérico está fuera del rango permitido",
            "causas_comunes": [
                "Array con tamaño negativo o muy grande",
                "Recursión infinita (stack overflow)",
                "toFixed/toPrecision con valores inválidos"
            ],
            "soluciones": [
                "Validar tamaños de arrays antes de crearlos",
                "Agregar condición de salida en funciones recursivas",
                "Verificar rangos de parámetros numéricos"
            ]
        },
        "Cannot read property of undefined": {
            "explicacion": "Intentas acceder a una propiedad de un valor que es undefined",
            "causas_comunes": [
                "Objeto no inicializado",
                "Respuesta de API aún no cargada",
                "Propiedad mal escrita"
            ],
            "soluciones": [
                "Usar optional chaining: obj?.prop",
                "Verificar con if (obj) antes de acceder",
                "Usar valores por defecto: const value = obj?.prop || 'default'"
            ]
        }
    }

    # Detectar tipo de error del mensaje si no se especificó
    if not tipo_error and mensaje_error:
        for error_tipo in errores_comunes.keys():
            if error_tipo in mensaje_error:
                tipo_error = error_tipo
                break

    info = errores_comunes.get(
        tipo_error,
        {
            "explicacion": "Error JavaScript genérico",
            "causas_comunes": ["Revisa la consola del navegador para más detalles"],
            "soluciones": ["Usa las DevTools del navegador para debuggear paso a paso"]
        }
    )

    return {
        "tipo_error": tipo_error,
        "mensaje_original": mensaje_error,
        "explicacion": info["explicacion"],
        "causas_comunes": info["causas_comunes"],
        "soluciones_recomendadas": info["soluciones"],
        "herramientas_debugging": [
            "Chrome DevTools / Firefox Developer Tools",
            "console.log() estratégico",
            "debugger; statement",
            "Source maps para código minificado"
        ]
    }
