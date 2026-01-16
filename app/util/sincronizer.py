"""Utilidades para sincronización de documentos y procesamiento de texto."""

import os
from typing import List, Any
import re

# LangChain splitter (mejor que CharacterTextSplitter para RAG)
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_files(path: str = "") -> List[str]:
    """Lista archivos válidos en una carpeta."""
    if not path or not os.path.isdir(path):
        return []
    files = []
    for element in os.listdir(path):
        full_path = os.path.join(path, element)
        if os.path.isfile(full_path):
            files.append(full_path)
    return files

def clean_text(text: str) -> str:
    """
    Limpieza robusta para eliminar ruido de conversión (tablas rotas, headers repetidos).
    """
    if not text:
        return ""
    text = text.replace("\r", " ")
    text = text.replace('""', '"')

    # Colapsar espacios múltiples y saltos de línea excesivos
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def split_text(text: str, max_chars: int = 1000, overlap: int = 100) -> List[str]:
    """Usa RecursiveCharacterTextSplitter para cortes inteligentes."""
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=max_chars,
        chunk_overlap=overlap,
    )
    return splitter.split_text(text)

def normalize_azure_search_results(results: Any):
    """Normaliza la respuesta de Azure Search SDK."""
    if hasattr(results, "results"):
        return results.results
    if isinstance(results, list):
        return results
    return None
