

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
=======
# NutriBot - Agente Funcional de Soporte Organizacional

Este repositorio contiene la implementación de "NutriBot", un agente de Inteligencia Artificial desarrollado para la Evaluación Parcial 2 (ISY0101). El agente asiste a ejecutivos de soporte de NutriFit Chile respondiendo consultas basadas en una base de conocimientos y registrando tickets de soporte de manera autónoma.

## Arquitectura y Orquestación de Componentes

El agente fue construido utilizando **LangGraph** (la evolución de LangChain Agents) para garantizar un flujo de trabajo cíclico, escalable y con retención de contexto (memoria). 

### Diagrama de Flujo (Orquestación)
1. **Entrada de Usuario**: El ejecutivo de soporte ingresa una consulta (ej. "Precio del Omega 3" o "Registrar queja por falta de stock").
2. **Memoria (MemorySaver)**: LangGraph inyecta el historial de la conversación (Thread) para mantener el contexto en interacciones prolongadas.
3. **LLM Core (GPT-3.5)**: El motor de OpenAI razona sobre el *System Prompt* y decide qué herramienta utilizar basado en la intención del usuario.
4. **Ejecución de Herramientas**:
   - **`consultar_base_datos`**: Herramienta RAG acoplada a ChromaDB y OpenAI Embeddings. Recupera normativas (PDF) e inventario (TXT).
   - **`registrar_ticket`**: Herramienta de escritura que anexa reclamos directamente en un archivo local `tickets_soporte.txt`.
5. **Respuesta**: El agente sintetiza la información obtenida de las herramientas y responde al ejecutivo.

## Requisitos Previos

- Python 3.10 o superior.
- Credencial de OpenAI (API Key).

## Instrucciones de Ejecución

1. **Instalar Dependencias**:
   Asegúrese de instalar las librerías necesarias ejecutando en la terminal:
   ```bash
   pip install -r requirements.txt
>>>>>>> 292b8e6 (Versión final NutriBot lista para Evaluación 2 y grabación)
