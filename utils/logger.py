import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class DeckForgeLogger:
    """Custom logger for DeckForge application."""
    
    def __init__(self, name: str = "DeckForge", log_level: str = "INFO", 
                 log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Prevent adding multiple handlers if logger already exists
        if self.logger.handlers:
            return
            
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self.logger.debug(message)
    
    def critical(self, message: str) -> None:
        """Log critical message."""
        self.logger.critical(message)


# Global logger instance
logger = DeckForgeLogger()


def get_logger(name: str = "DeckForge", log_level: str = "INFO", 
               log_file: Optional[str] = None) -> DeckForgeLogger:
    """Get a logger instance."""
    return DeckForgeLogger(name, log_level, log_file)