"""
Demo 05: SkillManager - Teoría y Operaciones
=============================================

Este demo explora en profundidad el SkillManager de InstantNeo:
- Filosofía: agentes auto-modificables y extensibles
- Relación InstantNeo ↔ SkillManager
- Métodos principales de gestión de skills
- Carga dinámica con SkillLoader
- Operaciones de conjunto entre SkillManagers

Visión: El SkillManager permite crear agentes que pueden:
- Aprender nuevas habilidades en runtime
- Compartir skills entre agentes
- Combinar capacidades de múltiples fuentes
- Auto-modificarse según contexto
"""

import os
from dotenv import load_dotenv
from instantneo import InstantNeo
from instantneo.skills import skill, SkillManager
from instantneo.skills.skill_manager_operations import SkillManagerOperations

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar en demos (configurable desde .env)
# Usa un modelo más liviano para demos rápidas
LLAMA_8B_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.1-8b-instant")  # Default: modelo rápido

print(f"🔧 Modelo configurado: {LLAMA_8B_MODEL}")


# ============================================================================
# FUNCIÓN AUXILIAR - SEPARADOR
# ============================================================================

def separador(titulo):
    """Imprime un separador visual para las secciones"""
    print("\n" + "="*70)
    print(titulo)
    print("="*70)


# ============================================================================
# DEFINICIÓN DE SKILLS DE EJEMPLO
# ============================================================================

@skill(
    name="calcular_area_circulo",
    description="Calcula el área de un círculo dado su radio",
    tags=["matematicas", "geometria"]
)
def calcular_area_circulo(radio: float) -> float:
    """
    Calcula el área de un círculo.

    Args:
        radio: Radio del círculo en unidades

    Returns:
        Área del círculo
    """
    import math
    return math.pi * radio ** 2


@skill(
    name="calcular_area_rectangulo",
    description="Calcula el área de un rectángulo",
    tags=["matematicas", "geometria"]
)
def calcular_area_rectangulo(base: float, altura: float) -> float:
    """
    Calcula el área de un rectángulo.

    Args:
        base: Base del rectángulo
        altura: Altura del rectángulo

    Returns:
        Área del rectángulo
    """
    return base * altura


@skill(
    name="convertir_celsius_fahrenheit",
    description="Convierte temperatura de Celsius a Fahrenheit",
    tags=["conversiones", "temperatura"]
)
def convertir_celsius_fahrenheit(celsius: float) -> float:
    """
    Convierte temperatura de Celsius a Fahrenheit.

    Args:
        celsius: Temperatura en grados Celsius

    Returns:
        Temperatura en Fahrenheit
    """
    return (celsius * 9/5) + 32


@skill(
    name="convertir_metros_pies",
    description="Convierte metros a pies",
    tags=["conversiones", "distancia"]
)
def convertir_metros_pies(metros: float) -> float:
    """
    Convierte metros a pies.

    Args:
        metros: Distancia en metros

    Returns:
        Distancia en pies
    """
    return metros * 3.28084


@skill(
    name="obtener_resumen_texto",
    description="Genera un resumen de un texto",
    tags=["texto", "nlp"]
)
def obtener_resumen_texto(texto: str, max_palabras: int = 50) -> str:
    """
    Genera un resumen simplificado de un texto.

    Args:
        texto: Texto a resumir
        max_palabras: Máximo número de palabras en el resumen

    Returns:
        Resumen del texto
    """
    palabras = texto.split()
    if len(palabras) <= max_palabras:
        return texto
    return " ".join(palabras[:max_palabras]) + "..."


# ============================================================================
# PARTE 1: FILOSOFÍA DEL SKILLMANAGER
# ============================================================================

def parte_1_filosofia():
    """
    Filosofía del SkillManager
    --------------------------
    El SkillManager es el componente que permite crear agentes
    verdaderamente extensibles y auto-modificables.

    Visión: Agentes que pueden:
    1. Aprender nuevas habilidades en runtime
    2. Desactivar habilidades no necesarias
    3. Compartir skills entre agentes
    4. Combinar capacidades de múltiples fuentes
    """
    print("\n" + "="*70)
    print("PARTE 1: FILOSOFÍA DEL SKILLMANAGER")
    print("="*70)

    print("""
El SkillManager gestiona las habilidades (skills) de un agente InstantNeo.:
Un agente complejo es una sociedad de agentes simples (skills)
- Cada skill es una capacidad específica
- El agente combina skills para resolver problemas complejos

Ventajas:
1. MODULARIDAD: Skills independientes y reutilizables
2. EXTENSIBILIDAD: Agregar/quitar skills en runtime
3. COMPARTIR: Múltiples agentes pueden usar los mismos skills
4. COMPOSICIÓN: Combinar skills de diferentes fuentes
5. ESPECIALIZACIÓN: Crear agentes expertos en dominios específicos
    """)


# ============================================================================
# PARTE 2: RELACIÓN INSTANTNEO ↔ SKILLMANAGER
# ============================================================================

def parte_2_relacion():
    """
    Relación InstantNeo ↔ SkillManager
    -----------------------------------
    Todo InstantNeo tiene un SkillManager interno accesible
    mediante agente.skill_manager
    """
    print("\n" + "="*70)
    print("PARTE 2: RELACIÓN INSTANTNEO ↔ SKILLMANAGER")
    print("="*70)

    # Crear un agente InstantNeo
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="""Eres un asistente inteligente capaz de utilizar skills para resolver tareas variadas."""
    )

    print("\n1. Todo InstantNeo tiene un SkillManager:")
    print(f"   agente.skill_manager: {agente.skill_manager}")
    print(f"   Tipo: {type(agente.skill_manager)}")

    # Acceder al SkillManager
    sm = agente.skill_manager

    print("\n2. El SkillManager está inicialmente vacío:")
    print(f"   Skills registrados: {sm.get_skill_names()}")

    # Registrar un skill directamente
    sm.register_skill(calcular_area_circulo)

    print("\n3. Podemos registrar skills directamente:")
    print(f"   Skills registrados: {sm.get_skill_names()}")

    print("\n4. Formas de trabajar con skills:")
    print("   a) Registrar en el SkillManager del agente")
    print("   b) Crear un SkillManager separado y pasarlo al agente")
    print("   c) Usar SkillLoader para carga dinámica")


# ============================================================================
# PARTE 3: MÉTODOS PRINCIPALES
# ============================================================================

def parte_3_metodos_principales():
    """
    Métodos principales del SkillManager
    ------------------------------------
    - register_skill(): Registrar un skill
    - get_skill_names(): Obtener nombres de skills
    - remove_skill(): Eliminar un skill
    - get_skills_by_tag(): Filtrar por tags
    """
    print("\n" + "="*70)
    print("PARTE 3: MÉTODOS PRINCIPALES DEL SKILLMANAGER")
    print("="*70)

    # Crear un SkillManager vacío
    sm = SkillManager()

    # 3.1 - register_skill()
    print("\n" + "-"*70)
    print("3.1 - register_skill(): Registrar skills")
    print("-"*70)

    sm.register_skill(calcular_area_circulo)
    sm.register_skill(calcular_area_rectangulo)
    sm.register_skill(convertir_celsius_fahrenheit)

    print(f"Skills registrados: {sm.get_skill_names()}")

    # 3.2 - get_skill_names()
    print("\n" + "-"*70)
    print("3.2 - get_skill_names(): Listar nombres de skills")
    print("-"*70)

    nombres = sm.get_skill_names()
    print(f"Total de skills: {len(nombres)}")
    for nombre in nombres:
        print(f"  - {nombre}")

    # 3.3 - remove_skill()
    print("\n" + "-"*70)
    print("3.3 - remove_skill(): Eliminar un skill")
    print("-"*70)

    print(f"Antes: {sm.get_skill_names()}")
    sm.remove_skill("convertir_celsius_fahrenheit")
    print(f"Después de eliminar 'convertir_celsius_fahrenheit': {sm.get_skill_names()}")

    # 3.4 - get_skills_by_tag()
    print("\n" + "-"*70)
    print("3.4 - get_skills_by_tag(): Filtrar skills por tags")
    print("-"*70)

    # Registrar más skills para demostrar filtrado
    sm.register_skill(convertir_celsius_fahrenheit)
    sm.register_skill(convertir_metros_pies)
    sm.register_skill(obtener_resumen_texto)

    print(f"\nTodos los skills: {sm.get_skill_names()}")

    # Filtrar por tag "matematicas"
    skills_matematicas = sm.get_skills_by_tag("matematicas")
    print(f"\nSkills con tag 'matematicas':")
    for skill_name in skills_matematicas:
        print(f"  - {skill_name}")

    # Filtrar por tag "conversiones"
    skills_conversiones = sm.get_skills_by_tag("conversiones")
    print(f"\nSkills con tag 'conversiones':")
    for skill_name in skills_conversiones:
        print(f"  - {skill_name}")

    # Filtrar por tag "texto"
    skills_texto = sm.get_skills_by_tag("texto")
    print(f"\nSkills con tag 'texto':")
    for skill_name in skills_texto:
        print(f"  - {skill_name}")


# ============================================================================
# PARTE 4: CARGA DINÁMICA CON SKILLLOADER
# ============================================================================

def parte_4_carga_dinamica():
    """
    Carga dinámica con SkillLoader
    -------------------------------
    SkillManager.load_skills proporciona métodos para cargar
    skills de diferentes fuentes:
    - from_file(): Cargar desde un archivo .py
    - from_folder(): Cargar todos los .py de una carpeta
    - from_module(): Cargar desde un módulo Python
    - from_current(): Cargar del módulo actual
    """
    print("\n" + "="*70)
    print("PARTE 4: CARGA DINÁMICA CON SKILLLOADER")
    print("="*70)

    # 4.1 - from_current()
    print("\n" + "-"*70)
    print("4.1 - from_current(): Cargar skills del módulo actual")
    print("-"*70)

    sm = SkillManager()

    # Cargar todos los skills definidos en este archivo
    sm.load_skills.from_current()

    print(f"Skills cargados desde el módulo actual:")
    for nombre in sm.get_skill_names():
        print(f"  - {nombre}")

    # 4.2 - from_folder() con filtrado por tags
    print("\n" + "-"*70)
    print("4.2 - from_folder() con filtrado por tags")
    print("-"*70)

    print("""
Ejemplo de uso (no ejecutado en esta demo):

# Cargar todos los skills de una carpeta
sm = SkillManager()
sm.load_skills.from_folder(
    "C:/ruta/a/carpeta/skills"
)

# Cargar solo skills con ciertos tags
sm_matematicas = SkillManager()
sm_matematicas.load_skills.from_folder(
    "C:/ruta/a/carpeta/skills",
    by_tags=["matematicas"]
)

# Cargar excluyendo ciertos tags
sm_sin_texto = SkillManager()
sm_sin_texto.load_skills.from_folder(
    "C:/ruta/a/carpeta/skills",
    exclude_tags=["texto", "nlp"]
)
    """)

    # 4.3 - from_file()
    print("\n" + "-"*70)
    print("4.3 - from_file(): Cargar skills de un archivo específico")
    print("-"*70)

    print("""
Ejemplo de uso (no ejecutado en esta demo):

sm = SkillManager()
sm.load_skills.from_file(
    "C:/ruta/a/archivo/mis_skills.py"
)
    """)

    # 4.4 - from_module()
    print("\n" + "-"*70)
    print("4.4 - from_module(): Cargar skills de un módulo Python")
    print("-"*70)

    print("""
Ejemplo de uso (no ejecutado en esta demo):

import mi_paquete.skills as skills_module

sm = SkillManager()
sm.load_skills.from_module(skills_module)
    """)


# ============================================================================
# PARTE 5: OPERACIONES DE CONJUNTO
# ============================================================================

def parte_5_operaciones_conjunto():
    """
    Operaciones de conjunto entre SkillManagers
    --------------------------------------------
    - union(): Combinar skills de múltiples managers
    - intersection(): Skills comunes
    - difference(): Skills únicos de un manager
    - symmetric_difference(): Skills únicos de cada manager
    """
    print("\n" + "="*70)
    print("PARTE 5: OPERACIONES DE CONJUNTO")
    print("="*70)

    # Crear dos SkillManagers con diferentes skills
    sm_matematicas = SkillManager()
    sm_matematicas.register_skill(calcular_area_circulo)
    sm_matematicas.register_skill(calcular_area_rectangulo)
    sm_matematicas.register_skill(convertir_celsius_fahrenheit)  # Común

    sm_conversiones = SkillManager()
    sm_conversiones.register_skill(convertir_celsius_fahrenheit)  # Común
    sm_conversiones.register_skill(convertir_metros_pies)
    sm_conversiones.register_skill(obtener_resumen_texto)

    print("\nSkillManager A (matemáticas):")
    print(f"  {sm_matematicas.get_skill_names()}")

    print("\nSkillManager B (conversiones):")
    print(f"  {sm_conversiones.get_skill_names()}")

    # 5.1 - union()
    print("\n" + "-"*70)
    print("5.1 - union(): Combinar todos los skills")
    print("-"*70)

    sm_union = SkillManagerOperations.union(sm_matematicas, sm_conversiones)
    print(f"Union (A ∪ B):")
    print(f"  {sm_union.get_skill_names()}")
    print(f"  Total: {len(sm_union.get_skill_names())} skills únicos")

    # 5.2 - intersection()
    print("\n" + "-"*70)
    print("5.2 - intersection(): Skills comunes")
    print("-"*70)

    sm_interseccion = SkillManagerOperations.intersection(sm_matematicas, sm_conversiones)
    print(f"Intersección (A ∩ B):")
    print(f"  {sm_interseccion.get_skill_names()}")

    # 5.3 - difference()
    print("\n" + "-"*70)
    print("5.3 - difference(): Skills únicos de A")
    print("-"*70)

    sm_diff_a = SkillManagerOperations.difference(sm_matematicas, sm_conversiones)
    print(f"Diferencia (A - B) - Skills solo en matemáticas:")
    print(f"  {sm_diff_a.get_skill_names()}")

    sm_diff_b = SkillManagerOperations.difference(sm_conversiones, sm_matematicas)
    print(f"\nDiferencia (B - A) - Skills solo en conversiones:")
    print(f"  {sm_diff_b.get_skill_names()}")

    # 5.4 - symmetric_difference()
    print("\n" + "-"*70)
    print("5.4 - symmetric_difference(): Skills únicos de cada uno")
    print("-"*70)

    sm_sym_diff = SkillManagerOperations.symmetric_difference(sm_matematicas, sm_conversiones)
    print(f"Diferencia simétrica (A Δ B) - Skills no compartidos:")
    print(f"  {sm_sym_diff.get_skill_names()}")


# ============================================================================
# PARTE 6: EJEMPLO PRÁCTICO COMPLETO
# ============================================================================

def parte_6_ejemplo_practico():
    """
    Ejemplo práctico: Crear agente especializado
    ---------------------------------------------
    Demuestra cómo usar SkillManager para crear un agente
    con skills específicos y probarlo.
    """
    print("\n" + "="*70)
    print("PARTE 6: EJEMPLO PRÁCTICO - AGENTE MATEMÁTICO")
    print("="*70)

    # Crear un SkillManager solo con skills matemáticos
    sm_matematico = SkillManager()
    sm_matematico.register_skill(calcular_area_circulo)
    sm_matematico.register_skill(calcular_area_rectangulo)

    print("\nSkills del agente matemático:")
    for nombre in sm_matematico.get_skill_names():
        print(f"  - {nombre}")

    # Crear un agente con estos skills
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        temperature=0.1,
        role_setup="""Eres un asistente matemático experto en cálculos geométricos y conversiones."""
        #skills=sm_matematico # También se puede hacer así 
    )

    # Asignar el SkillManager al agente
    agente.skill_manager = sm_matematico

    print("\n" + "-"*70)
    print("Probando el agente matemático...")
    print("-"*70)

    # Test 1: Calcular área de círculo
    print("\nTest 1: ¿Cuál es el área de un círculo con radio 5?")
    try:
        respuesta = agente.run(
            "Calcula el área de un círculo con radio 5",
            execution_mode=agente.WAIT_RESPONSE
        )
        print(f"Respuesta: {respuesta}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Calcular área de rectángulo
    print("\nTest 2: ¿Cuál es el área de un rectángulo de 10x8?")
    try:
        respuesta = agente.run(
            "Calcula el área de un rectángulo con base 10 y altura 8",
            execution_mode=agente.WAIT_RESPONSE
        )
        print(f"Respuesta: {respuesta}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "-"*70)
    print("Expandiendo el agente con skills de conversión...")
    print("-"*70)

    # Ahora agregar skills de conversión
    agente.skill_manager.register_skill(convertir_celsius_fahrenheit)
    agente.skill_manager.register_skill(convertir_metros_pies)

    print(f"\nSkills actualizados: {agente.skill_manager.get_skill_names()}")

    # Test 3: Conversión de temperatura
    print("\nTest 3: ¿Cuántos grados Fahrenheit son 25°C?")
    try:
        respuesta = agente.run(
            "Convierte 25 grados Celsius a Fahrenheit",
            execution_mode=agente.WAIT_RESPONSE
        )
        print(f"Respuesta: {respuesta}")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================================
# PARTE 3.5: CONSULTAS AVANZADAS
# ============================================================================

def parte_3_5_consultas_avanzadas():
    """
    PARTE 3.5: CONSULTAS AVANZADAS DEL SKILLMANAGER
    ================================================

    Métodos para consultar el registry de forma avanzada:
    - get_skills_with_keys(): Registry completo con identificadores únicos
    - get_all_skills_metadata(): Metadata de todas las skills
    - get_skills_by_tag(return_keys=True): Filtrado con keys completos
    """
    separador("PARTE 3.5: CONSULTAS AVANZADAS")

    sm = SkillManager()

    # Registrar skills de ejemplo
    @skill(description="Calcula área de círculo", tags=["matematicas", "geometria"])
    def calcular_area_circulo(radio: float) -> float:
        import math
        return math.pi * radio ** 2

    @skill(description="Convierte Celsius a Fahrenheit", tags=["conversiones", "temperatura"])
    def convertir_celsius_fahrenheit(celsius: float) -> float:
        return (celsius * 9/5) + 32

    sm.register_skill(calcular_area_circulo)
    sm.register_skill(convertir_celsius_fahrenheit)

    # 3.5.1 - get_skills_with_keys()
    print("\n3.5.1 - get_skills_with_keys(): Registry con identificadores únicos")
    print("  Este método retorna el registry completo con keys en formato 'module.nombre'")
    skills_dict = sm.get_skills_with_keys()
    for key, func in skills_dict.items():
        print(f"    {key} → {func.__name__}")

    # 3.5.2 - get_all_skills_metadata()
    print("\n3.5.2 - get_all_skills_metadata(): Metadata de todas las skills")
    all_metadata = sm.get_all_skills_metadata()
    for key, meta in all_metadata.items():
        print(f"    {key}:")
        print(f"      Descripción: {meta['description']}")
        print(f"      Tags: {meta['tags']}")

    # 3.5.3 - get_skills_by_tag() con return_keys=True
    print("\n3.5.3 - get_skills_by_tag(return_keys=True)")
    print("  Permite obtener skills por tag con sus keys completos")
    math_skills_dict = sm.get_skills_by_tag("matematicas", return_keys=True)
    print(f"    Skills con tag 'matematicas' (dict con keys):")
    for key in math_skills_dict.keys():
        print(f"      {key}")

    print("\n💡 UTILIDAD:")
    print("   - Operaciones precisas con duplicados")
    print("   - Debugging de conflictos")
    print("   - Migración entre managers")

# ============================================================================
# PARTE 4.5: FILTRADO AVANZADO
# ============================================================================

def parte_4_5_filtrado_avanzado():
    """
    PARTE 4.5: FILTRADO AVANZADO CON SKILLMANAGER
    ==============================================

    SkillManager permite filtrado de skills por tags usando get_skills_by_tag().
    IMPORTANTE: Cuando pasas múltiples tags, se usa lógica AND (debe tener TODOS).
    """
    separador("PARTE 4.5: FILTRADO AVANZADO - by_tags (lógica AND)")

    # Crear SkillManager y registrar skills con diferentes combinaciones de tags
    sm = SkillManager()

    @skill(tags=["math", "geometry", "2d"])
    def area_circulo(radio: float) -> float:
        import math
        return math.pi * radio ** 2

    @skill(tags=["math", "geometry", "3d"])
    def volumen_esfera(radio: float) -> float:
        import math
        return (4/3) * math.pi * radio ** 3

    @skill(tags=["math", "algebra"])
    def resolver_ecuacion(a: float, b: float) -> float:
        return -b / a

    @skill(tags=["text", "formatting"])
    def capitalizar(texto: str) -> str:
        return texto.upper()

    # Registrar todas las skills
    sm.register_skill(area_circulo)
    sm.register_skill(volumen_esfera)
    sm.register_skill(resolver_ecuacion)
    sm.register_skill(capitalizar)

    print("\n1. Todas las skills registradas:")
    print(f"   Total: {sm.get_skill_names()}")

    print("\n2. Filtrar solo skills con tag 'geometry':")
    skills_geo = sm.get_skills_by_tag("geometry")
    print(f"   Geometría: {skills_geo}")
    print("   Nota: Retorna ['area_circulo', 'volumen_esfera']")

    print("\n3. Filtrar solo skills con tag 'math':")
    skills_math = sm.get_skills_by_tag("math")
    print(f"   Matemáticas: {skills_math}")
    print("   Nota: Retorna todas menos 'capitalizar'")

    print("\n4. Filtrar skills de geometría 2D (con tags 'geometry' Y '2d'):")
    print("   Para AND lógico, filtra manualmente:")
    geo_skills = sm.get_skills_by_tag("geometry")
    skills_2d = [name for name in geo_skills if "2d" in sm.get_all_skills_metadata()]
    print(f"   Geometría 2D: {skills_2d}")
    print("   Nota: Solo 'area_circulo' tiene ambos tags")

    print("\n5. Obtener skill específica por nombre:")
    skill_especifica = sm.get_skill_by_name("resolver_ecuacion")
    print(f"   Skill: {skill_especifica.__name__}")
    # print(f"   Metadata: tags={skill_especifica.metadata.get('tags', [])}")

    print("\n💡 CASOS DE USO:")
    print("   - Agentes especializados por dominio (solo skills de 'database')")
    print("   - Deployment selectivo (dev/staging/prod)")
    print("   - Reducir superficie de ataque (seguridad)")
    print("   - Crear sub-managers por categoría")


# ============================================================================
# PARTE 7: TRACKING DE EJECUCIÓN
# ============================================================================

def parte_7_tracking_ejecucion():
    """
    PARTE 7: TRACKING DE EJECUCIÓN
    ===============================

    Cada skill decorada trackea automáticamente su última ejecución.
    Usa contextvars para ser thread-safe.
    """
    separador("PARTE 7: TRACKING DE EJECUCIÓN")

    @skill(description="Calcula impuesto sobre un monto")
    def calcular_impuesto(monto: float, tasa: float) -> float:
        return monto * tasa

    @skill(description="Divide dos números")
    def dividir(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b

    print("\n7.1 - Tracking de ejecución exitosa:")
    resultado = calcular_impuesto(100, 0.16)
    print(f"   Ejecutado: calcular_impuesto(100, 0.16)")
    print(f"   Resultado: {resultado}")

    last_call = calcular_impuesto.get_last_call()
    print(f"\n   get_last_call() retorna dict completo:")
    print(f"     args: {last_call['args']}")
    print(f"     kwargs: {last_call['kwargs']}")
    print(f"     result: {last_call['result']}")
    print(f"     exception: {last_call['exception']}")

    print(f"\n   get_last_result(): {calcular_impuesto.get_last_result()}")
    print(f"   get_last_params(): {calcular_impuesto.get_last_params()}")

    print("\n7.2 - Tracking de excepciones:")
    try:
        dividir(10, 0)
    except ValueError as e:
        print(f"   Excepción capturada: {e}")

    last_call = dividir.get_last_call()
    print(f"\n   get_last_call() después de excepción:")
    print(f"     exception: {last_call['exception']}")
    print(f"     result: {last_call['result']}")

    print("\n💡 CASOS DE USO:")
    print("   - Debugging: Ver qué parámetros causaron un error")
    print("   - Logging: Registrar historial de ejecuciones")
    print("   - Testing: Verificar llamadas correctas")
    print("   - Auditoría: Rastrear uso en producción")


# ============================================================================
# PARTE 8: METADATA PERSONALIZADA
# ============================================================================

def parte_8_metadata_personalizada():
    """
    PARTE 8: METADATA PERSONALIZADA
    ================================

    Puedes agregar cualquier metadata adicional al decorador @skill.
    """
    separador("PARTE 8: METADATA PERSONALIZADA")

    @skill(
        description="Procesa una imagen",
        tags=["vision", "ml"],
        version="2.0",
        # Metadata personalizada:
        requires_gpu=True,
        max_image_size_mb=10,
        supported_formats=["jpg", "png", "webp"],
        examples=[
            {"input": "cat.jpg", "output": ["cat", "whiskers"]},
            {"input": "dog.png", "output": ["dog", "tail"]}
        ],
        complexity_score=8,
        author="Team Vision",
    )
    def detectar_objetos(imagen_path: str) -> list:
        return ["objeto1", "objeto2"]

    sm = SkillManager()
    sm.register_skill(detectar_objetos)

    print("\n8.1 - Metadata estándar:")
    metadata = sm.get_skill_metadata_by_name("detectar_objetos")
    print(f"   Nombre: {metadata['name']}")
    print(f"   Descripción: {metadata['description']}")
    print(f"   Versión: {metadata['version']}")

    print("\n8.2 - Metadata personalizada:")
    print(f"   Requiere GPU: {metadata['requires_gpu']}")
    print(f"   Formatos soportados: {metadata['supported_formats']}")
    print(f"   Tamaño máximo: {metadata['max_image_size_mb']} MB")
    print(f"   Complejidad: {metadata['complexity_score']}/10")
    print(f"   Autor: {metadata['author']}")

    print("\n8.3 - Ejemplos incluidos en metadata:")
    for i, example in enumerate(metadata['examples'], 1):
        print(f"   Ejemplo {i}: {example['input']} → {example['output']}")

    print("\n8.4 - update_skill_metadata() para modificar en runtime:")
    key = list(sm.get_skills_with_keys().keys())[0]
    sm.update_skill_metadata(key, {
        "version": "2.1",
        "performance_improvement": "15% faster"
    })

    updated_meta = sm.get_skill_metadata_by_name("detectar_objetos")
    print(f"   Nueva versión: {updated_meta['version']}")
    print(f"   Mejora: {updated_meta.get('performance_improvement', 'N/A')}")

    print("\n💡 CASOS DE USO:")
    print("   - Documentación rica auto-generada")
    print("   - Validación pre-ejecución (ej: ¿hay GPU?)")
    print("   - Auto-generación de tests desde ejemplos")
    print("   - Estimación de recursos necesarios")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """
    Ejecuta todas las partes del demo
    """
    print("\n" + "="*70)
    print("DEMO 05: SKILLMANAGER - TEORÍA Y OPERACIONES")
    print("="*70)

    parte_1_filosofia()
    parte_2_relacion()
    parte_3_metodos_principales()
    parte_3_5_consultas_avanzadas()
    parte_4_carga_dinamica()
    parte_4_5_filtrado_avanzado()
    parte_5_operaciones_conjunto()
    parte_6_ejemplo_practico()
    parte_7_tracking_ejecucion()
    parte_8_metadata_personalizada()

    print("\n" + "="*70)
    print("CONCLUSIONES")
    print("="*70)
    print("""
1. FILOSOFÍA:
   - Agentes complejos = combinación de skills simples
   - Modular, extensible, reutilizable

2. MÉTODOS PRINCIPALES:
   - register_skill(): Agregar skills
   - remove_skill(): Eliminar skills
   - get_skill_names(): Listar skills
   - get_skills_by_tag(): Filtrar por tags

3. CARGA DINÁMICA (SkillLoader):
   - from_file(): Desde archivo específico
   - from_folder(): Desde carpeta (con filtrado por tags)
   - from_module(): Desde módulo Python
   - from_current(): Desde módulo actual

4. OPERACIONES DE CONJUNTO:
   - union(): Combinar skills
   - intersection(): Skills comunes
   - difference(): Skills únicos
   - symmetric_difference(): No compartidos

5. USO PRÁCTICO:
   - Crear agentes especializados
   - Compartir skills entre agentes
   - Modificar capacidades en runtime
   - Componer agentes complejos
    """)


if __name__ == "__main__":
    main()
