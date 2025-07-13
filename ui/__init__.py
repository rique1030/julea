import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

__all__ = ['logger']

from .ui import UserInterface
