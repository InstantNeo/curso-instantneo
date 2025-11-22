"""
EJERCICIO 04: Sistema de Soporte Multi-Producto (Agente Multi-Modo)

OBJETIVO:
Crear un agente de soporte técnico que cambia dinámicamente sus skills
según el tipo de producto del ticket (API, WebApp o Mobile).

CONCEPTO CLAVE:
- clear_registry(): Limpia todas las skills registradas
- load_skills.from_folder(): Carga skills de una carpeta específica
- Cambio dinámico de capacidades según contexto

ESCENARIO:
Tu empresa tiene 3 productos diferentes:
- API Backend
- Aplicación Web (Frontend)
- App Móvil (iOS/Android)

Cada producto tiene sus propias herramientas de debugging (skills).
El agente debe cargar solo las skills relevantes para cada ticket.

ESTRUCTURA DE SKILLS A CREAR:
skills/
├── api/
│   ├── verificar_endpoint.py
│   └── analizar_logs_api.py
├── webapp/
│   ├── validar_html.py
│   └── debug_javascript.py
└── mobile/
    ├── check_permisos.py
    └── analizar_crash.py

INSTRUCCIONES:
1. Crea la estructura de carpetas skills/ con las subcarpetas api/, webapp/, mobile/
2. En cada subcarpeta, crea 1-2 archivos .py con skills decoradas con @skill
3. Cada skill debe tener description, tags apropiados, y código funcional (no mock)
4. Implementa las funciones TODO en este archivo

CRITERIOS DE ÉXITO:
✓ El agente detecta correctamente el tipo de producto
✓ Carga solo las skills del producto correspondiente
✓ Limpia el registry entre cambios de producto
✓ Procesa los 3 tickets de ejemplo correctamente
✓ BONUS: Implementa modo "admin" que carga todas las skills
"""

import os
from dotenv import load_dotenv
from instantneo import InstantNeo
from instantneo.skills import SkillManager

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar (configurable desde .env)

GROQ_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.3-70b-versatile")  # Default si no está en .env

print(f"🔧 Modelo configurado: {GROQ_MODEL}")


# ==================== CONFIGURACIÓN ====================

# TODO: Ajusta esta ruta a donde creaste la carpeta skills/
SKILLS_BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "soluciones", "skills")

# Configuración del agente
API_KEY = os.getenv("API_KEY", "tu-api-key-aqui")
PROVIDER = "openai"  # o "anthropic" o "groq"


# ==================== TICKETS DE EJEMPLO ====================

tickets = [
    {
        "id": "TK-001",
        "producto": "API",
        "problema": "El endpoint /api/usuarios está devolviendo 503. Necesito verificar el estado y analizar los logs.",
        "prioridad": "ALTA"
    },
    {
        "id": "TK-002",
        "producto": "WebApp",
        "problema": "La página de login tiene problemas de accesibilidad y errores en el JavaScript. Validar HTML y debuggear JS.",
        "prioridad": "MEDIA"
    },
    {
        "id": "TK-003",
        "producto": "Mobile",
        "problema": "La app crashea al intentar usar la cámara en Android. Verificar permisos y analizar crash log.",
        "prioridad": "ALTA"
    }
]


# ==================== TODO 1: FUNCIÓN DETECTAR PRODUCTO ====================

def detectar_producto(descripcion_ticket: str) -> str:
    """
    Detecta el tipo de producto basándose en palabras clave en el ticket.

    Args:
        descripcion_ticket: Texto del ticket de soporte

    Returns:
        "api", "webapp", "mobile" o "desconocido"

    TODO: Implementa la lógica de detección
    Pistas:
    - Busca palabras clave como "endpoint", "HTML", "JavaScript", "crash", "permisos", etc.
    - Convierte el texto a lowercase para hacer matching case-insensitive
    - Puedes usar 'in' operator o regex

    Ejemplo:
        if "endpoint" in descripcion.lower():
            return "api"
    """
    descripcion = descripcion_ticket.lower()

    # TODO: Completa la lógica aquí
    # Palabras clave sugeridas:
    # API: endpoint, api, rest, http, status code, logs
    # WebApp: html, javascript, css, dom, navegador, frontend
    # Mobile: app, móvil, android, ios, crash, permisos, cámara

    pass  # Reemplaza con tu código


# ==================== TODO 2: FUNCIÓN CARGAR SKILLS ====================

def cargar_skills_producto(skill_manager: SkillManager, producto: str) -> bool:
    """
    Limpia el registry y carga las skills específicas del producto.

    Args:
        skill_manager: Instancia del SkillManager del agente
        producto: Tipo de producto ("api", "webapp", "mobile")

    Returns:
        True si se cargaron skills, False si no

    TODO: Implementa la carga dinámica de skills
    Pasos:
    1. Limpiar el registry con clear_registry()
    2. Construir la ruta de la carpeta de skills del producto
    3. Verificar que la carpeta existe
    4. Cargar skills con load_skills.from_folder()
    5. Retornar True si se cargó al menos una skill

    Pistas:
    - skill_manager.clear_registry()
    - os.path.join(SKILLS_BASE_PATH, producto)
    - os.path.exists(ruta)
    - skill_manager.load_skills.from_folder(ruta)
    - skill_manager.get_skill_names() para verificar
    """

    # TODO: 1. Limpiar el registry


    # TODO: 2. Construir ruta de carpeta de skills
    # Ejemplo: C:\...\skills\api


    # TODO: 3. Verificar que existe la carpeta


    # TODO: 4. Cargar skills de la carpeta


    # TODO: 5. Verificar que se cargaron skills y retornar True/False


    pass  # Reemplaza con tu código


# ==================== TODO 3: LOOP DE PROCESAMIENTO ====================

def procesar_tickets():
    """
    Procesa todos los tickets cambiando las skills dinámicamente.

    TODO: Implementa el loop de procesamiento
    Pasos para cada ticket:
    1. Detectar el tipo de producto
    2. Cargar las skills correspondientes
    3. Mostrar qué skills están cargadas
    4. Ejecutar el agente con el problema del ticket
    5. Mostrar la respuesta

    Estructura sugerida:
        for ticket in tickets:
            print(f"\n{'='*60}")
            print(f"Procesando {ticket['id']}: {ticket['producto']}")
            print(f"Prioridad: {ticket['prioridad']}")

            # Detectar producto
            producto_detectado = detectar_producto(ticket['problema'])

            # Cargar skills
            if cargar_skills_producto(...):
                # Mostrar skills cargadas
                # Ejecutar agente
                # Mostrar respuesta
            else:
                print("Error: No se pudieron cargar skills")
    """

    # Crear el agente (se reutiliza, solo cambian las skills)
    agente = InstantNeo(
        api_key=API_KEY,
        provider=PROVIDER,
        model=GROQ_MODEL,
        temperature=0.3
    )

    # TODO: Implementa el loop aquí
    # for ticket in tickets:
    #     ...


    pass  # Reemplaza con tu código


# ==================== BONUS: MODO ADMIN ====================

def modo_admin():
    """
    BONUS CHALLENGE:
    Implementa un modo "admin" que carga TODAS las skills de todos los productos.

    El agente tendría acceso a todas las herramientas de debugging a la vez.

    TODO BONUS:
    1. Limpiar registry
    2. Cargar skills de api/, webapp/ y mobile/
    3. Crear un ticket complejo que requiera skills de múltiples productos
    4. Ejecutar el agente

    Ejemplo de ticket complejo:
    "Tenemos un problema end-to-end: el endpoint /api/productos devuelve datos
    corruptos (verificar API), que causan errores de JavaScript en el frontend
    (debuggear WebApp), y la app móvil crashea al intentar mostrarlos (analizar Mobile)."
    """

    print("\n" + "="*60)
    print("MODO ADMIN: Cargando todas las skills...")
    print("="*60)

    # TODO BONUS: Implementa aquí

    pass


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """
    Función principal que ejecuta el ejercicio.
    """

    print("="*60)
    print("EJERCICIO 04: SISTEMA DE SOPORTE MULTI-PRODUCTO")
    print("="*60)

    # Verificar que existe la carpeta de skills
    if not os.path.exists(SKILLS_BASE_PATH):
        print(f"\n❌ ERROR: No se encuentra la carpeta de skills en:")
        print(f"   {SKILLS_BASE_PATH}")
        print(f"\n📝 INSTRUCCIONES:")
        print(f"   1. Crea la carpeta 'skills' con subcarpetas: api/, webapp/, mobile/")
        print(f"   2. En cada subcarpeta, crea archivos .py con skills decoradas")
        print(f"   3. Ajusta SKILLS_BASE_PATH si es necesario")
        return

    print(f"\n✓ Carpeta de skills encontrada: {SKILLS_BASE_PATH}")
    print(f"\nProcesando {len(tickets)} tickets...\n")

    # Procesar tickets normales
    procesar_tickets()

    # BONUS: Modo admin (descomenta para probar)
    # modo_admin()

    print("\n" + "="*60)
    print("✓ Ejercicio completado")
    print("="*60)


if __name__ == "__main__":
    main()


"""
NOTAS PARA EL ALUMNO:

1. ORDEN DE IMPLEMENTACIÓN:
   - Primero crea la estructura de carpetas y skills
   - Luego implementa detectar_producto()
   - Después cargar_skills_producto()
   - Finalmente el loop en procesar_tickets()

2. TESTING:
   - Prueba cada función por separado antes de integrar
   - Verifica que clear_registry() realmente limpia
   - Imprime los skill_names antes y después de cargar

3. DEBUGGING:
   - Si no encuentra las skills, imprime SKILLS_BASE_PATH
   - Verifica que los archivos .py tengan el decorator @skill
   - Asegúrate que cada skill tenga description y tags

4. EXTENSION:
   - Agrega más productos (database, cloud, etc.)
   - Crea skills más complejas
   - Implementa detección automática de producto con IA
   - Añade logging para auditoría de cambios de skills

¡Buena suerte! 🚀
"""
