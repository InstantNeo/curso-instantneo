"""
EJERCICIO 04 - SOLUCIÓN: Sistema de Soporte Multi-Producto (Agente Multi-Modo)

Esta es la implementación completa del ejercicio.
Demuestra cómo un agente puede cambiar dinámicamente sus capacidades
según el contexto, cargando y descargando skills según sea necesario.

CARACTERÍSTICAS:
✓ Detección automática de tipo de producto
✓ Carga dinámica de skills específicas por producto
✓ Limpieza de registry entre cambios
✓ Procesamiento de múltiples tickets con diferentes contextos
✓ BONUS: Modo admin con todas las skills cargadas
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

# Ruta a la carpeta de skills (relativa al archivo de solución)
SKILLS_BASE_PATH = os.path.join(os.path.dirname(__file__), "skills")

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


# ==================== SOLUCIÓN 1: DETECTAR PRODUCTO ====================

def detectar_producto(descripcion_ticket: str) -> str:
    """
    Detecta el tipo de producto basándose en palabras clave en el ticket.

    Args:
        descripcion_ticket: Texto del ticket de soporte

    Returns:
        "api", "webapp", "mobile" o "desconocido"
    """
    descripcion = descripcion_ticket.lower()

    # Definir palabras clave por tipo de producto
    keywords_api = [
        "endpoint", "api", "rest", "http", "status code",
        "logs api", "servicio", "backend", "servidor"
    ]

    keywords_webapp = [
        "html", "javascript", "css", "dom", "navegador",
        "frontend", "página", "web", "accesibilidad", "seo"
    ]

    keywords_mobile = [
        "app", "móvil", "android", "ios", "crash",
        "permisos", "cámara", "mobile", "smartphone", "tablet"
    ]

    # Contar coincidencias para cada tipo
    score_api = sum(1 for kw in keywords_api if kw in descripcion)
    score_webapp = sum(1 for kw in keywords_webapp if kw in descripcion)
    score_mobile = sum(1 for kw in keywords_mobile if kw in descripcion)

    # Retornar el tipo con mayor score
    max_score = max(score_api, score_webapp, score_mobile)

    if max_score == 0:
        return "desconocido"

    if score_api == max_score:
        return "api"
    elif score_webapp == max_score:
        return "webapp"
    else:
        return "mobile"


# ==================== SOLUCIÓN 2: CARGAR SKILLS ====================

def cargar_skills_producto(skill_manager: SkillManager, producto: str) -> bool:
    """
    Limpia el registry y carga las skills específicas del producto.

    Args:
        skill_manager: Instancia del SkillManager del agente
        producto: Tipo de producto ("api", "webapp", "mobile")

    Returns:
        True si se cargaron skills, False si no
    """

    # 1. Limpiar el registry de skills existentes
    print(f"   🧹 Limpiando registry...")
    skills_antes = skill_manager.get_skill_names()
    print(f"      Skills antes de limpiar: {len(skills_antes)}")

    skill_manager.clear_registry()

    skills_despues_limpiar = skill_manager.get_skill_names()
    print(f"      Skills después de limpiar: {len(skills_despues_limpiar)}")

    # 2. Construir ruta de carpeta de skills del producto
    producto_path = os.path.join(SKILLS_BASE_PATH, producto)
    print(f"   📂 Buscando skills en: {producto_path}")

    # 3. Verificar que existe la carpeta
    if not os.path.exists(producto_path):
        print(f"      ❌ ERROR: Carpeta no encontrada")
        return False

    # 4. Cargar skills de la carpeta
    try:
        skill_manager.load_skills.from_folder(producto_path)
    except Exception as e:
        print(f"      ❌ ERROR al cargar skills: {e}")
        return False

    # 5. Verificar que se cargaron skills
    skills_cargadas = skill_manager.get_skill_names()
    print(f"   ✓ Skills cargadas: {len(skills_cargadas)}")

    if len(skills_cargadas) > 0:
        print(f"      📋 Lista de skills:")
        for skill_name in skills_cargadas:
            print(f"         - {skill_name}")
        return True
    else:
        print(f"      ⚠️  ADVERTENCIA: No se encontraron skills en la carpeta")
        return False


# ==================== SOLUCIÓN 3: PROCESAMIENTO ====================

def procesar_tickets():
    """
    Procesa todos los tickets cambiando las skills dinámicamente.
    """

    # Crear el agente (se reutiliza, solo cambian las skills)
    agente = InstantNeo(
        api_key=API_KEY,
        provider=PROVIDER,
        model=GROQ_MODEL,
        temperature=0.3
    )

    # Procesar cada ticket
    for ticket in tickets:
        print(f"\n{'='*70}")
        print(f"📋 TICKET: {ticket['id']} - {ticket['producto']}")
        print(f"🔴 PRIORIDAD: {ticket['prioridad']}")
        print(f"{'='*70}")
        print(f"📝 Problema:")
        print(f"   {ticket['problema']}")
        print()

        # 1. Detectar el tipo de producto
        producto_detectado = detectar_producto(ticket['problema'])
        print(f"🔍 Producto detectado: {producto_detectado.upper()}")

        if producto_detectado == "desconocido":
            print("   ⚠️  No se pudo detectar el tipo de producto")
            print("   💡 Procesando con skills genéricas...")
            continue

        # 2. Cargar skills del producto
        print(f"\n🔧 Cargando skills específicas de {producto_detectado.upper()}...")
        skills_cargadas = cargar_skills_producto(agente.skill_manager, producto_detectado)

        if not skills_cargadas:
            print("   ❌ No se pudieron cargar las skills")
            continue

        # 3. Ejecutar el agente con el problema
        print(f"\n🤖 Ejecutando agente...")
        print(f"{'─'*70}")

        try:
            respuesta = agente.run(
                f"""Eres un agente de soporte técnico especializado en {producto_detectado.upper()}.

Ticket: {ticket['id']}
Problema: {ticket['problema']}

INSTRUCCIONES:
1. Usa las skills disponibles para diagnosticar el problema
2. Proporciona un análisis detallado
3. Sugiere soluciones concretas

Procede con el diagnóstico usando tus herramientas."""
            )

            # 4. Mostrar respuesta
            print(f"\n💬 RESPUESTA DEL AGENTE:")
            print(f"{'─'*70}")
            print(respuesta)
            print(f"{'─'*70}")

        except Exception as e:
            print(f"❌ ERROR al ejecutar agente: {e}")

        print(f"\n✓ Ticket {ticket['id']} procesado")


# ==================== BONUS: MODO ADMIN ====================

def modo_admin():
    """
    BONUS: Modo "admin" que carga TODAS las skills de todos los productos.
    Útil para problemas complejos que involucran múltiples sistemas.
    """

    print("\n" + "="*70)
    print("👑 MODO ADMIN: CARGANDO TODAS LAS SKILLS")
    print("="*70)

    # Crear agente
    agente = InstantNeo(
        api_key=API_KEY,
        provider=PROVIDER,
        model=GROQ_MODEL,
        temperature=0.3
    )

    # Limpiar registry
    agente.skill_manager.clear_registry()
    print("🧹 Registry limpiado\n")

    # Cargar skills de todos los productos
    productos = ["api", "webapp", "mobile"]
    total_skills = 0

    for producto in productos:
        producto_path = os.path.join(SKILLS_BASE_PATH, producto)
        if os.path.exists(producto_path):
            print(f"📂 Cargando skills de {producto.upper()}...")
            try:
                agente.skill_manager.load_skills.from_folder(producto_path)
                skills = [s for s in agente.skill_manager.get_skill_names() if s not in agente.skill_manager.get_skill_names()]
                print(f"   ✓ Skills cargadas de {producto}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

    # Mostrar todas las skills cargadas
    all_skills = agente.skill_manager.get_skill_names()
    print(f"\n📋 TOTAL DE SKILLS DISPONIBLES: {len(all_skills)}")
    print("─" * 70)
    for skill_name in all_skills:
        print(f"   • {skill_name}")
    print("─" * 70)

    # Ticket complejo que requiere múltiples tipos de skills
    ticket_complejo = """
    PROBLEMA CRÍTICO END-TO-END:

    Tenemos un incidente que afecta toda la plataforma:

    1. API BACKEND:
       - El endpoint /api/productos está devolviendo status 503
       - Los logs muestran timeouts y errores de conexión

    2. FRONTEND WEB:
       - La página muestra errores de JavaScript al intentar renderizar productos
       - El HTML tiene problemas de estructura que empeoran el problema

    3. APP MÓVIL:
       - La aplicación Android crashea al intentar cargar la lista de productos
       - Stack trace indica problemas de memoria y permisos de red

    Necesito un diagnóstico completo de los 3 sistemas y un plan de acción.
    """

    print(f"\n🔥 PROCESANDO TICKET CRÍTICO MULTI-SISTEMA...")
    print("─" * 70)

    try:
        respuesta = agente.run(
            f"""Eres un SENIOR TECHNICAL LEAD con acceso a herramientas de debugging
de TODOS los sistemas (API, WebApp, Mobile).

{ticket_complejo}

INSTRUCCIONES:
1. Usa tus skills de API para diagnosticar el backend
2. Usa tus skills de WebApp para analizar el frontend
3. Usa tus skills de Mobile para investigar el crash de la app
4. Proporciona un plan de acción coordinado para resolver todo

Procede con el diagnóstico completo usando TODAS tus herramientas disponibles."""
        )

        print(f"\n💬 ANÁLISIS COMPLETO DEL SENIOR TECH LEAD:")
        print("=" * 70)
        print(respuesta)
        print("=" * 70)

    except Exception as e:
        print(f"❌ ERROR: {e}")

    print(f"\n✓ Modo admin completado")


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """
    Función principal que ejecuta el ejercicio completo.
    """

    print("="*70)
    print("EJERCICIO 04 - SOLUCIÓN: SISTEMA DE SOPORTE MULTI-PRODUCTO")
    print("="*70)

    # Verificar que existe la carpeta de skills
    if not os.path.exists(SKILLS_BASE_PATH):
        print(f"\n❌ ERROR: No se encuentra la carpeta de skills en:")
        print(f"   {SKILLS_BASE_PATH}")
        print(f"\n📝 INSTRUCCIONES:")
        print(f"   1. Asegúrate de que la carpeta 'skills' existe")
        print(f"   2. Debe tener subcarpetas: api/, webapp/, mobile/")
        print(f"   3. Cada subcarpeta debe tener archivos .py con skills decoradas")
        return

    print(f"\n✓ Carpeta de skills encontrada: {SKILLS_BASE_PATH}")

    # Mostrar estructura de skills disponibles
    print(f"\n📁 ESTRUCTURA DE SKILLS:")
    for producto in ["api", "webapp", "mobile"]:
        producto_path = os.path.join(SKILLS_BASE_PATH, producto)
        if os.path.exists(producto_path):
            archivos = [f for f in os.listdir(producto_path) if f.endswith('.py') and f != '__init__.py']
            print(f"   📂 {producto}/")
            for archivo in archivos:
                print(f"      └─ {archivo}")
        else:
            print(f"   ⚠️  {producto}/ - NO ENCONTRADA")

    print(f"\n🎯 INICIANDO PROCESAMIENTO DE {len(tickets)} TICKETS...\n")

    # Procesar tickets normales
    procesar_tickets()

    # BONUS: Modo admin
    print("\n\n")
    respuesta_admin = input("¿Quieres probar el MODO ADMIN? (s/n): ").lower()
    if respuesta_admin == 's':
        modo_admin()

    print("\n" + "="*70)
    print("✅ EJERCICIO COMPLETADO CON ÉXITO")
    print("="*70)
    print("""
CONCEPTOS APRENDIDOS:
✓ Detección dinámica de contexto
✓ Carga/descarga de skills según necesidad
✓ Uso de clear_registry() para limpiar skills
✓ Uso de load_skills.from_folder() para carga dinámica
✓ Agentes multi-modo que adaptan sus capacidades
✓ Gestión eficiente de recursos (solo cargar lo necesario)

APLICACIONES REALES:
- Chatbots multi-dominio (ventas, soporte, RRHH)
- Asistentes especializados por contexto
- Sistemas de debugging inteligentes
- Agentes que escalan según demanda
- Plataformas multi-tenant con capacidades por cliente
    """)


if __name__ == "__main__":
    main()


"""
NOTAS SOBRE LA IMPLEMENTACIÓN:

1. DETECCIÓN DE PRODUCTO:
   - Usa sistema de scoring con palabras clave
   - Fácil de extender con más categorías
   - Se puede mejorar usando embeddings o clasificación con IA

2. CARGA DINÁMICA:
   - clear_registry() asegura estado limpio
   - from_folder() carga automáticamente todas las skills de una carpeta
   - Manejo robusto de errores

3. PROCESAMIENTO:
   - Un solo agente que se reconfigura dinámicamente
   - Más eficiente que crear múltiples agentes
   - Fácil de extender con más productos

4. MODO ADMIN:
   - Útil para problemas complejos multi-sistema
   - Demuestra el poder de combinar múltiples dominios
   - Trade-off: más capacidades = más tokens en prompt

5. MEJORAS POSIBLES:
   - Cache de skills por producto
   - Lazy loading de skills pesadas
   - Métricas de uso de skills
   - Versionado de skills
   - Hot-reload de skills sin reiniciar
   - A/B testing de diferentes sets de skills

6. PRODUCCIÓN:
   - Agregar logging de qué skills se cargan/usan
   - Timeout por si una skill se cuelga
   - Rate limiting por tipo de skill
   - Monitoreo de performance por producto
   - Feature flags para habilitar/deshabilitar skills
"""
