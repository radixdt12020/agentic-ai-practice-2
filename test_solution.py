import pytest
from solution import LRUCache


def test_init_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-5)


def test_put_and_get():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_get_missing_key():
    cache = LRUCache(2)
    assert cache.get("nonexistent") is None
    assert cache.get("nonexistent", default=-1) == -1


def test_eviction_policy():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # Evicts 'a'
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_get_updates_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    # Accessing 'a' makes 'b' the least recently used
    assert cache.get("a") == 1
    cache.put("c", 3)  # Should evict 'b'
    assert cache.get("a") == 1
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_update_existing_key():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)  # Updates 'a' and marks it recent
    cache.put("c", 3)   # Should evict 'b'
    assert cache.get("a") == 10
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_remove():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.remove("a") is True
    assert cache.remove("a") is False
    assert cache.get("a") is None
    assert len(cache) == 0


def test_clear():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.clear()
    assert len(cache) == 0
    assert cache.get("a") is None
    assert cache.get("b") is None


def test_len_and_contains():
    cache = LRUCache(2)
    assert len(cache) == 0
    assert "a" not in cache
    cache.put("a", 1)
    assert len(cache) == 1
    assert "a" in cache
    cache.put("b", 2)
    assert len(cache) == 2
