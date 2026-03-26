import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger() -> logging.Logger:
    logger = logging.getLogger('BinanceTestnetBot')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    #Now we have to prevent the duplicate handlers
    if not logger.handlers:

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            filename='bot.log',
            mode='a',
            maxBytes=5*1024*1024,
            backupCount=3,
        )

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.propagate = False

    return logger

logger = setup_logger()
    