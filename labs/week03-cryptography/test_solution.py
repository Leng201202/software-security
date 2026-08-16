import hashlib
import os
import unittest
from unittest.mock import patch

from solution_skeleton import (
    decrypt_gcm,
    encrypt_gcm,
    load_encryption_key,
    reset_token,
    store_password,
    verify_and_upgrade,
    verify_password,
)


class CryptoSolutionTests(unittest.TestCase):
    def test_password_hash_and_verify(self):
        stored_hash = store_password("correct horse battery staple")
        self.assertTrue(stored_hash.startswith("$argon2id$"))
        self.assertTrue(verify_password(stored_hash, "correct horse battery staple"))
        self.assertFalse(verify_password(stored_hash, "wrong password"))

    def test_legacy_md5_is_upgraded_only_after_valid_login(self):
        legacy = hashlib.md5(b"password123").hexdigest()
        valid, replacement = verify_and_upgrade(legacy, "password123")
        self.assertTrue(valid)
        self.assertIsNotNone(replacement)
        self.assertTrue(replacement.startswith("$argon2id$"))

        invalid, no_replacement = verify_and_upgrade(legacy, "wrong")
        self.assertFalse(invalid)
        self.assertIsNone(no_replacement)

    def test_gcm_round_trip_and_tamper_rejection(self):
        key = bytes.fromhex("11" * 32)
        nonce, ciphertext, tag = encrypt_gcm(b"top secret", key)
        self.assertEqual(len(nonce), 12)
        self.assertEqual(decrypt_gcm(nonce, ciphertext, tag, key), b"top secret")

        tampered = bytes([ciphertext[0] ^ 1]) + ciphertext[1:]
        with self.assertRaises(ValueError):
            decrypt_gcm(nonce, tampered, tag, key)

    def test_gcm_uses_a_fresh_nonce(self):
        key = bytes.fromhex("22" * 32)
        first_nonce, _, _ = encrypt_gcm(b"same message", key)
        second_nonce, _, _ = encrypt_gcm(b"same message", key)
        self.assertNotEqual(first_nonce, second_nonce)

    def test_key_must_come_from_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                load_encryption_key()

        with patch.dict(os.environ, {"ENC_KEY_HEX": "not-hex"}, clear=True):
            with self.assertRaises(ValueError):
                load_encryption_key()

        with patch.dict(os.environ, {"ENC_KEY_HEX": "aa" * 16}, clear=True):
            with self.assertRaises(ValueError):
                load_encryption_key()

        with patch.dict(os.environ, {"ENC_KEY_HEX": "aa" * 32}, clear=True):
            self.assertEqual(load_encryption_key(), bytes.fromhex("aa" * 32))

    def test_reset_token_is_long_and_url_safe(self):
        token = reset_token()
        self.assertGreaterEqual(len(token), 21)
        self.assertRegex(token, r"^[A-Za-z0-9_-]+$")


if __name__ == "__main__":
    unittest.main()
