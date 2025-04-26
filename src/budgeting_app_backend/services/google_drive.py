import os
import io
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


class GoogleDriveService:
    """
    Service for interacting with Google Drive API.
    Handles file uploads and manages authorization.
    """
    
    def __init__(self, credentials_path=None, folder_id=None):
        """
        Initialize the Google Drive service.
        
        Args:
            credentials_path: Path to the service account credentials JSON file
            folder_id: ID of the Google Drive folder to use for uploads
        """
        # Use provided credentials or get from environment variable
        self._credentials_path = credentials_path or os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH")
        # Use provided folder ID or get from environment variable
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
        """Create and return an authorized Google Drive API service instance."""
        credentials = service_account.Credentials.from_service_account_file(
            self._credentials_path, 
            scopes=['https://www.googleapis.com/auth/drive']
        )
        return build('drive', 'v3', credentials=credentials)
    
    def upload_file(self, file_content, mime_type='text/csv'):
        """
        Upload a file to Google Drive folder specified in the constructor.
        
        Args:
            file_content: The content of the file as bytes
            mime_type: MIME type of the file (default: 'text/csv')
            
        Returns:
            The file ID of the uploaded file
        """
        # Generate a timestamp-based filename
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"budget_transactions_dump_{timestamp}.csv"
        
        # Create a file-like object from the content
        file_obj = io.BytesIO(file_content)
        
        # Create media object for upload
        media = MediaIoBaseUpload(
            file_obj, 
            mimetype=mime_type,
            resumable=True
        )
        
        # Define file metadata
        file_metadata = {
            'name': filename,
            'parents': [self._folder_id]
        }
        
        # Execute the upload
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
