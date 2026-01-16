# 🎓 PUCP - Asistente de Normativa y Permanencia Estudiantil

Chatbot inteligente diseñado para ayudar a estudiantes universitarios a navegar la normativa académica y encontrar soluciones para evitar la deserción estudiantil.

## 📋 Descripción

Este asistente utiliza **LangChain** y **LangGraph** con modelos de Google Generative AI para:

- Analizar la situación académica del estudiante
- Buscar opciones normativas como amnistías, rectificaciones de matrícula, justificaciones de inasistencia
- Proporcionar orientación basada en reglamentos vigentes
- Sugerir alternativas como reserva de matrícula o licencias

## 🛠️ Tecnologías

- **Python 3.12**
- **LangChain / LangGraph** - Orquestación de agentes
- **Google Generative AI** - Modelo de lenguaje
- **Azure Cognitive Search** - Base de conocimientos
- **FastAPI** - API REST (opcional)
- **Pipenv** - Gestión de dependencias

## ⚙️ Configuración

### 1. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Modelo de IA
MODEL_API_KEY=tu_api_key_de_google
MODEL_TEMPERATURE=0.7

# Azure Search (Base de Conocimientos)
AZURE_SEARCH_SERVICE_NAME=tu_servicio
AZURE_SEARCH_API_KEY=tu_api_key
AZURE_SEARCH_INDEX_NAME=tu_indice
AZURE_SEARCH_TOP_K=5

# Azure Form Recognizer
AZURE_FORM_SERVICE_NAME=tu_servicio
AZURE_FORM_API_KEY=tu_api_key
```

### 2. Instalación de Dependencias

```bash
# Instalar pipenv (si no lo tienes)
pip install pipenv

# Activar entorno virtual
pipenv shell

# Instalar dependencias
pipenv install
```

## 🚀 Ejecución

### Modo Script (Recomendado)

Ejecuta el chatbot directamente en la terminal:

```bash
pipenv run dev
```

**Comandos disponibles:**

- `salir` - Terminar la conversación
- `nuevo` - Iniciar una nueva conversación

### Modo API (FastAPI)

Para ejecutar como servidor REST:

```bash
pipenv run start
```

La API estará disponible en `http://127.0.0.1:8000`

**Endpoints:**

- `GET /` - Health check
- `POST /agente` - Enviar mensaje al agente

## 📁 Estructura del Proyecto

```text
PUCP/
├── main.py              # Script principal (modo consola)
├── Pipfile              # Dependencias del proyecto
├── pyproject.toml       # Configuración de herramientas
├── .env                 # Variables de entorno (crear)
└── app/
    ├── app.py           # Aplicación FastAPI
    ├── sync.py          # Sincronización
    ├── agents/          # Definición de agentes
    ├── core/            # Configuración, LLM, checkpointer
    ├── flow/            # Flujo del agente tutor
    ├── router/          # Rutas de FastAPI
    ├── tools/           # Herramientas (búsqueda en BC)
    └── util/            # Utilidades
```

## 📝 Ejemplo de Uso

```text
============================================================
🎓 Asistente de Normativa y Permanencia Estudiantil - PUCP
============================================================
Escribe 'salir' para terminar la conversación.
Escribe 'nuevo' para iniciar una nueva conversación.
------------------------------------------------------------

Tú: ¿Qué opciones tengo si jalé un curso por tercera vez?

⏳ Procesando...

Agente: Entiendo que esta situación puede ser preocupante...
```
