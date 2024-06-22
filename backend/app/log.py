import logging
from colorlog import ColoredFormatter


logger = logging.getLogger('LOG')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()

formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
