import time
import pytest
from solution import (
    generate_secure_token,
    verify_token,
    decode_token,
    set_secret_key,
    reset_secret_key,
)


@pytest.fixture(autouse=True)
def reset_secret():
    """Ensure secret key is reset between tests."""
    reset_secret_key()
    yield
    reset_secret_key()


def test_valid_token_generation_and_verification():
    token = generate_secure_token("user_12345")
    assert isinstance(token, str)
    assert "." in token
    assert verify_token(token) is True

    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "user_12345"
    assert payload["exp"] > payload["iat"]


def test_token_uniqueness():
    # Tokens generated for the same user must differ due to nonce
    token1 = generate_secure_token("user_abc")
    token2 = generate_secure_token("user_abc")
    assert token1 != token2
    assert verify_token(token1) is True
    assert verify_token(token2) is True


def test_expired_token():
    token = generate_secure_token("user_expired", expires_in=-10)
    assert verify_token(token) is False
    assert decode_token(token) is None


def test_tampered_payload():
    token = generate_secure_token("alice")
    payload_b64, sig_b64 = token.split(".")

    # Tamper payload
    tampered_payload_b64 = payload_b64[:-1] + ("A" if payload_b64[-1] != "A" else "B")
    tampered_token = f"{tampered_payload_b64}.{sig_b64}"
    assert verify_token(tampered_token) is False


def test_tampered_signature():
    token = generate_secure_token("alice")
    payload_b64, sig_b64 = token.split(".")

    # Tamper signature
    tampered_sig_b64 = sig_b64[:-1] + ("X" if sig_b64[-1] != "X" else "Y")
    tampered_token = f"{payload_b64}.{tampered_sig_b64}"
    assert verify_token(tampered_token) is False


def test_secret_key_change_invalidates_token():
    token = generate_secure_token("bob")
    assert verify_token(token) is True

    set_secret_key("brand-new-secret-key-12345")
    assert verify_token(token) is False


def test_empty_and_invalid_user_id():
    with pytest.raises(ValueError):
        generate_secure_token("")

    with pytest.raises(ValueError):
        generate_secure_token("   ")

    with pytest.raises(ValueError):
        generate_secure_token(None)  # type: ignore

    with pytest.raises(ValueError):
        generate_secure_token(12345)  # type: ignore


@pytest.mark.parametrize(
    "bad_token",
    [
        "",
        None,
        123,
        "invalid_token_without_period",
        "too.many.dots.in.token",
        ".signature_only",
        "payload_only.",
        "!!!.???",
        "not_base64.not_base64",
    ],
)
def test_verify_malformed_tokens(bad_token):
    assert verify_token(bad_token) is False
    assert decode_token(bad_token) is None


def test_unicode_user_id():
    user_ids = ["ユーザー1", "admin@example.com", "🚀_space_user", "user-with-dashes.123"]
    for uid in user_ids:
        token = generate_secure_token(uid)
        assert verify_token(token) is True
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == uid


def test_token_expiration_over_time(monkeypatch):
    start_time = 1_000_000.0
    monkeypatch.setattr(time, "time", lambda: start_time)
    token = generate_secure_token("user_time", expires_in=100)
    assert verify_token(token) is True

    # Still valid right before expiry
    monkeypatch.setattr(time, "time", lambda: start_time + 99)
    assert verify_token(token) is True

    # Expired past expiry
    monkeypatch.setattr(time, "time", lambda: start_time + 101)
    assert verify_token(token) is False
