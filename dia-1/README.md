# Día 1: Fundamentos y Primeros Pasos

## 🎯 Objetivos del Día

Al finalizar el Día 1, serás capaz de:

✅ Entender qué son los LLMs y sus limitaciones
✅ Conocer el concepto de agente según Minsky
✅ Comprender la filosofía y arquitectura de InstantNeo
✅ Crear agentes básicos con y sin skills
✅ Usar el decorador `@skill` para extender capacidades

---

## 📂 Archivos del Día 1

### `00_concepto_agente_basico.py`
**Tipo:** Demostración conceptual

Muestra qué es un agente en su forma más simple:
- Input → Output (sin loops, sin memoria)
- Ejemplo: Clasificador de sentimiento
- Contraste: No razona ni aprende.

```bash
python 00_concepto_agente_basico.py
```

**Conceptos clave:**
- Agente = Percibe → Decide → Actúa
- No necesita loops ni memoria
- Puede ser usado en cualquier sistema

---

### `01_agente_sin_skills.py`
**Tipo:** Ejemplo + Experimentación

Primer agente con InstantNeo (sin skills):
- Configuración básica de InstantNeo
- Uso de `role_setup`, `temperature`, `max_tokens`
- Exploración de limitaciones

```bash
python 01_agente_sin_skills.py
```

**Conceptos clave:**
- Clase `InstantNeo` y sus parámetros
- Método `run()` para interactuar
- Limitaciones sin skills (cálculos, información actualizada)

**Experimentación sugerida:**
1. Cambiar `role_setup` (personalidad del agente)
2. Cambiar `temperature` (creatividad)
3. Probar preguntas que requieren herramientas

---

### `02_agente_con_skills.py`
**Tipo:** Ejemplo guiado + Demo con logging

Agente con skills básicas:
- Decorador `@skill`
- Registro de skills

```bash
python 02_agente_con_skills.py
```

**Conceptos clave:**
- El decorador `@skill` hace funciones "visibles" para el LLM
- El LLM decide cuándo y cómo usar cada skill
- Las skills resuelven las limitaciones del LLM solo

**Skills de ejemplo:**
- `sumar(a, b)` - Suma dos números
- `multiplicar(a, b)` - Multiplica dos números

---

### `03_ejercicio_skills_propias.py`
**Tipo:** Ejercicio práctico

Template para crear tus propias skills:
- Ejemplos comentados de skills
- Ideas para implementar
- Área para tu código

```bash
python 03_ejercicio_skills_propias.py
```

**Objetivo:**
Crear 2-3 skills originales y probarlas

**Skills de ejemplo incluidas:**
- `a_mayusculas(texto)` - Convierte texto a mayúsculas
- `contar_palabras(texto)` - Cuenta palabras
- `factorial(n)` - Calcula factorial
- `crear_archivo(nombre, contenido)` - Crea archivo de texto

**Ideas sugeridas:**
- Matemáticas: división, potencia, es_primo
- Texto: invertir, contar vocales, extraer números
- Archivos: leer, listar, eliminar
- Utilidades: timestamp, generar_id, validar_email
- Datos: parsear JSON, filtrar listas

---

## 🔑 Conceptos Clave del Día 1

### LLMs (Large Language Models)

**Capacidades:**
- Comprensión de lenguaje natural
- Generación de texto coherente
- Razonamiento sobre información en contexto

**Limitaciones:**
- ❌ Información estática (solo hasta fecha de entrenamiento)
- ❌ Sin acceso al mundo real (web, archivos, APIs)
- ❌ Alucinaciones (generan info falsa con confianza)
- ❌ Sin feedback en tiempo real

### Agentes (según Minsky)

Un agente es un componente simple que:
1. **Percibe** información
2. **Decide** qué hacer
3. **Actúa** ejecutando la acción

**NO necesita:**
- Loops complejos
- Memoria persistente
- Interfaz de chat

**Puede ser:**
- Un componente en una API
- Parte de un pipeline de datos
- Clasificador, parser, validador, OCR, etc.

### InstantNeo

**Filosofía "Society of Mind":**
- La inteligencia emerge de combinar agentes simples
- Cada agente es especializado
- El sistema se construye componiendo agentes
- La coordinación viene de TU diseño

**Componentes principales:**
- `InstantNeo`: Clase principal del agente
- `@skill`: Decorador para crear capacidades
- `SkillManager`: Registro de skills (veremos en Día 2)

---

## 💻 Código de Referencia

### Crear un Agente Básico

```python
from instantneo import InstantNeo
import os

agente = InstantNeo(
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="openai/gpt-oss-20b",
    role_setup="Eres un asistente amigable.",
    max_tokens=200
)

respuesta = agente.run("¿Qué es un agente?")
print(respuesta)
```

### Crear una Skill

```python
from instantneo import skill

@skill(description="Suma dos números")
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b
```

### Agente con Skills

```python
from instantneo import InstantNeo, skill

@skill(description="Multiplica dos números")
def multiplicar(a: int, b: int) -> int:
    return a * b

agente = InstantNeo(
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="openai/gpt-oss-20b",
    role_setup="Eres un asistente matemático.",
    skills=["multiplicar"]  # Nombres de funciones decoradas
)

resultado = agente.run("¿Cuánto es 25 * 17?")
```

---

## 📝 Tarea Opcional para el Día 2

1. **Lectura:**
   - Revisar [skills_guide.md](https://github.com/InstantNeo/instantneo/blob/main/docs/skills_guide.md)
   - Revisar [core_reference.md](https://github.com/InstantNeo/instantneo/blob/main/docs/core_reference.md)

2. **Experimentación:**
   - Crear 5 skills diferentes (matemáticas, texto, archivos, etc.)
   - Probar un agente con todas ellas
   - Observar qué skills elige el agente según el prompt

3. **Reflexión:**
   - ¿Qué limitaciones encontraste?
   - ¿Qué casos de uso se te ocurren?
   - Anota dudas para la próxima sesión

---

## 🤔 Preguntas Frecuentes

**¿Puedo usar mis propios API keys?**
Sí, puedes usar tus propias API keys. Solo actualiza el archivo `.env`.

**¿InstantNeo funciona con modelos locales?**
Actualmente soporta OpenAI, Anthropic y Groq. Soporte para más provedores está en el roadmap.

**¿Cómo manejo skills asíncronas?**
Las skills pueden ser async. Veremos esto en el Día 2.

**¿Qué pasa si dos skills tienen el mismo nombre?**
Se mantiene la primera registrada y se guarda en duplicados.

**¿Dónde encuentro más ejemplos?**
En el [repositorio de InstantNeo](https://github.com/InstantNeo/instantneo) y la documentación.

---

## 🎓 Próximos Pasos

**Día 2: Agentes Avanzados y Patrones**
- Skills avanzadas y SkillManager
- Modos de ejecución (WAIT_RESPONSE, EXECUTION_ONLY, GET_ARGS)
- Arquitectura multi-agente

---

¡Excelente trabajo completando el Día 1! 🎉
