import logging

from tinyscaf.util.logging_config import configure_logging


def test_configure_logging():
    configure_logging(log_level=True)
    logger = logging.getLogger()
    assert logger.level == logging.DEBUG
    assert logger.level != logging.INFO
