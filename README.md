
# Agente Inteligente Local para NutriFit Chile 🤖💪

Este repositorio contiene el código fuente para la **Evaluación Parcial N°2** de la asignatura Ingeniería de Soluciones con IA (ISY0101) en Duoc UC. 

El proyecto evoluciona de un simple sistema RAG a un **Agente Funcional 100% local**, capaz de integrar herramientas de consulta, escritura y razonamiento mediante un flujo de trabajo orquestado.

## 🏗️ Arquitectura y Orquestación (Componentes)

El agente fue diseñado priorizando la privacidad de los datos de la empresa y la escalabilidad a costo cero (sin depender de API Keys externas). 

- **Orquestador Central:** `LangGraph` (`create_react_agent`). Se encarga de evaluar la consulta del usuario, decidir qué herramienta utilizar y mantener el ciclo de razonamiento.
- **Motor LLM:** `Ollama` ejecutando el modelo `llama3.1`. Proporciona la capacidad de razonamiento y toma de decisiones en un entorno completamente local y privado.
- **Memoria Operativa:** `MemorySaver` de LangGraph. Gestiona el contexto a corto y largo plazo del hilo de la conversación, permitiendo al agente recordar interacciones pasadas (ej. detalles de un ticket previo).
- **Base de Conocimiento (RAG):** `ChromaDB` (Vectorstore) + `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`). Permite la recuperación semántica de las políticas e inventario de NutriFit.
- **Herramientas (Tools):**
  1. `@tool consultar_base_datos`: Busca información estricta en los documentos internos.
  2. `@tool registrar_ticket`: Interactúa con el sistema de archivos local (I/O) para generar un reporte físico (`tickets_soporte.txt`) en caso de reclamos.

## 🚀 Requisitos Previos

1. Instalar Python 3.10 o superior.
2. Instalar [Ollama](https://ollama.com/) en el sistema operativo.
3. Descargar el modelo base ejecutando en la terminal:
   ```bash
   ollama pull llama3.1
