# 🤖 NutriBot — Agente Local de Soporte con Observabilidad (NutriFit Chile)

Repositorio oficial del proyecto **NutriBot**, desarrollado para la **Evaluación Parcial N.º 3** de la asignatura *Ingeniería de Soluciones con IA (ISY0101)* en Duoc UC.

NutriBot es un asistente inteligente que opera **100% de forma local** para responder consultas de inventario, precios y políticas de NutriFit Chile, además de registrar tickets de soporte. En esta tercera etapa se incorporó una capa completa de **observabilidad, trazabilidad, control de privacidad (PII) y monitoreo visual**.

---

## 🚀 Novedades Implementadas (Evaluación 3)

* **Telemetría y Trazabilidad (`app.py`):** Registro estructurado en `logs_observabilidad.jsonl` con métricas por turno: latencia de inferencia (segundos), consumo de memoria RAM y CPU del proceso (`psutil`), herramienta invocada por LangGraph, detección de abstención frente a preguntas fuera de dominio y registro de excepciones.
* **Protección de Datos Personales (`limpiar_datos_personales`):** Filtro previo a la escritura que detecta y enmascara automáticamente RUTs chilenos (`[RUT_OCULTO]`), correos electrónicos (`[EMAIL_OCULTO]`) y teléfonos (`[FONO_OCULTO]`) antes de guardar reclamos en `tickets_soporte.txt`.
* **Batería Automatizada de Pruebas (`test_observabilidad.py`):** Suite de 12 escenarios diseñados para auditar el comportamiento del agente bajo variabilidad de datos (consultas RAG, consistencia semántica, preguntas trampa fuera de dominio, manejo de PII y memoria conversacional por `thread_id`).
* **Dashboard Interactivo (`dashboard.py`):** Panel visual construido en **Streamlit** y **Plotly** para filtrar ejecuciones y analizar KPIs (tasa de éxito, latencia media/máxima, uso de herramientas y consumo de RAM).

---

## 📁 Estructura del Proyecto

```text
Nutribot/
├── data/                        # Base de conocimientos (inventario.txt, politicas.pdf)
├── static/                      # Recursos estáticos de interfaz
├── app.py                       # Lógica principal del agente, telemetría y filtro PII
├── test_observabilidad.py       # Script de ejecución automatizada de 12 casos de prueba
├── dashboard.py                 # Dashboard visual en Streamlit + Plotly
├── logs_observabilidad.jsonl    # Registros estructurados generados tras las pruebas
├── tickets_soporte.txt          # Archivo de salida de reclamos con datos sanitizados
├── requirements.txt             # Dependencias base del proyecto
└── README.md                    # Documentación y guía de ejecución
