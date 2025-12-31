import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# class AppLogger:
#     def __init__(self, log_file: str = "app.log", max_bytes: int = 1_000_000, backup_count: int = 5):
#         self.logger = logging.getLogger("AppLogger")
#         self.logger.setLevel(logging.DEBUG)

#         # Create log directory if it doesn't exist
#         log_path = Path(log_file).parent
#         log_path.mkdir(parents=True, exist_ok=True)

#         # Create a rotating file handler
#         handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
#         handler.setLevel(logging.DEBUG)

#         # Create a logging format
#         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         handler.setFormatter(formatter)

#         # Add the handler to the logger
#         self.logger.addHandler(handler)

#     def get_logger(self):
#         return self.logger  
    

# class AppLogger1:
#     def __init__(self, log_file: str = "app.log", 
#                  max_bytes = 5*1024*1024,
#                  backup_count = 5):
#         self.logger = logging.getLogger(__class__.__name__)
#         self.logger.setLevel(logging.INFO)

#         log_path = Path(log_file).parent/"logs"
#         log_path.mkdir(parents=True, exist_ok=True)

#         handler = RotatingFileHandler(log_path / log_file,
#                                       maxBytes=max_bytes,
#                                       backupCount=backup_count)
#         handler.setLevel(logging.INFO)

#         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         handler.setFormatter(formatter)

#         self.logger.addHandler(handler)

#     def get_logger(self, name: str):
#         return self.logger

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import inspect

class AppLogger1:
    _loggers = {}

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Returns a logger with module + class context automatically attached.
        """
        # Inspect caller
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        module_name = module.__name__ if module else "unknown"

        # Try to get class name (if called from class)
        class_name = frame.frame.f_locals.get("self", None)
        if class_name:
            logger_name = f"{module_name}.{class_name.__class__.__name__}"
        else:
            logger_name = module_name

        # Reuse logger if already created
        if logger_name in cls._loggers:
            return cls._loggers[logger_name]

        # Create logs directory
        log_dir = Path(__name__).parent/"logs"
        log_dir.mkdir(exist_ok=True)

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Prevent duplicate handlers
        if not logger.handlers:
            file_handler = RotatingFileHandler(
                log_dir / "app.log",
                maxBytes=5 * 1024 * 1024,
                backupCount=5
            )
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        cls._loggers[logger_name] = logger
        return logger
