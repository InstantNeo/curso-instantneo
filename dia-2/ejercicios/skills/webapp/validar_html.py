"""Skills para validación de HTML y estructura web"""

from instantneo.skills import skill
import re


@skill(
    description="Valida la estructura HTML en busca de errores comunes y problemas de accesibilidad",
    tags=["webapp", "debugging", "html", "accessibility"]
)
def validar_html(html_codigo: str) -> dict:
    """
    Valida código HTML en busca de errores estructurales y problemas de accesibilidad.

    Args:
        html_codigo: Código HTML a validar

    Returns:
        Diccionario con errores y warnings encontrados
    """
    errores = []
    warnings = []

    # Verificar etiquetas sin cerrar
    etiquetas_abiertas = re.findall(r'<(\w+)[^>]*>', html_codigo)
    etiquetas_cerradas = re.findall(r'</(\w+)>', html_codigo)

    # Etiquetas que no necesitan cierre
    auto_cerradas = {'img', 'br', 'hr', 'input', 'meta', 'link'}

    for tag in etiquetas_abiertas:
        if tag not in auto_cerradas and etiquetas_abiertas.count(tag) > etiquetas_cerradas.count(tag):
            errores.append(f"Etiqueta <{tag}> no está cerrada correctamente")

    # Verificar imágenes sin alt
    imgs_sin_alt = re.findall(r'<img(?![^>]*alt=)[^>]*>', html_codigo)
    if imgs_sin_alt:
        warnings.append(f"Encontradas {len(imgs_sin_alt)} imágenes sin atributo alt (problema de accesibilidad)")

    # Verificar inputs sin label
    inputs = re.findall(r'<input[^>]*>', html_codigo)
    labels = re.findall(r'<label[^>]*>', html_codigo)
    if len(inputs) > len(labels):
        warnings.append(f"{len(inputs) - len(labels)} inputs sin label asociado (problema de accesibilidad)")

    # Verificar headings en orden
    h1_count = len(re.findall(r'<h1[^>]*>', html_codigo))
    if h1_count == 0:
        warnings.append("No se encontró etiqueta <h1> (importante para SEO)")
    elif h1_count > 1:
        warnings.append(f"Múltiples etiquetas <h1> encontradas ({h1_count}). Se recomienda solo una por página")

    # Verificar enlaces sin texto
    enlaces_vacios = re.findall(r'<a[^>]*>\s*</a>', html_codigo)
    if enlaces_vacios:
        errores.append(f"{len(enlaces_vacios)} enlaces sin texto de contenido")

    return {
        "html_valido": len(errores) == 0,
        "total_errores": len(errores),
        "total_warnings": len(warnings),
        "errores": errores,
        "warnings": warnings,
        "puntuacion_accesibilidad": max(0, 100 - (len(errores) * 20 + len(warnings) * 5))
    }


@skill(
    description="Analiza el SEO básico de una página HTML",
    tags=["webapp", "seo", "optimization"]
)
def analizar_seo_html(html_codigo: str) -> dict:
    """
    Analiza aspectos básicos de SEO en código HTML.

    Args:
        html_codigo: Código HTML a analizar

    Returns:
        Diccionario con análisis SEO y recomendaciones
    """
    problemas = []
    recomendaciones = []
    puntos_positivos = []

    # Verificar title
    title_match = re.search(r'<title>([^<]+)</title>', html_codigo)
    if not title_match:
        problemas.append("Falta etiqueta <title>")
    else:
        title_text = title_match.group(1)
        if len(title_text) < 30:
            recomendaciones.append(f"Title muy corto ({len(title_text)} caracteres). Recomendado: 50-60")
        elif len(title_text) > 60:
            recomendaciones.append(f"Title muy largo ({len(title_text)} caracteres). Recomendado: 50-60")
        else:
            puntos_positivos.append("Title tiene longitud óptima")

    # Verificar meta description
    meta_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html_codigo)
    if not meta_desc:
        problemas.append("Falta meta description")
    else:
        desc_text = meta_desc.group(1)
        if len(desc_text) < 120:
            recomendaciones.append(f"Meta description corta ({len(desc_text)} caracteres). Recomendado: 150-160")
        elif len(desc_text) > 160:
            recomendaciones.append(f"Meta description larga ({len(desc_text)} caracteres). Recomendado: 150-160")
        else:
            puntos_positivos.append("Meta description tiene longitud óptima")

    # Verificar meta viewport (mobile-friendly)
    if re.search(r'<meta\s+name=["\']viewport["\']', html_codigo):
        puntos_positivos.append("Tiene meta viewport configurado (mobile-friendly)")
    else:
        problemas.append("Falta meta viewport (no optimizado para móviles)")

    # Verificar estructura de headings
    h1_count = len(re.findall(r'<h1[^>]*>', html_codigo))
    h2_count = len(re.findall(r'<h2[^>]*>', html_codigo))

    if h1_count == 1:
        puntos_positivos.append("Tiene exactamente un H1 (óptimo)")
    elif h1_count == 0:
        problemas.append("No tiene H1 (crítico para SEO)")
    else:
        problemas.append(f"Tiene {h1_count} H1 (debería tener solo uno)")

    if h2_count > 0:
        puntos_positivos.append(f"Tiene {h2_count} H2 (buena estructura)")

    # Calcular puntuación SEO
    puntuacion = 100 - (len(problemas) * 25 + len(recomendaciones) * 10)
    puntuacion = max(0, min(100, puntuacion))

    return {
        "puntuacion_seo": puntuacion,
        "estado": "EXCELENTE" if puntuacion >= 80 else "BUENO" if puntuacion >= 60 else "NECESITA_MEJORAS",
        "problemas_criticos": problemas,
        "recomendaciones": recomendaciones,
        "puntos_positivos": puntos_positivos,
        "total_problemas": len(problemas),
        "total_recomendaciones": len(recomendaciones)
    }
