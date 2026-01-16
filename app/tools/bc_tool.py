"""Tool de base de conocimientos para el agente."""

# Manejo de herramientas y agentes
from langchain_core.tools import Tool

# Helpers propios
from app.core.knowledge import get_retriever

# Utilitario para crear tool de base de conocimientos
from app.util.retriever import create_retriever_tool

retriever = get_retriever()

def bc_tool() -> Tool:
    """Crear una herramienta de base de conocimientos para el agente."""
    return create_retriever_tool(
        retriever=retriever,
        name="bc_tool",
        description="""Úsala para responder preguntas técnicas específicas sobre los contenidos de programación disponibles en la base de conocimientos.
        Devuelve respuestas precisas y concisas basadas en los documentos que encuentres."""
    )
