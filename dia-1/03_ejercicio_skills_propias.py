"""
Ejercicio 3.4: Crear Skills Propias

OBJETIVO: Crear 2-3 skills originales y probarlas con un agente

INSTRUCCIONES:
1. Define tus skills usando el decorador @skill
2. Regístralas en el agente
3. Prueba con prompts que requieran esas skills
4. Experimenta con diferentes combinaciones
"""

from instantneo import InstantNeo, skill
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CONFIGURACIÓN
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ Error: No se encontró GROQ_API_KEY en .env")
    exit(1)

# ============================================================
# EJEMPLOS DE SKILLS (puedes usarlas como referencia)
# ============================================================

@skill(description="Convierte texto a mayúsculas")
def a_mayusculas(texto: str) -> str:
    """Convierte un texto a mayúsculas."""
    return texto.upper()


@skill(description="Cuenta las palabras en un texto")
def contar_palabras(texto: str) -> int:
    """Cuenta cuántas palabras hay en un texto."""
    return len(texto.split())


@skill(description="Calcula el factorial de un número")
def factorial(n: int) -> int:
    """
    Calcula el factorial de n.

    Args:
        n: Número entero positivo

    Returns:
        El factorial de n (n!)
    """
    if n == 0 or n == 1:
        return 1
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


@skill(
    description="Crea un archivo de texto con contenido dado",
    parameters={
        "nombre_archivo": "Nombre del archivo a crear (ej: 'notas.txt')",
        "contenido": "Contenido a escribir en el archivo"
    }
)
def crear_archivo(nombre_archivo: str, contenido: str) -> str:
    """Crea un archivo de texto con el contenido especificado."""
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    return f"Archivo '{nombre_archivo}' creado exitosamente."


# ============================================================
# 🎯 TU TURNO: Define tus propias skills aquí
# ============================================================

# Ejemplo 1: Skill de conversión
# @skill(description="Tu descripción aquí")
# def tu_skill_1(parametro: tipo) -> tipo_retorno:
#     """Tu docstring aquí"""
#     # Tu código aquí
#     pass

# Ejemplo 2: Skill de procesamiento
# @skill(description="Tu descripción aquí")
# def tu_skill_2(parametro: tipo) -> tipo_retorno:
#     """Tu docstring aquí"""
#     # Tu código aquí
#     pass

# Ejemplo 3: Skill creativa
# @skill(description="Tu descripción aquí")
# def tu_skill_3(parametro: tipo) -> tipo_retorno:
#     """Tu docstring aquí"""
#     # Tu código aquí
#     pass


# ============================================================
# IDEAS PARA SKILLS (elige algunas o crea las tuyas)
# ============================================================

# 🔢 Matemáticas:
# - dividir(a, b) - División con manejo de división por cero
# - potencia(base, exponente) - Calcular base^exponente
# - es_primo(n) - Verificar si un número es primo

# 📝 Texto:
# - invertir_texto(texto) - Invertir un string
# - a_minusculas(texto) - Convertir a minúsculas
# - contar_vocales(texto) - Contar vocales en un texto
# - extraer_numeros(texto) - Extraer todos los números de un texto

# 📁 Archivos:
# - leer_archivo(nombre) - Leer contenido de un archivo
# - listar_archivos() - Listar archivos en el directorio actual
# - eliminar_archivo(nombre) - Eliminar un archivo

# 🔧 Utilidades:
# - timestamp_actual() - Obtener fecha y hora actual
# - generar_id() - Generar un ID único
# - validar_email(email) - Validar formato de email

# 🌐 Datos:
# - parsear_json(json_string) - Parsear un string JSON
# - lista_a_dict(keys, values) - Convertir listas a diccionario
# - filtrar_pares(lista) - Filtrar números pares de una lista


# ============================================================
# CREAR AGENTE Y PROBAR
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EJERCICIO: Crear Skills Propias")
    print("=" * 70)

    # Crear agente con las skills de ejemplo
    agente = InstantNeo(
        provider="groq",
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-20b",
        role_setup="Eres un asistente versátil. Usa tus tools cuando sea necesario.",
        skills=[
            a_mayusculas,
            contar_palabras,
            factorial,
            crear_archivo
        ]
    )

    print("\n✅ Agente creado con skills de ejemplo:")
    print(f"   Skills disponibles: {agente.get_skill_names()}\n")

    # ============================================================
    # PRUEBAS CON LAS SKILLS DE EJEMPLO
    # ============================================================

    print("🧪 Probando skills de ejemplo:\n")

    # Test 1: Conversión a mayúsculas
    print("1️⃣ Test: Convertir a mayúsculas")
    resultado1 = agente.run("Convierte 'hola mundo' a mayúsculas")
    print(f"   Resultado: {resultado1}\n")

    # Test 2: Contar palabras
    print("2️⃣ Test: Contar palabras")
    resultado2 = agente.run("Cuántas palabras hay en 'InstantNeo es una librería para agentes'")
    print(f"   Resultado: {resultado2}\n")

    # Test 3: Factorial
    print("3️⃣ Test: Calcular factorial")
    resultado3 = agente.run("Calcula el factorial de 6")
    print(f"   Resultado: {resultado3}\n")

    # Test 4: Crear archivo
    print("4️⃣ Test: Crear archivo")
    resultado4 = agente.run("Crea un archivo llamado 'test.txt' con el contenido 'Hola desde InstantNeo'")
    print(f"   Resultado: {resultado4}\n")

    # Test 5: Sin relación a una skill
    # Ejemplo de invertir en bolsa

    # ============================================================
    # 🎯 AHORA TU TURNO
    # ============================================================

    print("=" * 70)
    print("🎯 TU TURNO:")
    print("=" * 70)
    print("1. Define 2-3 skills propias arriba (descomenta los ejemplos)")
    print("2. Regístralas en el agente usando:")
    print("   agente.register_skill(tu_skill_1)")
    print("   agente.register_skill(tu_skill_2)")
    print("3. Pruébalas con agente.run('tu prompt aquí')")
    print("4. Comparte tu skill más interesante en el chat del curso!")
    print("=" * 70)

    # ============================================================
    # REGISTRAR TUS SKILLS AQUÍ
    # ============================================================

    # Ejemplo de cómo registrar tus skills:
    # agente.register_skill(tu_skill_1)
    # agente.register_skill(tu_skill_2)
    # agente.register_skill(tu_skill_3)

    # print("\n✨ Skills agregadas:")
    # print(f"   Skills disponibles: {agente.get_skill_names()}\n")

    # ============================================================
    # PROBAR TUS SKILLS AQUÍ
    # ============================================================

    # Ejemplo de cómo probar tus skills:
    # print("🧪 Probando mis skills:\n")
    # resultado_tuyo = agente.run("tu prompt aquí")
    # print(f"Resultado: {resultado_tuyo}")

    print("\n💡 TIPS:")
    print("  - Usa type hints (int, str, bool, etc.) para mejor funcionamiento")
    print("  - Escribe docstrings claros - el LLM los usa para entender la skill")
    print("  - Maneja errores y logs dentro de tus skills (try/except)")
    print("  - Piensa en casos de uso reales (APIs, procesamiento, validación)")
    print("=" * 70)
