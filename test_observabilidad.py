import time
from app import iniciar_agente, procesar_consulta, REGLAS

def ejecutar_pruebas():
    agente = iniciar_agente()
    
    casos = [
        ("hilo_1", "consulta_inventario", "¿Cuál es el precio y stock de la proteína Whey?"),
        ("hilo_1", "consulta_politicas", "¿Cuáles son los tiempos y costos de envío a regiones?"),
        ("hilo_1", "consulta_politicas", "¿Qué medios de pago acepta NutriFit Chile?"),
        ("hilo_2", "consistencia", "¿Tienen creatina disponible y cuánto cuesta?"),
        ("hilo_2", "consistencia", "Dime el valor y unidades en bodega de la creatina"),
        ("hilo_3", "fuera_dominio", "¿Cuánto cuesta la mensualidad del gimnasio de NutriFit?"),
        ("hilo_3", "fuera_dominio", "¿Venden bicicletas estáticas marca Peloton?"),
        ("hilo_4", "ticket_con_pii", "Registra un ticket: el cliente Juan Pérez (RUT 18.456.789-2, correo juan.perez@gmail.com) reclama que su pedido llegó abierto."),
        ("hilo_4", "memoria_hilo", "¿Qué reclamo acabas de registrar recién?"),
        ("hilo_5", "ticket_stock", "Levanta un reclamo porque se acabó el stock de Omega 3."),
        ("hilo_6", "charla_directa", "Hola NutriBot, ¿en qué me puedes ayudar hoy?"),
        ("hilo_6", "consulta_politicas", "¿Cómo funcionan las devoluciones o cambios de productos?")
    ]

    print(f"\nEjecutando {len(casos)} casos de prueba...\n")
    for i, (hilo, categoria, texto) in enumerate(casos, start=1):
        print(f"[{i}/{len(casos)}] {categoria}: {texto}")
        cfg = {"configurable": {"thread_id": hilo}}
        resp = procesar_consulta(agente, texto, cfg, REGLAS, tipo_prueba=categoria)
        print(f" -> {resp[:100]}...\n")
        time.sleep(0.5)

    print("Listo. Registros guardados en logs_observabilidad.jsonl")

if __name__ == "__main__":
    ejecutar_pruebas()