import hashlib
import json
import pytest
from solution import create_session, restore_session


def test_create_and_restore_session_roundtrip():
    data = {"user_id": 123, "username": "alice", "is_admin": False}
    session_id, serialized = create_session(data)

    # Session ID should be 64-character SHA-256 hex digest
    assert len(session_id) == 64
    assert session_id == hashlib.sha256(serialized).hexdigest()

    restored = restore_session(serialized)
    assert restored == data


def test_create_session_type_error():
    with pytest.raises(TypeError, match="user_data must be a dict"):
        create_session("not_a_dict")  # type: ignore

    with pytest.raises(TypeError, match="user_data must be a dict"):
        create_session([1, 2, 3])  # type: ignore


def test_restore_session_invalid_bytes_type():
    with pytest.raises(TypeError, match="serialized_bytes must be bytes or bytearray"):
        restore_session("not_bytes")  # type: ignore


def test_restore_session_invalid_json():
    with pytest.raises(ValueError, match="Invalid session data"):
        restore_session(b"invalid-json-data")


def test_restore_session_non_dict_json():
    non_dict_serialized = json.dumps([1, 2, 3]).encode("utf-8")
    with pytest.raises(TypeError, match="Deserialized data is not a dict"):
        restore_session(non_dict_serialized)


def test_restore_session_rejects_pickle_payload():
    # Attempt to pass a pickle payload; it should fail safely rather than execute code
    pickle_payload = b"\x80\x04\x95\x0f\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x01a\x94K\x01s."
    with pytest.raises(ValueError):
        restore_session(pickle_payload)
