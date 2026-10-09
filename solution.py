from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    """
    A thread-unsafe Least Recently Used (LRU) Cache.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self._cache: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        """Retrieve an item from the cache. Returns default if key is not found."""
        if key not in self._cache:
            return default
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: Any, value: Any) -> None:
        """Insert or update an item in the cache, evicting the LRU item if at capacity."""
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    def delete(self, key: Any) -> bool:
        """Remove an item from the cache. Returns True if removed, False otherwise."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all items from the cache."""
        self._cache.clear()

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key: Any) -> bool:
        return key in self._cache
