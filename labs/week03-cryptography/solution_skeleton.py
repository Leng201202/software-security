"""
Week 3 — FIX the misuse here. Fill in the TODOs.
pip install argon2-cffi pycryptodome
"""
import hashlib
import hmac
import os
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from Crypto.Cipher import AES


ph = PasswordHasher()

def store_password(pw: str) -> str:
    # FIX: argon2id, salted automatically
    return ph.hash(pw)

def verify_password(hash_: str, pw: str) -> bool:
    try:
        return ph.verify(hash_, pw)
    except (InvalidHashError, VerificationError, VerifyMismatchError):
        return False

def load_encryption_key() -> bytes:
    key_hex = os.environ.get("ENC_KEY_HEX")
    if not key_hex:
        raise RuntimeError("ENC_KEY_HEX must be set to a 32-byte hexadecimal key")
    try:
        key = bytes.fromhex(key_hex)
    except ValueError as exc:
        raise ValueError("ENC_KEY_HEX must contain hexadecimal characters only") from exc
    if len(key) != 32:
        raise ValueError("ENC_KEY_HEX must decode to exactly 32 bytes")
    return key

def encrypt_gcm(data: bytes, key: bytes) -> tuple[bytes, bytes, bytes]:
    # FIX: authenticated encryption (AES-GCM), random nonce, key from env/KMS
    nonce = secrets.token_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(data)
    return nonce, ct, tag

def decrypt_gcm(nonce: bytes, ct: bytes, tag: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ct, tag)

def reset_token() -> str:
    # FIX: CSPRNG
    return secrets.token_urlsafe(16)

def verify_and_upgrade(stored_hash: str, pw: str) -> tuple[bool, str | None]:
    if stored_hash.startswith("$argon2id"):
        if not verify_password(stored_hash, pw):
            return False, None
        if ph.check_needs_rehash(stored_hash):
            return True, store_password(pw)
        return True, None

    candidate = hashlib.md5(pw.encode()).hexdigest()
    if hmac.compare_digest(candidate, stored_hash):
        return True, store_password(pw)
    return False, None

if __name__ == "__main__":
    key = load_encryption_key()
    h = store_password("password123")
    print("argon2 ok:", verify_password(h, "password123"))
    legacy = hashlib.md5(b"password123").hexdigest()
    login_ok, upgraded = verify_and_upgrade(legacy, "password123")
    print("legacy login ok:", login_ok)
    print("upgraded to argon2id:", bool(upgraded and upgraded.startswith("$argon2id")))

    nonce, ciphertext, tag = encrypt_gcm(b"secret", key)
    print("gcm round-trip:", decrypt_gcm(nonce, ciphertext, tag, key))
    tampered = bytes([ciphertext[0] ^ 1]) + ciphertext[1:]
    try:
        decrypt_gcm(nonce, tampered, tag, key)
        print("tamper check: FAILED")
    except ValueError:
        print("tamper check: rejected")
    print("token:", reset_token())
