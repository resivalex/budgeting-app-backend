from budgeting_app_backend.services import GoogleDriveService


class GoogleDriveDump:
    """Transaction data dumps to Google Drive."""
    
    def __init__(self, credentials_path=None, folder_id=None):
        """Initialize with Google Drive service.
        
        Args:
            credentials_path: Path to service account credentials JSON
            folder_id: Google Drive folder ID for uploads
        """
        self._google_drive = GoogleDriveService(
            credentials_path=credentials_path,
            folder_id=folder_id
        )
        
    def put(self, content: bytes) -> dict:
        """Upload transaction dump to Google Drive.
        
        Args:
            content: CSV data as bytes
            
        Returns:
            Dict with file ID, name, and link
        """
        return self._google_drive.upload_file(content)
