"""Subida y sincronización de documentos con Azure Cognitive Search."""

# Utilitarios para sincronización de documentos con Azure Cognitive Search
from typing import List, Dict, Any
import os
import shutil
import uuid
import time

# Azure Document Intelligence
from azure.ai.formrecognizer import DocumentAnalysisClient

# Helpers propios
from app.core.knowledge import connect_search_client, get_analyzer
from app.util.sincronizer import clean_text, split_text, get_files, normalize_azure_search_results

def read_document(file_path: str):
    """
    Lee el contenido de un documento usando Azure Document Intelligence.
    """
    service: DocumentAnalysisClient = get_analyzer()

    with open(file_path, "rb") as file:
        instruct = service.begin_analyze_document("prebuilt-layout", file)
        result = instruct.result()

    full_text = result.content or ""
    sections: List[Dict[str, Any]] = []

    for page in result.pages:
        lines_content = []

        # Recolectamos el texto línea por línea
        if hasattr(page, 'lines'):
            for line in page.lines:
                lines_content.append(line.content)

        # Unimos con salto de línea.
        page_text = "\n".join(lines_content)

        # Solo guardamos si la página tiene texto
        if page_text.strip():
            sections.append({
                "text": page_text, 
                "page": page.page_number
            })

    # Fallback: Si por alguna razón extraña no hay páginas detectadas pero sí texto global
    if not sections and full_text:
        sections.append({"text": full_text, "page": 1})

    return full_text, sections

def get_chunks(content: str) -> List[Dict[str, str]]:
    """
    Obtiene los chunks desde un texto leído.
    """
    chunks = split_text(content)
    identified_chunks = []

    for chunk in chunks:
        processed_text = clean_text(chunk)
        if len(processed_text) > 10:
            identified_chunks.append({
                "id": str(uuid.uuid4()),
                "content": processed_text})
    return identified_chunks

def upload_file(file_path: str = "") -> bool:
    """
    Lee el PDF, genera chunks con metadatos y los sube.
    Args:
        rutaDeArchivo (str): Ruta del archivo a procesar.
    Returns: Resultados de la operación de subida.
    """
    try:
        content,_ = read_document(file_path)
        chunks = get_chunks(content)

        knowledge_base = connect_search_client()
        results = knowledge_base.upload_documents(chunks)
        clean_results = normalize_azure_search_results(results)
        if not clean_results:
            return False

        for result in clean_results:
            if not result.succeeded:
                return False
        return True
    except OSError as e:
        print(f"⚠️ Error al procesar {file_path}: {e}")
        return False

def upload_files_from_folder(folder_path: str = ""):
    """Carga todos los archivos de una carpeta a la base de conocimiento."""
    error_folder = os.path.join(folder_path, "error_files")

    while True:
        print("Ejecutando sincronización...")
        archivos = get_files(folder_path)

        if archivos:
            for file_path in archivos:
                filename = os.path.basename(file_path)

                # Evitar procesar archivos temporales o de sistema
                if filename.startswith(".") or filename == "error_files":
                    continue

                print(f"procesando: {filename}...")

                success = upload_file(file_path)

                if success:
                    try:
                        os.remove(file_path)
                        print(f"{filename} procesado y eliminado.")
                    except OSError as e:
                        print(f"⚠️ Error al borrar archivo {filename}: {e}")
                else:
                    print(f"{filename} tiene errores. Moviendo a carpeta de revisión.")
                    os.makedirs(error_folder, exist_ok=True)

                    timestamp = int(time.time())
                    destino = os.path.join(error_folder, f"{timestamp}_{filename}")
                    shutil.move(file_path, destino)
        time.sleep(5)
