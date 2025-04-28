"""
Database backup utility for the POS system.
"""

import os
import shutil
from datetime import datetime
from config import DATABASE
from utils.logger import setup_logger, log_info, log_error

logger = setup_logger('database.backup')

def create_backup():
    """
    Create a backup of the database.
    
    Returns:
        str: Path to the backup file if successful, None otherwise
    """
    try:
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"pos_backup_{timestamp}.db"
        backup_path = os.path.join(DATABASE['backup_dir'], backup_filename)
        
        # Copy database file to backup location
        shutil.copy2(DATABASE['path'], backup_path)
        
        log_info(logger, f"Database backup created successfully: {backup_path}")
        return backup_path
    except Exception as e:
        log_error(logger, e, {"operation": "create_backup"})
        return None

def restore_backup(backup_path):
    """
    Restore database from a backup file.
    
    Args:
        backup_path (str): Path to the backup file
        
    Returns:
        bool: True if restore was successful, False otherwise
    """
    try:
        if not os.path.exists(backup_path):
            log_error(logger, f"Backup file not found: {backup_path}")
            return False
            
        # Create a backup of current database before restore
        current_backup = create_backup()
        
        # Restore from backup
        shutil.copy2(backup_path, DATABASE['path'])
        
        log_info(logger, f"Database restored successfully from: {backup_path}")
        return True
    except Exception as e:
        log_error(logger, e, {
            "operation": "restore_backup",
            "backup_path": backup_path
        })
        return False

def list_backups():
    """
    List all available database backups.
    
    Returns:
        list: List of backup file paths
    """
    try:
        backups = []
        for filename in os.listdir(DATABASE['backup_dir']):
            if filename.startswith('pos_backup_') and filename.endswith('.db'):
                backup_path = os.path.join(DATABASE['backup_dir'], filename)
                backups.append(backup_path)
        return sorted(backups, reverse=True)
    except Exception as e:
        log_error(logger, e, {"operation": "list_backups"})
        return []

def delete_backup(backup_path):
    """
    Delete a database backup file.
    
    Args:
        backup_path (str): Path to the backup file
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        if not os.path.exists(backup_path):
            log_error(logger, f"Backup file not found: {backup_path}")
            return False
            
        os.remove(backup_path)
        log_info(logger, f"Backup file deleted: {backup_path}")
        return True
    except Exception as e:
        log_error(logger, e, {
            "operation": "delete_backup",
            "backup_path": backup_path
        })
        return False 