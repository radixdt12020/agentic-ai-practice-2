import hashlib
import json
from typing import Any, Dict, Tuple


def create_session(user_data: Dict[str, Any]) -> Tuple[str, bytes]:
    """Serialize user data using JSON and generate a SHA-256 session ID.

    Args:
        user_data: Dictionary containing user session data.

    Returns:
        A tuple of (64-character session ID string, serialized bytes).
    """
    if not isinstance(user_data, dict):
        raise TypeError("user_data must be a dict")

    try:
        serialized_bytes = json.dumps(user_data, sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Failed to serialize user_data: {exc}") from exc

    session_id = hashlib.sha256(serialized_bytes).hexdigest()
    return session_id, serialized_bytes


def restore_session(serialized_bytes: bytes) -> Dict[str, Any]:
    """Deserialize user session data safely from bytes using JSON.

    Args:
        serialized_bytes: Serialized bytes produced by JSON encoding.

    Returns:
        Deserialized user data dictionary.
    """
    if not isinstance(serialized_bytes, (bytes, bytearray)):
        raise TypeError("serialized_bytes must be bytes or bytearray")

    try:
        decoded_str = serialized_bytes.decode("utf-8")
        user_data = json.loads(decoded_str)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid session data: {exc}") from exc

    if not isinstance(user_data, dict):
        raise TypeError("Deserialized data is not a dict")

    return user_data
