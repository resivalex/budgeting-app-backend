"""
Scheduler module for managing backup schedules.
"""
from datetime import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Callable, Dict, Any, Optional
from .backup_service import BackupService

logger = logging.getLogger(__name__)

class BackupScheduler:
    """
    Manages scheduling of automated backups.
    """
    
    def __init__(
        self,
        backup_service: BackupService,
        hour: int = 3,
        minute: int = 0
    ):
        """
        Initialize the backup scheduler with a backup service.
        
        Args:
            backup_service: Service that performs the actual backup operation
            hour: Hour of the day to run backup (UTC, 0-23)
            minute: Minute of the hour to run backup (0-59)
        """
        self.backup_service = backup_service
        self.scheduler = BackgroundScheduler()
        self.hour = hour
        self.minute = minute
        
        # Setup the job
        self._configure_scheduler()
    
    def _configure_scheduler(self):
        """Setup the scheduler with the backup job."""
        self.scheduler.add_job(
            self._perform_backup,
            trigger=CronTrigger(hour=self.hour, minute=self.minute),
            id="daily_backup",
            name=f"Daily backup to Google Drive at {self.hour:02d}:{self.minute:02d} UTC",
            replace_existing=True,
        )
    
    def _perform_backup(self):
        """Execute the backup operation."""
        logger.info("Starting scheduled daily backup...")
        
        try:
            result = self.backup_service.create_backup()
            
            if result.get("status") == "error":
                logger.error(f"Error creating backup: {result.get('error')}")
            else:
                logger.info(f"Daily backup completed successfully. File: {result.get('name', 'unknown')}")
                logger.info(f"Google Drive link: {result.get('link', 'not available')}")
                
        except Exception as e:
            logger.error(f"Unexpected error during daily backup: {str(e)}")
    
    def start(self):
        """Start the scheduler if it's not already running."""
        if not self.scheduler.running:
            self.scheduler.start()
            
            # Log information about the backup job
            job = self.scheduler.get_job("daily_backup")
            if job:
                next_run = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S UTC') if job.next_run_time else "unknown"
                logger.info(f"Backup scheduler started (next run: {next_run})")
            else:
                logger.warning("Backup scheduler started but daily_backup job not found")
                
        else:
            logger.info("Scheduler already running, not starting again")
    
    def shutdown(self):
        """Shut down the scheduler if it's running."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Backup scheduler shut down")
    
    def trigger_backup_now(self) -> Dict[str, Any]:
        """
        Manually trigger a backup immediately.
        
        Returns:
            Dictionary with details of the backup operation
        """
        logger.info("Manually triggered backup...")
        
        try:
            result = self.backup_service.create_backup()
            if result.get("status") == "error":
                return {
                    "status": "error",
                    "message": f"Backup failed: {result.get('error')}"
                }
                
            return {
                "status": "success",
                "message": "Backup completed successfully",
                "name": result.get("name", "unknown"),
                "link": result.get("link", "not available")
            }
            
        except Exception as e:
            logger.error(f"Error in manual backup: {str(e)}")
            return {
                "status": "error",
                "message": f"Backup failed: {str(e)}"
            }
    
    def get_next_backup_time(self) -> Optional[str]:
        """
        Get the next scheduled backup time.
        
        Returns:
            ISO formatted datetime string or None if no job is scheduled
        """
        job = self.scheduler.get_job("daily_backup")
        if job and job.next_run_time:
            return job.next_run_time.isoformat()
        return None
