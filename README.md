# Curso InstantNeo - Construcción de Agentes Inteligentes

Formación intensiva de 3 días sobre construcción de agentes con InstantNeo.

## 📋 Información del Curso

- **Duración:** 3 días
- **Modalidad:** Remota y sincrónica
- **Nivel:** Intermedio (requiere conocimientos de Python)

## 🎯 Objetivos

1. Comprender los fundamentos teóricos de LLMs y agentes inteligentes
2. Dominar InstantNeo para construir agentes desde básicos hasta avanzados
3. Desarrollar proyectos funcionales integrando conceptos aprendidos
4. Prepararse para contribuir a la comunidad InstantNeo

## 📦 Requisitos Previos

### Conocimientos Técnicos

- Python (POO, type hints, decoradores)
- Git básico
- Uso de pip y entornos virtuales
- Conceptos de APIs REST

### Software Necesario

- Python 3.8 o superior
- Git
- Editor de código (VS Code, PyCharm, etc.)
- API Key de OpenAI (se compartirá durante el curso)

## 🚀 Setup del Entorno

### 1. Clonar el Repositorio

```bash
git clone https://github.com/InstantNeo/instantneo-curso.git
cd instantneo-curso
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Linux/Mac
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key de OpenAI
# OPENAI_API_KEY=tu-api-key-aqui
```

### 5. Verificar Instalación

```bash
python -c "from instantneo import InstantNeo; print('✅ InstantNeo instalado correctamente')"
```

## 📚 Estructura del Curso

```
curso-instantneo/
├── dia-1/                              # Fundamentos y Primeros Pasos
│   ├── 00_concepto_agente_basico.py   # ¿Qué es un agente?
│   ├── 01_agente_sin_skills.py        # Primer agente con InstantNeo
│   ├── 02_agente_con_skills.py        # Agente con @skill decorator
│   └── 03_ejercicio_skills_propias.py # Práctica: crear skills
│
├── dia-2/                              # Agentes Avanzados (próximamente)
│   └── ...
│
└── dia-3/                              # Proyecto Final (próximamente)
    └── ...
```

## 📖 Día 1: Fundamentos y Primeros Pasos

### Contenido

1. **Conceptos Fundamentales**

2. **Introducción a InstantNeo**

3. **Práctica con Código**
   
### Ejemplos del Día 1

#### Ejemplo 1: Concepto de Agente
```bash
cd dia-1
python 00_concepto_agente_basico.py
```

Muestra el concepto de agente (Input → Output) llevado al extremo más simple.

#### Ejemplo 2: Primer Agente InstantNeo
```bash
python 01_agente_sin_skills.py
```

Crea un agente básico con InstantNeo y explora sus limitaciones sin skills.

#### Ejemplo 3: Agente con Skills
```bash
python 02_agente_con_skills.py
```

Agrega capacidades al agente usando el decorador `@skill`.

#### Ejemplo 4: Práctica
```bash
python 03_ejercicio_skills_propias.py
```

Template para que crees tus propias skills.

## 🔑 Conceptos Clave

### ¿Qué es un Agente?

En pocas palabras, algo que:
- **Percibe** información del entorno
- **Decide** qué acción tomar
- **Actúa** ejecutando la acción

**NO necesita:**
- Loops complejos
- Memoria persistente
- Interfaces de chat

**Puede ser usado en:**
- APIs REST
- Pipelines de datos
- Sistemas de automatización
- Componentes de software normal

### Filosofía InstantNeo

- **Transparencia:** Ves exactamente qué hace cada componente
- **Simplicidad:** Agentes simples que se combinan
- **Control:** Tú orquestas, no el framework
- **Society of Mind:** La inteligencia emerge de combinar agentes simples

## 🛠️ Comandos Útiles

```bash
# Ver skills disponibles en un agente
python -c "
from instantneo import InstantNeo
agente = InstantNeo(...)
print(agente.get_skill_names())
"
```

## 📝 Recursos Adicionales

- [Documentación InstantNeo](https://github.com/InstantNeo/instantneo)
- [Guía de Skills](https://github.com/InstantNeo/instantneo/blob/main/docs/skills_guide.md)
- [Core Reference](https://github.com/InstantNeo/instantneo/blob/main/docs/core_reference.md)

## 🤝 Contribuir

Después del curso, puedes contribuir a InstantNeo:
- Creando ejemplos y tutoriales
- Reportando bugs
- Sugiriendo mejoras
- Desarrollando nuevas features

## 📧 Soporte

- **Durante el curso:** Canal de Discord
- **Comunidad InstantNeo:** [GitHub Issues](https://github.com/InstantNeo/instantneo/issues)

## 📄 Licencia

Este material del curso está bajo licencia MIT.

---

**¡Bienvenido al mundo de los agentes inteligentes con InstantNeo! 🚀**
