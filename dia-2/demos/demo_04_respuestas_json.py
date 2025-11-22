"""
Demo 04: Respuestas en formato JSON
====================================

Este demo muestra cómo configurar InstantNeo para retornar respuestas
en formato JSON válido, facilitando la integración con sistemas externos,
APIs y procesos ETL.

Casos de uso:
- Extracción de datos estructurados
- Integración con APIs REST
- Procesos ETL (Extract, Transform, Load)
- Generación de configuraciones
"""

import os
import json
from dotenv import load_dotenv
from instantneo import InstantNeo

# Cargar variables de entorno
load_dotenv()

# ============================================================
# CONFIGURACIÓN DEL MODELO
# ============================================================

# Modelo a utilizar en demos (configurable desde .env)
# Usa un modelo más liviano para demos rápidas
LLAMA_8B_MODEL = os.getenv("LLAMA_8B_MODEL", "llama-3.1-8b-instant")  # Default: modelo rápido

print(f"🔧 Modelo configurado: {LLAMA_8B_MODEL}")

def demo_json_simple():
    """
    Caso 1: JSON simple
    -------------------
    Solicitar al agente que extraiga información de texto
    y la retorne como JSON simple (objeto plano).
    """
    print("\n" + "="*60)
    print("CASO 1: JSON SIMPLE - Extracción de información de producto")
    print("="*60)

    # Inicializar agente con Groq
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        temperature=0.1,  # Baja temperatura para respuestas más consistentes
        role_setup="""Eres un extractor de datos especializado en convertir descripciones de productos en JSON válido."""
    )

    # Input de ejemplo: descripción de producto en texto natural
    input_texto = "Laptop Dell XPS 15 de 15.6 pulgadas con procesador Intel i7, 16GB RAM, 512GB SSD, precio $1200, disponible en stock."

    # Prompt que solicita JSON específico
    prompt = f"""
Extrae la información del siguiente producto y retorna ÚNICAMENTE un JSON válido
con esta estructura exacta:
{{
    "nombre": "nombre del producto",
    "precio": precio_numerico,
    "disponible": true/false
}}

Producto: {input_texto}

IMPORTANTE: Retorna solo el JSON, sin texto adicional, sin markdown, sin ```json.
"""

    print(f"\nInput: {input_texto}")
    print("\nSolicitando JSON al agente...")

    try:
        # Ejecutar agente
        respuesta = agente.run(prompt)
        print(f"\nRespuesta raw del agente:\n{respuesta}")

        # Intentar parsear el JSON
        datos = json.loads(respuesta)
        print("\nJSON parseado exitosamente:")
        print(json.dumps(datos, indent=2, ensure_ascii=False))

        # Usar los datos en código Python
        print("\nUsando los datos extraídos:")
        print(f"  - Nombre: {datos['nombre']}")
        print(f"  - Precio: ${datos['precio']}")
        print(f"  - Disponible: {'Sí' if datos['disponible'] else 'No'}")


    except json.JSONDecodeError as e:
        print(f"\nERROR: No se pudo parsear el JSON")
        print(f"Detalle: {e}")
        print("Tip: Asegúrate de que el agente retorne SOLO JSON, sin texto adicional")
    except KeyError as e:
        print(f"\nERROR: Falta una clave esperada en el JSON: {e}")
    except Exception as e:
        print(f"\nERROR inesperado: {e}")


def demo_json_anidado():
    """
    Caso 2: JSON anidado
    --------------------
    Solicitar una estructura JSON más compleja con objetos
    anidados y arrays.
    """
    print("\n" + "="*60)
    print("CASO 2: JSON ANIDADO - Múltiples productos")
    print("="*60)

    # Inicializar agente
    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        temperature=0.1,
        role_setup="""Eres un extractor de datos especializado en convertir inventarios de productos en JSON válido con estructuras anidadas."""
    )

    # Input con múltiples productos
    input_texto = """
    Inventario de electrónica:
    1. Laptop Dell XPS 15 - $1200 - 5 unidades
    2. Mouse Logitech MX Master - $99 - 20 unidades
    3. Teclado mecánico Corsair - $150 - 0 unidades
    """

    # Prompt que solicita JSON anidado
    prompt = f"""
Extrae el inventario y retorna ÚNICAMENTE un JSON válido con esta estructura:
{{
    "inventario": [
        {{
            "id": numero_secuencial,
            "nombre": "nombre del producto",
            "precio": precio_numerico,
            "stock": {{
                "cantidad": numero_unidades,
                "disponible": true/false
            }}
        }}
    ],
    "total_productos": numero_total,
    "total_disponibles": numero_disponibles
}}

Datos: {input_texto}

IMPORTANTE: Retorna solo el JSON, sin texto adicional, sin markdown, sin ```json.
"""

    print(f"\nInput:\n{input_texto}")
    print("\nSolicitando JSON anidado al agente...")

    try:
        # Ejecutar agente
        respuesta = agente.run(prompt)
        print(f"\nRespuesta raw del agente:\n{respuesta}")

        # Intentar parsear el JSON
        datos = json.loads(respuesta)
        print("\nJSON parseado exitosamente:")
        print(json.dumps(datos, indent=2, ensure_ascii=False))

        # Usar los datos en código Python
        print("\n" + "-"*60)
        print("ANÁLISIS DEL INVENTARIO")
        print("-"*60)

        for producto in datos['inventario']:
            print(f"\nProducto #{producto['id']}: {producto['nombre']}")
            print(f"  Precio: ${producto['precio']}")
            print(f"  Stock: {producto['stock']['cantidad']} unidades")
            print(f"  Estado: {'Disponible' if producto['stock']['disponible'] else 'Agotado'}")

        print(f"\n{'='*60}")
        print(f"Total de productos: {datos['total_productos']}")
        print(f"Productos disponibles: {datos['total_disponibles']}")

        # Ejemplo de uso real: calcular valor total del inventario
        valor_total = sum(
            p['precio'] * p['stock']['cantidad']
            for p in datos['inventario']
        )
        print(f"Valor total del inventario: ${valor_total:,.2f}")

    except json.JSONDecodeError as e:
        print(f"\nERROR: No se pudo parsear el JSON")
        print(f"Detalle: {e}")
    except KeyError as e:
        print(f"\nERROR: Falta una clave esperada en el JSON: {e}")
    except Exception as e:
        print(f"\nERROR inesperado: {e}")


def demo_uso_real_api():
    """
    Caso 3: Ejemplo de uso real - Integración con API
    --------------------------------------------------
    Simula cómo los JSONs generados se usarían para
    llamar a una API REST.
    """
    print("\n" + "="*60)
    print("CASO 3: USO REAL - Integración con API REST")
    print("="*60)

    agente = InstantNeo(
        provider="groq",
        api_key=os.getenv("GROQ_API_KEY"),
        model=LLAMA_8B_MODEL,
        temperature=0.1,
        role_setup="""Eres un extractor de datos especializado en convertir facturas en JSON valide."""
    )

    # Descripción en lenguaje natural de una orden de compra
    descripcion = """
    Cliente: Juan Pérez
    Email: juan@example.com
    Productos:
    - 2 Laptops Dell XPS a $1200 cada una
    - 1 Mouse Logitech a $99
    Método de pago: Tarjeta de crédito
    Dirección de envío: Calle Principal 123, Ciudad, CP 12345
    """

    prompt = f"""
Convierte esta orden de compra en un JSON válido para enviar a una API REST:
{{
    "cliente": {{
        "nombre": "nombre completo",
        "email": "email"
    }},
    "items": [
        {{
            "producto": "nombre",
            "cantidad": numero,
            "precio_unitario": numero
        }}
    ],
    "metodo_pago": "metodo",
    "envio": {{
        "direccion": "direccion completa",
        "codigo_postal": "cp"
    }},
    "total": total_calculado
}}

Orden: {descripcion}

IMPORTANTE: Retorna solo el JSON, sin texto adicional.
"""

    print(f"\nDescripción de la orden:\n{descripcion}")
    print("\nGenerando JSON para API...")

    try:
        respuesta = agente.run(prompt)
        orden_json = json.loads(respuesta)

        print("\nJSON generado para la API:")
        print(json.dumps(orden_json, indent=2, ensure_ascii=False))

        # Simulación de llamada a API
        print("\n" + "-"*60)
        print("SIMULACIÓN DE LLAMADA A API")
        print("-"*60)
        print("POST https://api.tienda.com/v1/ordenes")
        print(f"Content-Type: application/json")
        print(f"\nBody:\n{json.dumps(orden_json, indent=2, ensure_ascii=False)}")

        # En un caso real, haríamos:
        # import requests
        # response = requests.post(
        #     "https://api.tienda.com/v1/ordenes",
        #     json=orden_json,
        #     headers={"Authorization": "Bearer TOKEN"}
        # )

        # Ejemplo de "enriquecimiento" de la respuesta, tomando los valores unitarios y cantidades del JSON generado para calcular el total de la orden y compararlo con el total calculado por el agente. Si el total es diferente, se ajusta el total en el JSON antes de enviarlo a la API.
        total_calculado = sum(
            item['cantidad'] * item['precio_unitario']
            for item in orden_json['items']
        )
        if total_calculado != orden_json['total']:
            print(f"\n[AVISO] El total calculado (${total_calculado}) no coincide con el total proporcionado (${orden_json['total']}). Ajustando el total en el JSON.")
            orden_json['total'] = total_calculado
        

        print("\n[Simulación] Respuesta de la API:")
        print('{"status": "success", "order_id": "ORD-12345", "message": "Orden creada exitosamente"}')

    except Exception as e:
        print(f"\nERROR: {e}")


def main():
    """
    Ejecuta todas las demos de respuestas JSON
    """
    print("\n" + "="*60)
    print("DEMO 04: RESPUESTAS EN FORMATO JSON")
    print("="*60)
    print("\nEste demo muestra cómo obtener respuestas estructuradas")
    print("en formato JSON para integración con sistemas externos.")

    # Ejecutar demos
    demo_json_simple()
    demo_json_anidado()
    demo_uso_real_api()

    print("\n" + "="*60)
    print("CONCLUSIONES")
    print("="*60)
    print("""
1. Usar temperatura baja (0.1-0.3) para respuestas JSON consistentes
2. Ser explícito en el prompt: "retorna SOLO JSON, sin texto adicional"
3. Siempre usar try/except para manejar JSONDecodeError
4. Validar que el JSON tiene las claves esperadas
5. Los JSONs generados son directamente usables en:
   - Llamadas a APIs REST
   - Procesos ETL
   - Bases de datos
   - Sistemas de integración
    """)


if __name__ == "__main__":
    main()
