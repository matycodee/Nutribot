import warnings
warnings.filterwarnings("ignore")

import os
import re
import time
import json
import psutil
from datetime import datetime

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

ARCHIVO_LOGS = "logs_observabilidad.jsonl"

def limpiar_datos_personales(texto: str):
    limpio = texto
    se_oculto = False

    if re.search(r'\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b', limpio):
        limpio = re.sub(r'\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b', "[RUT_OCULTO]", limpio)
        se_oculto = True

    if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', limpio):
        limpio = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "[EMAIL_OCULTO]", limpio)
        se_oculto = True

    if re.search(r'(\+?56\s?9\s?\d{4}\s?\d{4}|\b9\d{8}\b)', limpio):
        limpio = re.sub(r'(\+?56\s?9\s?\d{4}\s?\d{4}|\b9\d{8}\b)', "[FONO_OCULTO]", limpio)
        se_oculto = True

    return limpio, se_oculto

def guardar_log(datos: dict):
    with open(ARCHIVO_LOGS, "a", encoding="utf-8") as f:
        f.write(json.dumps(datos, ensure_ascii=False) + "\n")

@tool
def registrar_ticket(problema: str) -> str:
    """Guarda un ticket de soporte cuando un cliente tiene un reclamo o falta stock."""
    problema_filtrado, hubo_pii = limpiar_datos_personales(problema)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("tickets_soporte.txt", "a", encoding="utf-8") as f:
        f.write(f"[{fecha}] TICKET DE SOPORTE: {problema_filtrado}\n---\n")
    if hubo_pii:
        return "El ticket fue guardado exitosamente (datos personales enmascarados por privacidad)."
    return "El ticket fue redactado y guardado exitosamente en el sistema."

def iniciar_agente():
    t_inicio = time.perf_counter()
    print("Cargando la base de conocimientos de NutriFit...")
    
    loader_txt = TextLoader(file_path="./data/inventario.txt", encoding="utf-8")
    docs_txt = loader_txt.load()
    loader_pdf = PyPDFLoader(file_path="./data/politicas.pdf")
    docs_pdf = loader_pdf.load_and_split()
    documentos = docs_txt + docs_pdf
    
    print("Vectorizando datos localmente...")
    vectorstore = Chroma.from_documents(
        documents=documentos, 
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    @tool
    def consultar_base_datos(consulta: str) -> str:
        """Busca información de inventario, stock, precios y políticas de NutriFit."""
        docs = retriever.invoke(consulta)
        if not docs:
            return "Sin coincidencias en los documentos."
        return "\n\n".join(doc.page_content for doc in docs)

    tools = [consultar_base_datos, registrar_ticket]
    
    print("Iniciando Llama 3.1 en Ollama...")
    llm = ChatOllama(model="llama3.1", temperature=0)
    memory = MemorySaver()

    agent_executor = create_react_agent(llm, tools, checkpointer=memory)
    print(f"Agente listo en {round(time.perf_counter() - t_inicio, 2)}s")
    return agent_executor

def procesar_consulta(agente, pregunta: str, config: dict, instrucciones: str, tipo_prueba: str = "manual") -> str:
    proceso = psutil.Process(os.getpid())
    ram_inicial = proceso.memory_info().rss / (1024 * 1024)
    psutil.cpu_percent(interval=None)
    t0 = time.perf_counter()

    herramienta = "respuesta_directa"
    uso_fallback = False
    estado = "ok"
    detalle_error = ""
    respuesta_final = ""

    try:
        prev_state = agente.get_state(config)
        cant_previa = len(prev_state.values.get("messages", [])) if prev_state.values else 0

        res = agente.invoke(
            {"messages": [("system", instrucciones), ("user", pregunta)]}, 
            config
        )
        
        for msg in res["messages"][cant_previa:]:
            if isinstance(msg, ToolMessage):
                herramienta = msg.name

        respuesta_final = res["messages"][-1].content

        # Si el modelo devuelve el JSON como texto en vez de invocar la tool, lo ejecutamos igual
        if '{"name": "registrar_ticket"' in respuesta_final:
            try:
                data = json.loads(respuesta_final)
                prob = data.get("parameters", {}).get("problema", "Problema no especificado")
                registrar_ticket.invoke({"problema": prob})
                respuesta_final = "¡Listo! El ticket fue redactado y guardado exitosamente en el sistema."
                herramienta = "registrar_ticket (fallback)"
                uso_fallback = True
            except Exception as ex:
                estado = "error_fallback"
                detalle_error = str(ex)

    except Exception as e:
        estado = "error"
        detalle_error = str(e)
        respuesta_final = f"Error al procesar consulta: {e}"

    latencia = round(time.perf_counter() - t0, 3)
    ram_final = proceso.memory_info().rss / (1024 * 1024)
    cpu = psutil.cpu_percent(interval=None)

    _, pii_detectado = limpiar_datos_personales(pregunta)
    sin_datos = "no poseo esa información" in respuesta_final.lower()

    guardar_log({
        "timestamp": datetime.now().isoformat(),
        "thread_id": config["configurable"]["thread_id"],
        "escenario": tipo_prueba,
        "pregunta": pregunta,
        "respuesta_corta": respuesta_final[:160],
        "herramienta": herramienta,
        "fallback_activado": uso_fallback,
        "latencia_seg": latencia,
        "ram_mb": round(ram_final, 2),
        "delta_ram_mb": round(ram_final - ram_inicial, 2),
        "cpu_pct": cpu,
        "estado": estado,
        "sin_evidencia": sin_datos,
        "pii_detectado": pii_detectado,
        "error": detalle_error
    })
    return respuesta_final

REGLAS = (
    "Eres 'NutriBot', asistente interno para soporte de NutriFit Chile. "
    "Reglas: "
    "1. Si preguntan por productos, precios, stock o políticas, usa 'consultar_base_datos'. "
    "2. Si el dato no aparece en los documentos, responde exacto: 'No poseo esa información en mis registros actuales'. "
    "3. No inventes datos bajo ningún motivo. "
    "4. Si piden registrar un ticket o reclamo, usa 'registrar_ticket'."
)

if __name__ == "__main__":
    try:
        agente = iniciar_agente()
        print("\n--- NutriBot Iniciado (escribe 'salir' para cerrar) ---")
        config = {"configurable": {"thread_id": "sesion_1"}}
        
        while True:
            pregunta = input("\nEjecutivo NutriFit: ")
            if pregunta.lower() == "salir":
                break
            salida = procesar_consulta(agente, pregunta, config, REGLAS, tipo_prueba="manual")
            print(f"\nNutriBot: {salida}")
    except Exception as e:
        print(f"\nError al iniciar: {e}")