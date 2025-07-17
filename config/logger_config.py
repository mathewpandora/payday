import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str = 'content_generation') -> logging.Logger:
    """Настройка логгера с записью в файл и выводом в консоль"""

    log_dir = Path("../logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


    file_handler = RotatingFileHandler(
        log_dir / 'generation.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()