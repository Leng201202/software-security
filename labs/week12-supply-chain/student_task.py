"""Offline artifact trust exercise using real RSA signatures and OpenSSL.
This is key-based verification, not a claim to simulate Sigstore OIDC identity.
Complete trusted_key(): a valid signature under an untrusted key is insufficient.
"""
from pathlib import Path
import subprocess

def trusted_key(public_key, expected_sha256):
    """Return whether the public-key FILE bytes match the issued trust pin."""
    raise NotImplementedError("check the issued public-key fingerprint")


def verify_artifact(artifact, signature, public_key, expected_sha256):
    if not trusted_key(public_key, expected_sha256):
        return False
    result = subprocess.run(["openssl", "dgst", "-sha256", "-verify", str(public_key),
                             "-signature", str(signature), str(artifact)],
                            capture_output=True, timeout=10)
    return result.returncode == 0
