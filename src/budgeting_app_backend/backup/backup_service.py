"""
Backup service implementation.
"""
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BackupService:
    """
    Service for performing application data backups.
    """
    
    def __init__(self, state_factory: callable):
        """
        Initialize the backup service.
        
        Args:
            state_factory: A factory function that creates a new State instance
        """
        self.state_factory = state_factory
    
    def create_backup(self) -> Dict[str, Any]:
        """
        Creates a backup of the current application data.
        
        Returns:
            Dictionary containing the result of the backup operation
        """
        try:
            # Get a fresh state instance
            state = self.state_factory()
            
            # Perform the dump operation
            result = state.dump()
            
            return result
            
        except Exception as e:
            logger.error(f"Error during backup creation: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
