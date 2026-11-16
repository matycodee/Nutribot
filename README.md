# 🤖 NutriBot - Agente Inteligente Local para NutriFit Chile

Este repositorio contiene el código fuente para la **Evaluación Parcial N°2** de la asignatura Ingeniería de Soluciones con IA (ISY0101) en Duoc UC. 

El proyecto evoluciona de un simple sistema de consultas a un **Agente Autónomo 100% local**, capaz de integrar herramientas de búsqueda, escritura y razonamiento mediante un flujo de trabajo orquestado, sin depender de internet ni de APIs externas de pago.

## 🏗️ Arquitectura y Tecnologías
El agente fue diseñado priorizando la privacidad absoluta de los datos de la empresa. Todo el procesamiento ocurre en la máquina local:
* **Orquestador Central:** **LangGraph** (`create_react_agent`). Se encarga de evaluar la consulta del usuario, decidir qué herramienta utilizar y mantener el ciclo de razonamiento.
* **Motor LLM:** **Ollama** ejecutando el modelo **Llama 3.1**. Proporciona la capacidad de razonamiento y toma de decisiones.
* **Memoria Operativa:** `MemorySaver` de LangGraph. Gestiona el contexto a corto plazo del hilo de la conversación, permitiendo al agente recordar interacciones pasadas.
* **Base de Conocimiento (RAG):** **ChromaDB** junto con *HuggingFace Embeddings*. Permite la recuperación semántica de las políticas e inventario de NutriFit.

## 🛠️ Herramientas (Tools)
1. `consultar_base_datos`: Busca información estricta en los documentos internos (PDF/CSV) para generar respuestas precisas sin alucinaciones.
2. `registrar_ticket`: Interactúa con el sistema de archivos local (I/O) para redactar y guardar un reporte físico (`tickets_soporte.txt`) en caso de reclamos.

## 💻 Instrucciones de Ejecución
1. Instalar Python 3.10 o superior.
2. Descargar e instalar [Ollama](https://ollama.com/).
3. Descargar el modelo base ejecutando en la terminal:
   ```bash
   ollama pull llama3.1
