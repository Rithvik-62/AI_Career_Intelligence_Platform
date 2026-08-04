import logging
import os
import sys

# Add root directory to path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import LOGS_DIR

def setup_logger():
    """Sets up centralized, structured logging for the application."""
    log_file = os.path.join(LOGS_DIR, 'app.log')
    
    logger = logging.getLogger('AI_Career_Intelligence')
    
    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Format includes timestamp, level, module name, and message
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(module)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

app_logger = setup_logger()
