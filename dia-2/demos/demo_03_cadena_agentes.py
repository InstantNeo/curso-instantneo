"""
Demo 03: Cadena de Agentes - Pipeline de Procesamiento con Visión
==================================================================

Conceptos clave:
- Pipeline de múltiples agentes especializados
- Flujo de datos: salida de un agente → entrada del siguiente
- Cada agente tiene un rol y tarea específica
- NO es un chatbot, es procesamiento de datos en pipeline
- Caso de uso: Procesamiento automatizado de facturas
- NUEVO: Agente con visión para leer facturas escaneadas

Pipeline:
    Imagen Factura → [Lector OCR] → Texto Natural → [Conversor JSON] → Datos JSON →
    [Clasificador] → Categoría + Prioridad → [Generador] → Resumen

Autor: Curso InstantNeo - Día 2
"""

import os
import json
from dotenv import load_dotenv
from pathlib import Path
import sys
# from instantneo import InstantNeo
instantneo_path = Path(__file__).parent.parent.parent / "instantneo"
sys.path.insert(0, str(instantneo_path))

from instantneo import InstantNeo
# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar en demos (configurable desde .env)
# Usa un modelo más liviano para demos rápidas
LLAMA_8B_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.1-8b-instant")  # Default: modelo rápido
VISION_MODEL = os.getenv("LLAMA_SCOUT_MODEL", "llama-3.2-11b-vision-preview")  # Modelo con visión
print(f"🔧 Modelo configurado: {LLAMA_8B_MODEL}")


def separador(titulo):
    """Imprime un separador visual con título."""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def log_agente(nombre_agente, etiqueta, contenido, color="azul"):
    """
    Logger visual para mostrar el flujo del pipeline.

    Args:
        nombre_agente (str): Nombre del agente
        etiqueta (str): INPUT, OUTPUT, PROCESSING
        contenido (str): Contenido a mostrar
        color (str): Color visual (solo decorativo)
    """
    colores = {
        "azul": "🔵",
        "verde": "🟢",
        "amarillo": "🟡",
        "rojo": "🔴"
    }

    icono = colores.get(color, "⚪")

    if etiqueta == "INPUT":
        print(f"{icono} [{nombre_agente}] ← INPUT:")
        print(f"   {contenido}")
    elif etiqueta == "OUTPUT":
        print(f"{icono} [{nombre_agente}] → OUTPUT:")
        print(f"   {contenido}")
    elif etiqueta == "PROCESSING":
        print(f"{icono} [{nombre_agente}] ⚙️  PROCESANDO...")

    print()


def crear_agente_lector_ocr():
    """
    Agente 1: LECTOR OCR (con Visión)
    Lee una imagen de factura y extrae el texto visible.
    Usa modelo multimodal con capacidad de visión.
    """
    return InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=VISION_MODEL,  # Modelo con visión
        role_setup="""Eres un lector OCR especializado en documentos de facturas.
Tu tarea es leer la imagen y extraer TODO el texto visible en lenguaje natural.
Describe la información exactamente como la ves, sin formatear a JSON.
Solo extrae el texto visible, no inventes información.""",
        temperature=0.1,  # Muy determinista para OCR
        max_tokens=500
    )


def crear_agente_conversor_json():
    """
    Agente 2: CONVERSOR A JSON
    Convierte texto natural de factura a formato JSON estructurado.
    """
    return InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="""Eres un conversor de texto a JSON especializado en facturas.
Tu tarea es tomar texto de factura y convertirlo a JSON válido.
Debes extraer: numero_factura, empresa, monto (solo número), fecha, items (una lista con nombre y cantidad).
Responde SOLO con JSON válido, sin explicaciones adicionales.""",
        temperature=0.1,  # Muy determinista para conversión
        max_tokens=200
    )


def crear_agente_clasificador():
    """
    Agente 2: CLASIFICADOR
    Clasifica la factura según monto y empresa.
    """
    return InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="""Eres un clasificador de facturas.
Debes clasificar la factura en:
- CATEGORÍA: 'suministros', 'servicios', 'productos', u 'otros'
- PRIORIDAD: 'alta' (>$3000), 'media' ($1000-$3000), 'baja' (<$1000)
Responde SOLO con JSON válido con las claves 'categoria' y 'prioridad'.""",
        temperature=0.1,
        max_tokens=150
    )


def crear_agente_generador():
    """
    Agente 3: GENERADOR
    Genera un resumen ejecutivo de la factura procesada.
    """
    return InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        role_setup="""Eres un generador de resúmenes ejecutivos para facturas.
Debes crear un resumen profesional y conciso que incluya:
- Información principal de la factura
- Categorización y prioridad
- Recomendaciones de acción si aplica
Usa un tono formal y directo.""",
        temperature=0.5,  # Un poco más creativo para el resumen
        max_tokens=300
    )


def procesar_factura_pipeline(imagen_factura_path=None):
    """
    Pipeline completo de procesamiento de factura con visión.

    Args:
        imagen_factura_path (str): Path a imagen de factura (si None, busca en directorio)

    Returns:
        dict: Resultado final del pipeline con todos los datos procesados
    """
    separador("INICIO DEL PIPELINE DE PROCESAMIENTO CON VISIÓN")

    # Buscar imagen si no se proporciona
    if imagen_factura_path is None:
        import glob
        imagenes = glob.glob("*.jpg") + glob.glob("*.png")
        if imagenes:
            imagen_factura_path = imagenes[0]
        else:
            print("⚠️  No se encontró imagen de factura. Usando texto de ejemplo...")
            return procesar_factura_texto_ejemplo()

    print(f"📷 IMAGEN DE FACTURA: {imagen_factura_path}")
    print(f"Iniciando procesamiento en 4 etapas...\n")

    # ========================================
    # ETAPA 1: LECTURA OCR (con Visión)
    # ========================================
    separador("ETAPA 1: LECTOR OCR (Visión)")

    agente_ocr = crear_agente_lector_ocr()
    log_agente("LECTOR_OCR", "INPUT", f"Imagen: {imagen_factura_path}", "azul")
    log_agente("LECTOR_OCR", "PROCESSING", "", "azul")

    prompt_ocr = """Lee esta imagen de factura y extrae TODO el texto visible.
Describe exactamente lo que ves, en lenguaje natural.
No formatees a JSON, solo extrae el texto."""

    texto_factura = agente_ocr.run(
        prompt=prompt_ocr,
        images=imagen_factura_path
    )
    log_agente("LECTOR_OCR", "OUTPUT", texto_factura, "azul")

    # ========================================
    # ETAPA 2: CONVERSIÓN A JSON
    # ========================================
    separador("ETAPA 2: CONVERSOR A JSON")

    agente_conversor = crear_agente_conversor_json()
    log_agente("CONVERSOR_JSON", "INPUT", texto_factura, "verde")
    log_agente("CONVERSOR_JSON", "PROCESSING", "", "verde")

    prompt_conversor = f"""Convierte este texto de factura a JSON con:
- numero_factura
- empresa
- monto (solo el número)
- fecha
- items (una lista con nombre y cantidad)

Texto de factura:
{texto_factura}

JSON:"""

    datos_json = agente_conversor.run(prompt=prompt_conversor)
    log_agente("CONVERSOR_JSON", "OUTPUT", datos_json, "verde")

    # Intentar parsear el JSON
    try:
        datos_extraidos = json.loads(datos_json)
    except json.JSONDecodeError:
        # Si falla, intentar extraer el JSON del texto
        import re
        json_match = re.search(r'\{.*\}', datos_json, re.DOTALL)
        if json_match:
            datos_extraidos = json.loads(json_match.group())
        else:
            datos_extraidos = {"error": "No se pudo parsear JSON"}

    # ========================================
    # ETAPA 3: CLASIFICACIÓN
    # ========================================
    separador("ETAPA 3: CLASIFICADOR")

    agente_clasificador = crear_agente_clasificador()

    input_clasificador = f"Datos de factura: {json.dumps(datos_extraidos, indent=2)}"
    log_agente("CLASIFICADOR", "INPUT", input_clasificador, "amarillo")
    log_agente("CLASIFICADOR", "PROCESSING", "", "amarillo")

    prompt_clasificador = f"""Clasifica esta factura:

{json.dumps(datos_extraidos, indent=2)}

Retorna JSON con:
- categoria: 'suministros', 'servicios', 'productos', u 'otros'
- prioridad: 'alta', 'media' o 'baja'

JSON:"""

    clasificacion_json = agente_clasificador.run(prompt=prompt_clasificador)
    log_agente("CLASIFICADOR", "OUTPUT", clasificacion_json, "amarillo")

    # Parsear clasificación
    try:
        clasificacion = json.loads(clasificacion_json)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{.*\}', clasificacion_json, re.DOTALL)
        if json_match:
            clasificacion = json.loads(json_match.group())
        else:
            clasificacion = {"categoria": "otros", "prioridad": "media"}

    # Combinar datos
    datos_completos = {
        **datos_extraidos,
        **clasificacion
    }

    # ========================================
    # ETAPA 4: GENERACIÓN DE RESUMEN
    # ========================================
    separador("ETAPA 4: GENERADOR DE RESUMEN")

    agente_generador = crear_agente_generador()

    input_generador = f"Datos completos: {json.dumps(datos_completos, indent=2)}"
    log_agente("GENERADOR", "INPUT", input_generador, "rojo")
    log_agente("GENERADOR", "PROCESSING", "", "rojo")

    prompt_generador = f"""Genera un resumen ejecutivo de esta factura procesada:

{json.dumps(datos_completos, indent=2)}

El resumen debe incluir:
1. Datos principales (empresa, monto, fecha)
2. Clasificación (categoría y prioridad)
3. Recomendaciones de acción

Resumen:"""

    resumen_final = agente_generador.run(prompt=prompt_generador)
    log_agente("GENERADOR", "OUTPUT", resumen_final, "rojo")

    # ========================================
    # RESULTADO FINAL
    # ========================================
    separador("RESULTADO FINAL DEL PIPELINE")

    resultado = {
        "imagen_original": imagen_factura_path,
        "texto_extraido": texto_factura,
        "datos_extraidos": datos_extraidos,
        "clasificacion": clasificacion,
        "resumen_ejecutivo": resumen_final
    }

    print("📊 DATOS ESTRUCTURADOS:")
    print(json.dumps({
        "datos_extraidos": datos_extraidos,
        "clasificacion": clasificacion
    }, indent=2, ensure_ascii=False))

    print(f"\n📝 RESUMEN EJECUTIVO:")
    print(f"{resumen_final}")

    return resultado


def procesar_factura_texto_ejemplo():
    """
    Función de fallback para procesar facturas desde texto
    cuando no hay imagen disponible.
    """
    separador("MODO FALLBACK: Procesamiento desde Texto")
    print("⚠️  No se encontró imagen. Usando ejemplo de texto.\n")

    texto_ejemplo = "Factura #123, Acme Corp, $5000, 15-01-2024"
    print(f"📄 TEXTO DE EJEMPLO: {texto_ejemplo}\n")

    # Crear agente conversor para procesar directamente
    agente_conversor = crear_agente_conversor_json()

    prompt = f"""Convierte este texto de factura a JSON con:
- numero_factura
- empresa
- monto (solo el número)
- fecha

Texto: {texto_ejemplo}

JSON:"""

    datos_json = agente_conversor.run(prompt=prompt)

    try:
        datos_extraidos = json.loads(datos_json)
    except:
        import re
        json_match = re.search(r'\{.*\}', datos_json, re.DOTALL)
        datos_extraidos = json.loads(json_match.group()) if json_match else {}

    # Continuar con clasificación
    agente_clasificador = crear_agente_clasificador()
    prompt_clasificador = f"""Clasifica esta factura:
{json.dumps(datos_extraidos, indent=2)}

Retorna JSON con categoria y prioridad.
JSON:"""

    clasificacion_json = agente_clasificador.run(prompt=prompt_clasificador)

    try:
        clasificacion = json.loads(clasificacion_json)
    except:
        import re
        json_match = re.search(r'\{.*\}', clasificacion_json, re.DOTALL)
        clasificacion = json.loads(json_match.group()) if json_match else {"categoria": "otros", "prioridad": "media"}

    # Generar resumen
    datos_completos = {**datos_extraidos, **clasificacion}
    agente_generador = crear_agente_generador()

    prompt_generador = f"""Genera un resumen ejecutivo de esta factura:
{json.dumps(datos_completos, indent=2)}

Resumen:"""

    resumen_final = agente_generador.run(prompt=prompt_generador)

    print("📊 RESULTADO:")
    print(json.dumps(datos_completos, indent=2, ensure_ascii=False))
    print(f"\n📝 RESUMEN:\n{resumen_final}\n")

    return {
        "texto_original": texto_ejemplo,
        "datos_extraidos": datos_extraidos,
        "clasificacion": clasificacion,
        "resumen_ejecutivo": resumen_final
    }


def visualizar_arquitectura():
    """Muestra la arquitectura del pipeline"""
    separador("ARQUITECTURA DEL PIPELINE CON VISIÓN")

    print("""
    ┌─────────────────────────────────────────────────────────────────┐
    │             PIPELINE DE PROCESAMIENTO CON VISIÓN                │
    └─────────────────────────────────────────────────────────────────┘

                          ┌─────────────────┐
                          │ Imagen Factura  │
                          │   (JPG/PNG)     │
                          └────────┬────────┘
                                   │
                                   ▼
                    ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
                    ┃ AGENTE 1: LECTOR OCR   ┃
                    ┃ Model: vision-preview  ┃
                    ┃ Temp: 0.1 (preciso)    ┃
                    ┗━━━━━━━━━┬━━━━━━━━━━━━━━┛
                              │
                              ▼
                    ┌─────────────────┐
                    │ Texto Natural   │
                    │ Extraído OCR    │
                    └────────┬────────┘
                             │
                             ▼
                    ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
                    ┃ AGENTE 2: CONVERSOR    ┃
                    ┃ Role: Text → JSON      ┃
                    ┃ Temp: 0.1 (preciso)    ┃
                    ┗━━━━━━━━━┬━━━━━━━━━━━━━━┛
                              │
                              ▼
                    ┌─────────────────┐
                    │  Datos JSON     │
                    │  Estructurados  │
                    └────────┬────────┘
                             │
                             ▼
                    ┏━━━━━━━━━━━━━━━━━━━━━━━┓
                    ┃  AGENTE 3: CLASIFICADOR┃
                    ┃  Role: Clasificador    ┃
                    ┃  Temp: 0.1 (preciso)   ┃
                    ┗━━━━━━━━━┬━━━━━━━━━━━━━━┛
                              │
                              ▼
                    ┌─────────────────┐
                    │  Categoría +    │
                    │  Prioridad      │
                    └────────┬────────┘
                             │
                             ▼
                    ┏━━━━━━━━━━━━━━━━━━━━━━━┓
                    ┃  AGENTE 4: GENERADOR   ┃
                    ┃  Role: Generador       ┃
                    ┃  Temp: 0.5 (creativo)  ┃
                    ┗━━━━━━━━━┬━━━━━━━━━━━━━━┛
                              │
                              ▼
                    ┌─────────────────┐
                    │ Resumen Final   │
                    │ Ejecutivo       │
                    └─────────────────┘

    CARACTERÍSTICAS:
    • 4 agentes especializados en el pipeline
    • Agente con visión para leer imágenes (OCR)
    • Separación clara: OCR → Conversión → Clasificación → Resumen
    • Cada agente es especialista en UNA tarea
    • Flujo unidireccional de datos
    • Salida de uno = Entrada del siguiente
    • No hay conversación, solo transformación de datos
    • Ideal para procesamiento automatizado y batch
    """)


if __name__ == "__main__":
    print("\n" + "#"*70)
    print("  DEMO 03: Cadena de Agentes - Pipeline con Visión")
    print("#"*70)

    # Verificar API key
    if not os.getenv("GROQ_API_KEY"):
        print("\n⚠️  ERROR: GROQ_API_KEY no encontrada en .env")
        print("    Por favor, configura tu API key en el archivo .env")
        exit(1)

    # Mostrar arquitectura
    visualizar_arquitectura()

    # Procesar factura desde imagen
    print("\n" + "="*70)
    print("  PROCESAMIENTO DE FACTURA CON PIPELINE DE 4 AGENTES")
    print("="*70)

    procesar_factura_pipeline('./1744405478112-72f86cda-8607-4af5-8d06-fd10fb064da6.jpg')  # Auto-detecta imagen o usa fallback

    print("\n" + "#"*70)
    print("  FIN DEL DEMO 03")
    print("#"*70 + "\n")

    print("💡 LECCIONES CLAVE:")
    print("   1. NUEVO: Agente con visión para leer imágenes de facturas (OCR)")
    print("   2. Pipeline de 4 agentes: OCR → Conversor → Clasificador → Generador")
    print("   3. Cada agente tiene un rol y tarea específica")
    print("   4. Los agentes se encadenan: salida → entrada")
    print("   5. NO es conversacional, es procesamiento de datos")
    print("   6. Ideal para automatización y procesamiento en lote")
    print("   7. Diferentes temperatures según la tarea (0.1 vs 0.5)\n")
