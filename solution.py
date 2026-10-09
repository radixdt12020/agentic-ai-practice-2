from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    """Least Recently Used (LRU) Cache implementation."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity: int = capacity
        self._cache: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve an item from the cache. Returns None if the key is not found."""
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert or update an item in the cache, evicting the LRU item if capacity is exceeded."""
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    def __len__(self) -> int:
        """Return the current number of items in the cache."""
        return len(self._cache)

    def __contains__(self, key: Any) -> bool:
        """Check if a key exists in the cache without updating its access order."""
        return key in self._cache
