import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class AzureBlobDocumentStorage:
    """Gestionnaire de persistance et d'archivage des documents sources sur Azure Blob Storage."""

    def __init__(self):
        self._blob_service_client = None

    def _get_client(self):
        if not settings.AZURE_STORAGE_CONNECTION_STRING:
            return None
        if self._blob_service_client is None:
            try:
                from azure.storage.blob import BlobServiceClient
                self._blob_service_client = BlobServiceClient.from_connection_string(
                    settings.AZURE_STORAGE_CONNECTION_STRING
                )
                logger.info("Client Azure Blob Storage initialisé avec succès.")
            except Exception as e:
                logger.warning(f"Échec d'initialisation du client Azure Blob: {e}")
                return None
        return self._blob_service_client

    def upload_file(self, local_path: str, filename: str) -> bool:
        """Téléverse un fichier local sur Azure Blob Storage sous le container documents."""
        client = self._get_client()
        if not client:
            return False

        blob_name = f"documents/{filename}"
        try:
            blob_client = client.get_blob_client(
                container=settings.AZURE_STORAGE_CONTAINER_DOCUMENTS,
                blob=blob_name
            )
            with open(local_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            logger.info(f"Fichier archivé sur Azure Blob : {settings.AZURE_STORAGE_CONTAINER_DOCUMENTS}/{blob_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur d'archivage Azure Blob pour {filename}: {e}")
            return False

    def upload_bytes(self, content: bytes, filename: str) -> bool:
        """Téléverse des données brutes en bytes sur Azure Blob Storage."""
        client = self._get_client()
        if not client:
            return False

        blob_name = f"documents/{filename}"
        try:
            blob_client = client.get_blob_client(
                container=settings.AZURE_STORAGE_CONTAINER_DOCUMENTS,
                blob=blob_name
            )
            blob_client.upload_blob(content, overwrite=True)
            logger.info(f"Contenu archivé sur Azure Blob : {settings.AZURE_STORAGE_CONTAINER_DOCUMENTS}/{blob_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur d'archivage Azure Blob pour {filename}: {e}")
            return False

    def delete_document(self, filename: str) -> bool:
        """Supprime un document du container Azure Blob."""
        client = self._get_client()
        if not client:
            return False

        blob_name = f"documents/{filename}"
        try:
            blob_client = client.get_blob_client(
                container=settings.AZURE_STORAGE_CONTAINER_DOCUMENTS,
                blob=blob_name
            )
            blob_client.delete_blob()
            logger.info(f"Document supprimé d'Azure Blob : {settings.AZURE_STORAGE_CONTAINER_DOCUMENTS}/{blob_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression Azure Blob pour {filename}: {e}")
            return False


azure_blob_storage = AzureBlobDocumentStorage()
