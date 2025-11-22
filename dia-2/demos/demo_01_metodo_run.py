"""
Demo 01: Método run() - Uso Básico de InstantNeo
=================================================

Conceptos clave:
- Uso básico del método run()
- Diferencia entre parámetros en constructor vs run()
- El prompt como única entrada necesaria
- Independencia entre llamadas (sin contexto compartido)
- Comparación visual de diferentes configuraciones

Autor: Curso InstantNeo - Día 2
"""

import os
from dotenv import load_dotenv
from instantneo import InstantNeo
from instantneo import skill

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar en demos (configurable desde .env)
# Usa un modelo más liviano para demos rápidas
LLAMA_8B_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.1-8b-instant")  # Default: modelo rápido
VISION_MODEL = os.getenv("LLAMA_SCOUT_MODEL", "llama-3.1-8b-vision-instant")  # Default: modelo con visión

print(f"🔧 Modelo configurado: {LLAMA_8B_MODEL}")

def separador(titulo):
    """Imprime un separador visual con título."""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def demo_basico():
    """Ejemplo 1: Uso básico del método run()"""
    separador("EJEMPLO 1: Uso Básico de run()")

    # Crear agente con configuración básica
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un asistente conciso y directo.",
        temperature=0.7,
        max_tokens=100
    )

    print("Configuración del agente:")
    print(f"  - Provider: groq")
    print(f"  - Modelo: {LLAMA_8B_MODEL}")
    print(f"  - Temperature: 0.7")
    print(f"  - Max tokens: 100")
    print(f"  - Role: Asistente conciso y directo\n")

    # Llamada simple con solo el prompt
    prompt = "¿Qué es Python en una frase?"
    print(f"Prompt: {prompt}\n")
    print("Respuesta:")

    respuesta = agente.run(prompt=prompt)
    print(f"  {respuesta}\n")


def demo_parametros_constructor_vs_run():
    """Ejemplo 2: Parámetros en constructor vs run()"""
    separador("EJEMPLO 2: Constructor vs Run - Sobrescritura de Parámetros")

    # Crear agente con temperatura baja (más determinista)
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un poeta creativo.",
        temperature=0.2,  # Baja creatividad por defecto
        max_tokens=80
    )

    prompt = "Escribe un verso sobre el mar."

    # Primera llamada: usa los parámetros del constructor
    print("LLAMADA 1 - Usando parámetros del constructor:")
    print(f"  Temperature: 0.2 (baja creatividad)")
    print(f"  Max tokens: 80")
    print(f"  Prompt: {prompt}\n")

    respuesta1 = agente.run(prompt=prompt)
    print(f"Respuesta: {respuesta1}\n")

    # Segunda llamada: sobrescribe parámetros en run()
    print("\nLLAMADA 2 - Sobrescribiendo parámetros en run():")
    print(f"  Temperature: 1.5 (alta creatividad)")
    print(f"  Max tokens: 150")
    print(f"  Role setup: Poeta épico y dramático")
    print(f"  Prompt: {prompt}\n")

    respuesta2 = agente.run(
        prompt=prompt,
        temperature=1,  # Sobrescribe: alta creatividad
        max_tokens=150,   # Sobrescribe: más tokens
        role_setup="Eres un poeta épico y dramático."  # Sobrescribe role
    )
    print(f"Respuesta: {respuesta2}\n")

    print("\nObservación: Los parámetros en run() tienen prioridad sobre")
    print("los del constructor, permitiendo flexibilidad por llamada.")


def demo_independencia_llamadas():
    """Ejemplo 3: Independencia entre llamadas"""
    separador("EJEMPLO 3: Independencia de Llamadas (Sin Contexto)")

    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un asistente que responde concisamente.",
        max_tokens=100
    )

    print("Las llamadas a run() son INDEPENDIENTES entre sí.")
    print("El agente NO recuerda información de llamadas anteriores.\n")

    # Llamada 1: Establecer un dato
    print("LLAMADA 1:")
    prompt1 = "Mi color favorito es el azul."
    print(f"  Usuario: {prompt1}")
    respuesta1 = agente.run(prompt=prompt1)
    print(f"  Agente: {respuesta1}\n")

    # Llamada 2: Otro dato independiente
    print("LLAMADA 2:")
    prompt2 = "Mi animal favorito es el gato."
    print(f"  Usuario: {prompt2}")
    respuesta2 = agente.run(prompt=prompt2)
    print(f"  Agente: {respuesta2}\n")

    # Llamada 3: Intentar recordar datos anteriores
    print("LLAMADA 3:")
    prompt3 = "¿Cuál es mi color favorito y mi animal favorito?"
    print(f"  Usuario: {prompt3}")
    respuesta3 = agente.run(prompt=prompt3)
    print(f"  Agente: {respuesta3}\n")

    print("⚠️  RESULTADO: El agente NO recuerda las llamadas anteriores.")
    print("    Cada llamada a run() es completamente independiente.")
    print("    En el siguiente demo veremos cómo gestionar contexto.\n")


def demo_procesamiento_datos():
    """Ejemplo 4: El prompt como entrada para procesar datos"""
    separador("EJEMPLO 4: Procesamiento de Datos con Prompt")

    # Simular datos de un archivo o lista
    datos_productos = [
        {"nombre": "Laptop", "precio": 1200, "stock": 5},
        {"nombre": "Mouse", "precio": 25, "stock": 50},
        {"nombre": "Teclado", "precio": 75, "stock": 30}
    ]

    print("Datos de productos:")
    for producto in datos_productos:
        print(f"  - {producto['nombre']}: ${producto['precio']} (Stock: {producto['stock']})")
    print()

    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un analista de datos que genera resúmenes concisos.",
        max_tokens=150
    )

    # Construir prompt con los datos
    prompt = f"""Analiza estos productos y proporciona un resumen ejecutivo:

Productos:
{datos_productos}

Genera un resumen que incluya:
- Total de productos
- Valor total del inventario
- Producto más caro
- Producto con mayor stock"""

    print("Enviando datos al agente para análisis...\n")
    print("Respuesta del agente:")

    respuesta = agente.run(prompt=prompt)
    print(f"{respuesta}\n")

    print("💡 LECCIÓN: El prompt puede incluir datos estructurados")
    print("    (listas, diccionarios, texto de archivos, etc.)")


def demo_execution_modes():
    """
    EJEMPLO 5: Modos de Ejecución (execution_mode)

    InstantNeo tiene 3 modos para controlar cómo se ejecutan las skills:
    - wait_response: Ejecuta y espera resultado (default)
    - get_args: Solo extrae argumentos, NO ejecuta (para planning)
    - execution_only: Fire-and-forget, ejecuta en background
    """
    separador("EJEMPLO 5: Modos de Ejecución (execution_mode)")

    # Definir skill de ejemplo
    @skill(description="Suma dos números")
    def sumar(a: int, b: int) -> int:
        print(f"    [EJECUTANDO] Sumando {a} + {b}...")
        return a + b

    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un asistente matemático."
    )
    agente.register_skill(sumar)

    prompt = "Suma 15 y 27"

    print("\n1. MODO: wait_response (default)")
    print("   Ejecuta la skill y espera el resultado")
    resultado = agente.run(prompt, execution_mode="wait_response")
    print(f"   Resultado: {resultado}\n")

    print("2. MODO: get_args")
    print("   Extrae argumentos pero NO ejecuta la skill")
    args = agente.run(prompt, execution_mode="get_args")
    print(f"   Argumentos extraídos: {args}")
    print("   Nota: La función NO se ejecutó\n")

    print("3. MODO: execution_only")
    print("   Ejecuta la skill en background sin esperar")
    resultado = agente.run(prompt, execution_mode="execution_only")
    print(f"   Resultado: {resultado}\n")

    print("💡 Uso:")
    print("   - wait_response: Uso normal")
    print("   - get_args: Planning, validación, tool chaining")
    print("   - execution_only: Fire-and-forget (logging, notificaciones)")


def demo_skills_parameter():
    """
    EJEMPLO 6: Parámetro 'skills' - Filtrado Temporal

    Permite usar solo un subset de skills para un run específico,
    sin modificar el SkillManager del agente.
    """
    separador("EJEMPLO 6: Parámetro 'skills' - Filtrado Temporal")

    @skill(description="Suma dos números")
    def sumar(a: int, b: int) -> int:
        return a + b

    @skill(description="Multiplica dos números")
    def multiplicar(a: int, b: int) -> int:
        return a * b

    @skill(description="Envía un email")
    def enviar_email(destinatario: str, mensaje: str) -> str:
        return f"Email enviado a {destinatario}"

    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="Eres un asistente general."
    )

    agente.register_skill(sumar)
    agente.register_skill(multiplicar)
    agente.register_skill(enviar_email)

    print(f"Skills registradas: {agente.get_skill_names()}\n")

    print("1. Usando SOLO skills matemáticas (filtrado temporal)")
    print("   skills=['sumar', 'multiplicar']")
    resultado = agente.run(
        prompt="Calcula 5 + 3",
        skills=["sumar", "multiplicar"]
    )
    print(f"   Resultado: {resultado}\n")

    print("2. Usando TODAS las skills (default)")
    resultado = agente.run(
        prompt="Envía email a juan@example.com diciendo Hola"
    )
    print(f"   Resultado: {resultado}\n")

    print("💡 Útil para:")
    print("   - Restringir capabilities por contexto")
    print("   - Testing de skills específicas")
    print("   - Control fino por usuario/rol")


def demo_vision():
    """
    EJEMPLO 8: Análisis de Imágenes con Visión (Multimodal)

    Groq soporta modelos multimodales (llama-3.2-90b-vision-preview)
    que pueden analizar imágenes y responder preguntas sobre ellas.
    """
    separador("EJEMPLO 8: Análisis de Imágenes (Visión)")

    # Buscar imagen de factura en el directorio
    import glob
    imagenes = glob.glob("*.jpg") + glob.glob("*.png")

    if not imagenes:
        print("⚠️  No se encontraron imágenes (.jpg o .png) en el directorio actual")
        print("    Saltando demo de visión...")
        return

    imagen_path = imagenes[0]
    print(f"📷 Imagen encontrada: {imagen_path}\n")

    # Crear agente con modelo de visión
    agente_vision = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=VISION_MODEL,  # Modelo con capacidad de visión
        role_setup="Eres un asistente que analiza imágenes con precisión.",
        temperature=0.3,
        max_tokens=200
    )

    print("Configuración del agente con visión:")
    print(f"  - Modelo: llama-3.2-90b-vision-preview")
    print(f"  - Capacidad: Visión multimodal")
    print(f"  - Temperature: 0.3\n")

    # Analizar la imagen
    print("Analizando imagen...\n")

    respuesta = agente_vision.run(
        prompt="Describe brevemente qué ves en esta imagen.",
        images=imagen_path  # Puede ser path local o URL
    )

    print("Análisis de la imagen:")
    print("-" * 70)
    print(respuesta)
    print("-" * 70)

    print("\n💡 Uso del parámetro 'images':")
    print("   - Acepta path local: './factura.jpg'")
    print("   - Acepta URL: 'https://ejemplo.com/imagen.jpg'")
    print("   - Acepta lista: ['img1.jpg', 'img2.jpg']")
    print("   - Requiere modelo con capacidad de visión")
    print("   - Groq: llama-3.2-90b-vision-preview")


def comentarios_otros_parametros():
    """
    OTROS PARÁMETROS DISPONIBLES (no demostrados, pero útiles)

    1. return_full_response (bool):
       - Retorna objeto completo del provider (con metadata)
       - Útil para: debugging, tracking de tokens, acceso a usage
       - Ejemplo: response = agente.run("test", return_full_response=True)
                  tokens_usados = response.usage.total_tokens

    2. async_execution (bool):
       - Ejecuta múltiples skills en paralelo (async/await)
       - Mejora performance cuando hay múltiples skill calls
       - Se combina con execution_mode

    3. image_detail (str):
       - Control de detalle en procesamiento de imágenes
       - Opciones: "auto", "low", "high"
       - Solo aplicable con parámetro 'images'

    4. seed (int):
       - Para reproducibilidad de respuestas
       - Mismo seed + misma temp = misma respuesta

    5. stop (str | List[str]):
       - Secuencias de parada para la generación
       - Ejemplo: stop=[",", "."] detiene en coma o punto

    6. presence_penalty / frequency_penalty (float):
       - Control fino de generación (-2.0 a 2.0)
       - presence: penaliza palabras ya usadas
       - frequency: penaliza palabras frecuentes

    7. tool_choice (str | dict):
       - Control sobre cuándo usar skills
       - Opciones: "auto", "none", "required", o skill específica

    Para más detalles, consulta la documentación de InstantNeo.
    """
    pass


if __name__ == "__main__":
    print("="*70)
    print("DEMO COMPLETA: Método run() de InstantNeo")
    print("="*70)

    # Verificar API key
    if not os.getenv("GROQ_API_KEY"):
        print("\n⚠️  ERROR: GROQ_API_KEY no encontrada en .env")
        print("    Por favor, configura tu API key en el archivo .env")
        exit(1)

    # Ejecutar demos existentes
    demo_basico()
    demo_parametros_constructor_vs_run()
    demo_independencia_llamadas()
    demo_procesamiento_datos()

    # Nuevas demos
    demo_execution_modes()       # CRÍTICO
    demo_skills_parameter()      # CRÍTICO
    demo_vision()                # IMPORTANTE - Visión multimodal

    # Comentarios sobre otros parámetros
    print("\n" + "="*70)
    print("OTROS PARÁMETROS DISPONIBLES")
    print("="*70)
    print(comentarios_otros_parametros.__doc__)

    print("\n" + "#"*70)
    print("  FIN DEL DEMO 01")
    print("#"*70 + "\n")
