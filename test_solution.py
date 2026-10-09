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
    assert cache.get("c") is None
    assert cache.get("c", default="missing") == "missing"


def test_eviction_order():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    # Access 'a' to make 'b' the least recently used
    assert cache.get("a") == 1
    # Insert 'c', which should evict 'b'
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_update_existing_key():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    # Updating 'a' marks it as recently used and changes its value
    cache.put("a", 10)
    cache.put("c", 3)  # Evicts 'b'
    assert cache.get("a") == 10
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_delete():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.delete("a") is True
    assert cache.get("a") is None
    assert cache.delete("nonexistent") is False


def test_clear_and_len():
    cache = LRUCache(3)
    assert len(cache) == 0
    cache.put("a", 1)
    cache.put("b", 2)
    assert len(cache) == 2
    assert "a" in cache
    assert "x" not in cache
    cache.clear()
    assert len(cache) == 0
    assert "a" not in cache
