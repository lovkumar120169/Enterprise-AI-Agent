import time
from functools import wraps

from backend.utils.logging import logger


def retry(
    max_attempts: int = 2,
    delay_seconds: float = 0.5
):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            last_error = None

            for attempt in range(1, max_attempts + 1):

                try:
                    return func(*args, **kwargs)

                except Exception as error:

                    last_error = error

                    logger.warning(
                        "Attempt %s/%s failed for %s: %s",
                        attempt,
                        max_attempts,
                        func.__name__,
                        error
                    )

                    if attempt < max_attempts:
                        time.sleep(
                            delay_seconds * attempt
                        )

            raise last_error

        return wrapper

    return decorator