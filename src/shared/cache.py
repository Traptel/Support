import json
from typing import Any

import redis
from django.conf import settings


class CacheService:
    def __init__(self, connection_url: str = settings.CACHE_URL) -> None:
        self.connection = redis.Redis.from_url(connection_url)

    def _build_key(self, namespace: str, key: Any) -> str:
        return f"{namespace}:{key}"

    def save(
        self, namespace: str, key: Any, instance: dict, ttl: int | None = None
    ) -> None:
        payload: str = json.dumps(instance)

        self.connection.set(self._build_key(namespace, key), payload, ex=ttl)

    def get(self, namespace: str, key: Any) -> dict:
        result: str = self.connection.get(self._build_key(namespace, key))
        return json.loads(result)

    def delete(self, namespace: str, key: Any) -> None:
        self.connection.delete(self._build_key(namespace, str(key)))
