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


def test_eviction_order():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # 'a' is accessed, making 'b' least recently used
    cache.put("c", 3)  # Evicts 'b'
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_update_existing_key():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)  # Update 'a'
    cache.put("c", 3)   # Should evict 'b'
    assert cache.get("a") == 10
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_capacity_one():
    cache = LRUCache(1)
    cache.put("x", 100)
    assert cache.get("x") == 100
    cache.put("y", 200)
    assert cache.get("x") is None
    assert cache.get("y") == 200


def test_len_and_contains():
    cache = LRUCache(3)
    assert len(cache) == 0
    assert "a" not in cache
    cache.put("a", 1)
    assert len(cache) == 1
    assert "a" in cache
