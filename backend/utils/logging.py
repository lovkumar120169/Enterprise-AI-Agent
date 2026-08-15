import logging
import sys
from contextvars import ContextVar


request_id_context = ContextVar(
    "request_id",
    default="-"
)


class RequestIdFilter(logging.Filter):

    def filter(self, record):

        record.request_id = (
            request_id_context.get()
        )

        return True


def setup_logger():

    logger = logging.getLogger(
        "enterprise_ai_agent"
    )

    logger.setLevel(
        logging.DEBUG
    )

    logger.handlers.clear()

    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.setLevel(
        logging.DEBUG
    )

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "request_id=%(request_id)s | "
        "%(message)s"
    )

    handler.setFormatter(
        formatter
    )

    handler.addFilter(
        RequestIdFilter()
    )

    logger.addHandler(
        handler
    )

    logger.propagate = False

    return logger


logger = setup_logger()


logger.info(
    "========== LOGGER INITIALIZED =========="
)