import os
import io
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


class GoogleDriveService:
    """Google Drive API service for file uploads."""
    
    def __init__(self, credentials_path=None, folder_id=None):
        """Initialize Google Drive service.
        
        Args:
            credentials_path: Path to service account credentials JSON
            folder_id: Google Drive folder ID for uploads
        """
        self._credentials_path = credentials_path or os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH")
        self._folder_id = folder_id or os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        
        if not self._credentials_path or not os.path.exists(self._credentials_path):
            raise ValueError(
                "Google Drive credentials file not found. "
                "Please provide a valid path to service account credentials."
            )
            
        if not self._folder_id:
            raise ValueError(
                "Google Drive folder ID not provided. "
                "Please set the GOOGLE_DRIVE_FOLDER_ID environment variable."
            )
            
        # Initialize the service
        self._service = self._create_drive_service()
        
    def _create_drive_service(self):
        """Create an authorized Google Drive API service."""
        credentials = service_account.Credentials.from_service_account_file(
            self._credentials_path, 
            scopes=['https://www.googleapis.com/auth/drive']
        )
        return build('drive', 'v3', credentials=credentials)
    
    def upload_file(self, file_content, mime_type='text/csv'):
        """Upload file to Google Drive.
        
        Args:
            file_content: File content as bytes
            mime_type: MIME type (default: 'text/csv')
            
        Returns:
            Dict with file id, name, and link
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"budget_transactions_dump_{timestamp}.csv"
        
        file_obj = io.BytesIO(file_content)
        
        media = MediaIoBaseUpload(
            file_obj, 
            mimetype=mime_type,
            resumable=True
        )
        file_metadata = {
            'name': filename,
            'parents': [self._folder_id]
        }
        
        uploaded_file = self._service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        return {
            'id': uploaded_file['id'],
            'name': uploaded_file['name'],
            'link': uploaded_file.get('webViewLink', '')
        }
