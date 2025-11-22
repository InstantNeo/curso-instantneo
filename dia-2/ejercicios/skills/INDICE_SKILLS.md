# Índice de Skills - Ejercicio 04

## API (4 skills)

### verificar_endpoint.py

1. **verificar_endpoint(url: str, metodo: str = "GET") -> dict**
   - Description: Verifica el estado y disponibilidad de un endpoint de API
   - Tags: api, debugging, monitoring
   - Uso: Diagnosticar problemas de conectividad y disponibilidad de endpoints

2. **diagnosticar_error_http(status_code: int, endpoint: str = "") -> dict**
   - Description: Analiza los códigos de respuesta HTTP de una API y sugiere soluciones
   - Tags: api, debugging, troubleshooting
   - Uso: Entender y resolver errores HTTP (400, 401, 403, 404, 500, 503)

### analizar_logs_api.py

3. **analizar_logs_api(log_texto: str, buscar_errores: bool = True) -> dict**
   - Description: Analiza logs de API en busca de patrones de error y anomalías
   - Tags: api, debugging, logs
   - Uso: Buscar errores, warnings, timeouts, problemas de conexión, rate limits

4. **extraer_metricas_rendimiento(log_texto: str) -> dict**
   - Description: Extrae métricas de rendimiento de logs de API (tiempos de respuesta, throughput)
   - Tags: api, monitoring, performance
   - Uso: Calcular P50, P95, P99, promedios, detectar requests lentos

---

## WebApp (4 skills)

### validar_html.py

5. **validar_html(html_codigo: str) -> dict**
   - Description: Valida la estructura HTML en busca de errores comunes y problemas de accesibilidad
   - Tags: webapp, debugging, html, accessibility
   - Uso: Detectar etiquetas sin cerrar, imágenes sin alt, inputs sin label, problemas de headings

6. **analizar_seo_html(html_codigo: str) -> dict**
   - Description: Analiza el SEO básico de una página HTML
   - Tags: webapp, seo, optimization
   - Uso: Validar title, meta description, viewport, estructura de headings

### debug_javascript.py

7. **analizar_codigo_javascript(js_codigo: str) -> dict**
   - Description: Analiza código JavaScript en busca de errores comunes y malas prácticas
   - Tags: webapp, debugging, javascript
   - Uso: Detectar uso de var, console.log, ==, funciones anónimas, callback hell, eval

8. **explicar_error_javascript(tipo_error: str, mensaje_error: str = "") -> dict**
   - Description: Explica errores comunes de JavaScript y cómo solucionarlos
   - Tags: webapp, debugging, javascript, troubleshooting
   - Uso: Entender TypeError, ReferenceError, SyntaxError, RangeError, errores de undefined

---

## Mobile (4 skills)

### check_permisos.py

9. **verificar_permisos_requeridos(funcionalidad: str, plataforma: str = "Android") -> dict**
   - Description: Verifica qué permisos necesita una funcionalidad de app móvil y si están configurados
   - Tags: mobile, debugging, permissions
   - Uso: Saber qué permisos declarar para cámara, ubicación, almacenamiento, notificaciones

10. **diagnosticar_problema_permisos(descripcion_problema: str, plataforma: str = "Android") -> dict**
    - Description: Diagnostica problemas comunes relacionados con permisos en apps móviles
    - Tags: mobile, debugging, permissions, troubleshooting
    - Uso: Resolver problemas de permisos denegados, cámara no funciona, ubicación no disponible

### analizar_crash.py

11. **analizar_crash_log(stack_trace: str, plataforma: str = "Android") -> dict**
    - Description: Analiza stack traces de crashes móviles y sugiere causas probables
    - Tags: mobile, debugging, crash, troubleshooting
    - Uso: Diagnosticar NullPointerException, OutOfMemoryError, crashes de iOS, etc.

12. **sugerir_herramientas_debugging(tipo_problema: str, plataforma: str = "Android") -> dict**
    - Description: Sugiere herramientas y técnicas para debugging de crashes específicos
    - Tags: mobile, debugging, crash, tools
    - Uso: Conocer herramientas para debuggear memory, UI, network, crashes

---

## Mapa de Uso por Escenario

### Problemas de API
```
Endpoint no responde
  -> verificar_endpoint()
  -> diagnosticar_error_http()

Logs con errores
  -> analizar_logs_api()

Performance lenta
  -> extraer_metricas_rendimiento()
```

### Problemas de WebApp
```
HTML roto
  -> validar_html()

Problemas de SEO
  -> analizar_seo_html()

Errores de JavaScript
  -> analizar_codigo_javascript()
  -> explicar_error_javascript()
```

### Problemas de Mobile
```
Funcionalidad requiere permiso
  -> verificar_permisos_requeridos()

Permiso denegado/no funciona
  -> diagnosticar_problema_permisos()

App crashea
  -> analizar_crash_log()

No sé cómo debuggear
  -> sugerir_herramientas_debugging()
```

---

## Tips de Implementación

1. **Todas las skills son funcionales** - No son mocks, tienen lógica real
2. **Fácil de extender** - Agrega más skills siguiendo el patrón existente
3. **Bien documentadas** - Cada skill tiene docstring y ejemplos
4. **Type-safe** - Todas usan type hints para validación
5. **Tagged** - Usa tags para filtrar skills relacionadas

## Agregar Nuevas Skills

Para agregar una nueva skill a cualquier categoría:

```python
from instantneo.skills import skill

@skill(
    description="Descripción clara de qué hace la skill",
    tags=["categoria", "subcategoria", "uso"]
)
def mi_nueva_skill(parametro: str, opcional: int = 10) -> dict:
    """
    Docstring completo.

    Args:
        parametro: Descripción del parámetro
        opcional: Parámetro opcional con default

    Returns:
        Diccionario con resultados
    """
    # Implementación
    return {"resultado": "valor"}
```

Guarda el archivo en la carpeta correspondiente y se cargará automáticamente con `load_skills.from_folder()`.
