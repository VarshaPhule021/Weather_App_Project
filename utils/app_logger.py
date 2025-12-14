import logging
import logging.handlers
import os
from datetime import datetime

class AppLogger:
    """Logger utility for the Weather App"""
    
    def __init__(self, log_dir='logs'):
        """Initialize logger with file and console handlers"""
        self.log_dir = log_dir
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create logger
        self.logger = logging.getLogger('WeatherApp')
        self.logger.setLevel(logging.DEBUG)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler - logs everything
        log_file = os.path.join(log_dir, f'weather_app_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler - logs warnings and above
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """Return the configured logger instance"""
        return self.logger


# Initialize logger
_app_logger = AppLogger()
logger = _app_logger.get_logger()
