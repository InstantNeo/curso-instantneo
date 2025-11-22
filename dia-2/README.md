# Día 2: Agentes Avanzados y SkillManager
## 🎯 Objetivos

Al finalizar el Día 2:

✅ Dominar el método `run()` y gestión de contexto
✅ Entender que los agentes NO son chatbots
✅ Construir pipelines y cadenas de agentes
✅ Trabajar con respuestas estructuradas (JSON)
✅ Usar SkillManager para sistemas modulares

---

## 📂 Archivos

```
dia-2/
├── README.md                           # Esta guía
├── 01_ejercicio_contexto.py           # Gestión manual de contexto
├── 02_ejercicio_sistema_datos.py      # Sistema de procesamiento
├── 03_ejercicio_pipeline_etl.py       # Cadena de agentes ETL
├── 04_ejercicio_multiagente_json.py   # Multi-agente con JSON
├── 05_ejercicio_skillmanager_1.py     # SkillManager práctica 1
└── 06_ejercicio_skillmanager_2.py     # SkillManager práctica 2
```

---

## 💡 Conceptos Clave

### Agentes ≠ Chatbots

Los agentes pueden ser componentes en:
- APIs REST
- Pipelines de datos
- Sistemas de automatización
- ETL processes
- Validadores
- Clasificadores
- Parsers

### Gestión de Contexto

InstantNeo NO tiene memoria automática.
El desarrollador gestiona el contexto via el prompt.

### Cadenas de Agentes

Output de Agente A → Input de Agente B
Cada agente es especializado en UNA tarea.

### Respuestas Estructuradas

Agentes pueden retornar JSON para integración programática.

---

## 🔧 Setup

Asegúrate de tener:
- Entorno virtual activado
- `GROQ_API_KEY` en `.env`
- InstantNeo instalado

```bash
cd dia-2
python 01_ejercicio_contexto.py
```
