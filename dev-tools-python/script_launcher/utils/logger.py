import os
import logging
from datetime import datetime
from typing import Optional

class ScriptLogger:
    def __init__(self, log_file: str):
        """Initialise le logger.
        
        Args:
            log_file (str): Chemin vers le fichier de log
        """
        self.log_file = log_file
        self._setup_logger()
        
    def _setup_logger(self) -> None:
        """Configure le logger."""
        self.logger = logging.getLogger(f"script_logger_{os.path.basename(self.log_file)}")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler pour le fichier
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Ajouter le handler au logger
        self.logger.addHandler(file_handler)
        
    def _check_log_size(self) -> None:
        """Vérifie la taille du fichier de log et le tronque si nécessaire."""
        try:
            size = os.path.getsize(self.log_file)
            if size > 5 * 1024 * 1024:  # 5 Mo
                # Créer un fichier de backup
                backup_path = f"{self.log_file}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
                os.rename(self.log_file, backup_path)
                
                # Créer un nouveau fichier de log
                self._setup_logger()
        except OSError:
            pass
            
    def log(self, message: str, level: str = "INFO") -> None:
        """Écrit un message dans le log.
        
        Args:
            message (str): Message à logger
            level (str): Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._check_log_size()
        
        level_map = {
            "DEBUG": self.logger.debug,
            "INFO": self.logger.info,
            "WARNING": self.logger.warning,
            "ERROR": self.logger.error,
            "CRITICAL": self.logger.critical
        }
        
        log_func = level_map.get(level.upper(), self.logger.info)
        log_func(message)