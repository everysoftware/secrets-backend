"""Mocked Redis."""
from typing import Any, Optional

from redis.asyncio.client import Redis


class MockedRedis(Redis):
    """Mocked Redis for unittests."""

    data = {}

    async def get(self, name: str) -> Optional[str]:
        """Get value from mocked storage."""
        return self.data.get(name)

    async def set(self, name: str, value: Any, *_) -> Optional[bool]:
        """Set key-value pair in mocked storage."""
        self.data[name] = value
        return True

    async def delete(self, name: str) -> bool:
        if not self.exists(name):
            return False

        self.data.pop(name)
        return True

    async def exists(self, name: str) -> int:
        """Check if keys are exists in mocked storage."""
        return name in self.data
