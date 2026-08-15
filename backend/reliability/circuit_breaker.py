import time


class CircuitBreaker:

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 30
    ):

        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.opened_at = None

    @property
    def is_open(self) -> bool:

        if self.opened_at is None:
            return False

        elapsed = (
            time.time() - self.opened_at
        )

        if elapsed >= self.recovery_timeout:

            self.failure_count = 0
            self.opened_at = None

            return False

        return True

    def before_call(self):

        if self.is_open:

            raise RuntimeError(
                "Circuit breaker is open."
            )

    def record_success(self):

        self.failure_count = 0
        self.opened_at = None

    def record_failure(self):

        self.failure_count += 1

        if (
            self.failure_count
            >= self.failure_threshold
        ):

            self.opened_at = time.time()