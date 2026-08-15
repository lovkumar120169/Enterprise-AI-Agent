import hashlib
import time
from typing import Any


class TTLCache:

    def __init__(
        self,
        ttl_seconds: int = 300
    ):

        self.ttl_seconds = ttl_seconds

        self._cache: dict[
            str,
            tuple[float, Any]
        ] = {}

    @staticmethod
    def _key(value: str) -> str:

        return hashlib.sha256(
            value.strip().lower().encode(
                "utf-8"
            )
        ).hexdigest()

    def get(self, value: str):

        key = self._key(value)

        item = self._cache.get(key)

        if item is None:
            return None

        created_at, result = item

        if (
            time.time() - created_at
            > self.ttl_seconds
        ):

            del self._cache[key]

            return None

        return result

    def set(
        self,
        value: str,
        result: Any
    ):

        key = self._key(value)

        self._cache[key] = (
            time.time(),
            result
        )

    def clear(self):

        self._cache.clear()