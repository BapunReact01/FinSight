from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import AzureError
from typing import Optional, BinaryIO
from app.config import settings
import os

class AzureBlobStorage:
    def __init__(self):
        self.connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
        self.container_name = settings.AZURE_CONTAINER_NAME
        self.blob_service_client = None
        self.container_client = None
        
        if self.connection_string:
            self._initialize()
    
    def _initialize(self):
        """Initialize Azure Blob Storage client"""
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            self.container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            # Create container if not exists
            self.container_client.create_container()
        except AzureError as e:
            print(f"Azure Storage initialization error: {e}")
    
    def upload_file(self, file_name: str, file_data: BinaryIO, 
                   content_type: str = "application/octet-stream") -> Optional[str]:
        """Upload file to Azure Blob Storage"""
        if not self.blob_service_client:
            print("Azure Storage not configured")
            return None
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=file_name
            )
            blob_client.upload_blob(
                file_data,
                overwrite=True,
                content_settings={'content_type': content_type}
            )
            return blob_client.url
        except AzureError as e:
            print(f"Upload error: {e}")
            return None
    
    def download_file(self, file_name: str) -> Optional[bytes]:
        """Download file from Azure Blob Storage"""
        if not self.blob_service_client:
            return None
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=file_name
            )
            download_stream = blob_client.download_blob()
            return download_stream.readall()
        except AzureError as e:
            print(f"Download error: {e}")
            return None
    
    def delete_file(self, file_name: str) -> bool:
        """Delete file from Azure Blob Storage"""
        if not self.blob_service_client:
            return False
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=file_name
            )
            blob_client.delete_blob()
            return True
        except AzureError as e:
            print(f"Delete error: {e}")
            return False
    
    def file_exists(self, file_name: str) -> bool:
        """Check if file exists in Azure Blob Storage"""
        if not self.blob_service_client:
            return False
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=file_name
            )
            blob_client.get_blob_properties()
            return True
        except AzureError:
            return False

# Global instance
azure_storage = AzureBlobStorage()