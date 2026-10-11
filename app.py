import warnings
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# 1. HERRAMIENTA DE ESCRITURA (Tickets)
@tool
def registrar_ticket(problema: str) -> str:
    """Útil para escribir, registrar o guardar un ticket de soporte cuando un cliente tiene un reclamo o falta stock."""
    with open("tickets_soporte.txt", "a", encoding="utf-8") as f:
        f.write(f"TICKET DE SOPORTE: {problema}\n---\n")
    return "El ticket fue redactado y guardado exitosamente en el sistema."

def iniciar_agente():
    print("Cargando la base de conocimientos de NutriFit...")
    
    loader_txt = TextLoader(file_path="./data/inventario.txt", encoding="utf-8")
    docs_txt = loader_txt.load()
    loader_pdf = PyPDFLoader(file_path="./data/politicas.pdf")
    docs_pdf = loader_pdf.load_and_split()
    documentos = docs_txt + docs_pdf
    
    print("Vectorizando datos de forma local con HuggingFace...")
    vectorstore = Chroma.from_documents(documents=documentos, embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # 2. HERRAMIENTA DE CONSULTA (RAG)
    @tool
    def consultar_base_datos(consulta: str) -> str:
        """Útil para buscar información estricta de inventario, stock, precios y políticas corporativas de NutriFit."""
        documentos_recuperados = retriever.invoke(consulta)
        return "\n\n".join(doc.page_content for doc in documentos_recuperados)

    tools = [consultar_base_datos, registrar_ticket]
    
    print("Iniciando motor LLM con Ollama...")
    llm = ChatOllama(model="llama3.1", temperature=0)
    memory = MemorySaver()

    # 3. ORQUESTACIÓN CON LANGGRAPH (Sin parámetros conflictivos)
    agent_executor = create_react_agent(
        llm, 
        tools, 
        checkpointer=memory
    )
    
    return agent_executor

if __name__ == "__main__":
    try:
        agente = iniciar_agente()
        print("\n--- NutriBot Agente Local Iniciado. Escribe 'salir' para terminar ---")
        
        config = {"configurable": {"thread_id": "sesion_1"}}
        
        # Mantenemos las reglas aquí para inyectarlas directamente en el flujo
        instrucciones = (
            "Eres 'NutriBot', un agente técnico exclusivo para los ejecutivos de soporte de NutriFit Chile. "
            "REGLAS ESTRICTAS: "
            "1. Si te preguntan por productos o políticas, DEBES usar la herramienta 'consultar_base_datos'. "
            "2. Si la información no está en la base de datos, responde textualmente: 'No poseo esa información en mis registros actuales'. "
            "3. Nunca inventes precios, ni políticas, ni stock. "
            "4. Si te piden levantar, guardar o registrar un ticket, usa la herramienta 'registrar_ticket'."
        )
        
        import json # Necesario para leer la respuesta del bot
        
        while True:
            pregunta = input("\nEjecutivo NutriFit: ")
            if pregunta.lower() == "salir":
                break
            try:
                # Inyectamos el SystemMessage junto con la pregunta
                respuesta = agente.invoke(
                    {"messages": [("system", instrucciones), ("user", pregunta)]}, 
                    config
                )
                
                texto_bot = respuesta['messages'][-1].content
                
                # --- INICIO DEL SALVAVIDAS ---
                # Si LangGraph no lo ejecuta, atrapamos el JSON manualmente
                if '{"name": "registrar_ticket"' in texto_bot:
                    try:
                        # Extraemos el problema del texto JSON
                        datos = json.loads(texto_bot)
                        problema = datos.get("parameters", {}).get("problema", "Problema no especificado")
                        # Forzamos la ejecución de la herramienta
                        registrar_ticket.invoke({"problema": problema})
                        print("\nNutriBot: ¡Listo! El ticket fue redactado y guardado exitosamente en el sistema.")
                        continue # Volvemos a pedir otra pregunta
                    except Exception as e:
                        pass # Si falla, que siga normal
                # --- FIN DEL SALVAVIDAS ---
                
                print(f"\nNutriBot: {texto_bot}")
            except Exception as e:
                print(f"\n[Error al procesar consulta]: {e}")
    except Exception as e:
        print(f"\n[Error al inicializar agente]: {e}")