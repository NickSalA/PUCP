"""Cliente de Azure Cognitive Search."""
from langchain_community.retrievers import AzureAISearchRetriever
from azure.search.documents import SearchClient
from azure.ai.formrecognizer import DocumentAnalysisClient

# Credenciales Azure
from azure.core.credentials import AzureKeyCredential

# Helpers propios
from app.core.config import settings

def get_retriever() -> AzureAISearchRetriever:
    """ Obtener el retriever de Azure Cognitive Search.
    Returns:
        AzureAISearchRetriever: Instancia del retriever.
    """

    return AzureAISearchRetriever(
        service_name = settings.AZURE_SEARCH_SERVICE_NAME,
        api_key = settings.AZURE_SEARCH_API_KEY,
        index_name = settings.AZURE_SEARCH_INDEX_NAME,
        top_k = settings.AZURE_SEARCH_TOP_K,
    )

def connect_search_client() -> SearchClient:
    """ Conectar al cliente de Azure Cognitive Search.
    Returns:
        SearchClient: Instancia del cliente de búsqueda.
    """

    return SearchClient(
        f"https://{settings.AZURE_SEARCH_SERVICE_NAME}.search.windows.net",
        settings.AZURE_SEARCH_INDEX_NAME,
        AzureKeyCredential(settings.AZURE_SEARCH_API_KEY)
    )

def get_analyzer() -> DocumentAnalysisClient:
    """ Conectar al cliente de Azure Document Intelligence.
    Returns:
        DocumentAnalysisClient: Instancia del cliente de análisis de documentos.
    """

    return DocumentAnalysisClient(
        endpoint=f"https://{settings.AZURE_FORM_SERVICE_NAME}.cognitiveservices.azure.com/",
        credential=AzureKeyCredential(settings.AZURE_FORM_API_KEY)
    )
