# Skills para Ejercicio 04: Sistema de Soporte Multi-Producto

Esta carpeta contiene las skills especializadas para cada tipo de producto.

## Estructura

```
skills/
├── api/                    # Skills para debugging de APIs
│   ├── verificar_endpoint.py       (2 skills)
│   └── analizar_logs_api.py        (2 skills)
│
├── webapp/                 # Skills para debugging de WebApps
│   ├── validar_html.py             (2 skills)
│   └── debug_javascript.py         (2 skills)
│
└── mobile/                 # Skills para debugging de Apps Móviles
    ├── check_permisos.py           (2 skills)
    └── analizar_crash.py           (2 skills)
```

## Skills por Categoría

### API (6 skills total)

1. **verificar_endpoint**: Verifica estado y disponibilidad de endpoints
2. **diagnosticar_error_http**: Analiza códigos HTTP y sugiere soluciones
3. **analizar_logs_api**: Busca patrones de error en logs de API
4. **extraer_metricas_rendimiento**: Extrae métricas de tiempos de respuesta

### WebApp (4 skills total)

1. **validar_html**: Valida estructura HTML y accesibilidad
2. **analizar_seo_html**: Analiza aspectos básicos de SEO
3. **analizar_codigo_javascript**: Busca errores y malas prácticas en JS
4. **explicar_error_javascript**: Explica errores comunes de JavaScript

### Mobile (4 skills total)

1. **verificar_permisos_requeridos**: Verifica permisos necesarios por funcionalidad
2. **diagnosticar_problema_permisos**: Diagnostica problemas de permisos
3. **analizar_crash_log**: Analiza stack traces de crashes
4. **sugerir_herramientas_debugging**: Sugiere herramientas específicas

## Uso

Estas skills se cargan dinámicamente según el tipo de ticket:

```python
# Cargar solo skills de API
skill_manager.clear_registry()
skill_manager.load_skills.from_folder("skills/api")

# Cargar solo skills de WebApp
skill_manager.clear_registry()
skill_manager.load_skills.from_folder("skills/webapp")

# Cargar solo skills de Mobile
skill_manager.clear_registry()
skill_manager.load_skills.from_folder("skills/mobile")

# Modo ADMIN: cargar todas
for producto in ["api", "webapp", "mobile"]:
    skill_manager.load_skills.from_folder(f"skills/{producto}")
```

## Características de las Skills

- **Funcionales**: Todas tienen implementación real (no mocks)
- **Documentadas**: Descripciones claras y docstrings completas
- **Tagged**: Cada skill tiene tags para filtrado
- **Type-hinted**: Parámetros con type hints para validación
- **Prácticas**: Basadas en problemas reales de debugging

## Extender

Para agregar nuevas categorías de producto:

1. Crear nueva carpeta (ej: `database/`)
2. Crear archivos con skills decoradas
3. Agregar detección en `detectar_producto()`
4. Las skills se cargarán automáticamente con `from_folder()`
