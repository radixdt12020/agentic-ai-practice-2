import base64
import hmac
import hashlib
import json
import os
import secrets
import time
from typing import Any, Dict, Optional

# Default secret key generated securely per process or loaded from environment
_DEFAULT_SECRET: bytes = os.environ.get("AUTH_TOKEN_SECRET", "").encode("utf-8") or secrets.token_bytes(32)
_current_secret: bytes = _DEFAULT_SECRET


def set_secret_key(secret: bytes | str) -> None:
    """Update the secret key used for signing and verifying tokens."""
    global _current_secret
    if isinstance(secret, str):
        _current_secret = secret.encode("utf-8")
    elif isinstance(secret, (bytes, bytearray)):
        _current_secret = bytes(secret)
    else:
        raise TypeError("Secret key must be bytes or str.")


def reset_secret_key() -> None:
    """Reset secret key to the default process secret."""
    global _current_secret
    _current_secret = _DEFAULT_SECRET


def _b64url_encode(data: bytes) -> str:
    """Encode bytes into URL-safe base64 string without trailing padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    """Decode URL-safe base64 string handling stripped padding."""
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data.encode("ascii"))


def generate_secure_token(user_id: str, expires_in: int = 3600) -> str:
    """
    Creates an unforgeable, cryptographically secure bearer token.

    Args:
        user_id: Unique identifier for the user (non-empty string).
        expires_in: Token lifetime in seconds (defaults to 3600).

    Returns:
        Cryptographically signed bearer token string.
    """
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("user_id must be a non-empty string")

    now = int(time.time())
    payload: Dict[str, Any] = {
        "sub": user_id,
        "iat": now,
        "exp": now + int(expires_in),
        "nonce": secrets.token_hex(16),
    }

    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    encoded_payload = _b64url_encode(payload_bytes)

    signature = hmac.new(
        _current_secret,
        encoded_payload.encode("ascii"),
        hashlib.sha256
    ).digest()
    encoded_sig = _b64url_encode(signature)

    return f"{encoded_payload}.{encoded_sig}"


def verify_token(token: str, clock_skew: int = 60) -> bool:
    """
    Validates token integrity and ensures it has not expired.

    Args:
        token: The bearer token to validate.
        clock_skew: Allowed clock drift in seconds (default: 60).

    Returns:
        True if token is authentic and valid, False otherwise.
    """
    return decode_token(token, clock_skew=clock_skew) is not None


def decode_token(token: str, clock_skew: int = 60) -> Optional[Dict[str, Any]]:
    """
    Validates token integrity and returns payload if valid, otherwise None.
    """
    if not isinstance(token, str) or not token:
        return None

    parts = token.split(".")
    if len(parts) != 2:
        return None

    encoded_payload, encoded_sig = parts

    try:
        expected_sig = hmac.new(
            _current_secret,
            encoded_payload.encode("ascii"),
            hashlib.sha256
        ).digest()
        provided_sig = _b64url_decode(encoded_sig)
    except Exception:
        return None

    if not hmac.compare_digest(expected_sig, provided_sig):
        return None

    try:
        payload_raw = _b64url_decode(encoded_payload)
        payload = json.loads(payload_raw.decode("utf-8"))
    except Exception:
        return None

    if not isinstance(payload, dict):
        return None

    user_id = payload.get("sub")
    exp = payload.get("exp")
    iat = payload.get("iat")

    if not isinstance(user_id, str) or not user_id.strip():
        return None
    if not isinstance(exp, (int, float)) or not isinstance(iat, (int, float)):
        return None

    now = time.time()
    if now > exp:
        return None
    if iat > now + clock_skew:
        return None

    return payload
