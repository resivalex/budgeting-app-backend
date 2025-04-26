from budgeting_app_backend.services import GoogleDriveService


class GoogleDriveDump:
    """
    Handles transaction data dumps to Google Drive.
    """
    
    def __init__(self, credentials_path=None, folder_id=None):
        """
        Initialize the GoogleDriveDump with Google Drive service.
        
        Args:
            credentials_path: Path to the service account credentials JSON file
            folder_id: ID of the Google Drive folder to use for uploads
        """
        self._google_drive = GoogleDriveService(
            credentials_path=credentials_path,
            folder_id=folder_id
        )
        
    def put(self, content: bytes) -> dict:
        """
        Upload transaction dump content to Google Drive.
        
        Args:
            content: CSV data as bytes
            
        Returns:
            Dictionary with upload details (file ID, name, link)
        """
        return self._google_drive.upload_file(content)
