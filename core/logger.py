import logging
from rich.logging import RichHandler

def setup_logger(name=__name__):
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        handlers=[RichHandler()]
    )
    return logging.getLogger(name)
