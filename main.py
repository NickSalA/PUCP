"""Script principal para interactuar con el agente de flujo sin FastAPI."""

import asyncio
from app.flow.flow import FlowAgent


async def main():
    """Función principal del script."""
    print("=" * 60)
    print("🎓 Asistente de Normativa y Permanencia Estudiantil - PUCP")
    print("=" * 60)
    print("Escribe 'salir' para terminar la conversación.")
    print("Escribe 'nuevo' para iniciar una nueva conversación.")
    print("-" * 60)

    agente = FlowAgent()
    thread_id = agente.reset_memory()

    while True:
        try:
            mensaje = input("Tú: ").strip()

            if not mensaje:
                continue

            if mensaje.lower() == "salir":
                print("\n👋 ¡Hasta luego! Esperamos haberte ayudado.")
                break

            if mensaje.lower() == "nuevo":
                thread_id = agente.reset_memory()
                print(f"\n🔄 Nueva conversación iniciada. Thread ID: {thread_id}\n")
                continue

            print("\n⏳ Procesando...\n")
            respuesta = await agente.answer_message(mensaje, thread_id)
            print(f"Agente: {respuesta}\n")
            print("-" * 60)

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break

if __name__ == "__main__":
    asyncio.run(main())
