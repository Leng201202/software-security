"""Offline real-signature checks; no registry, model, login or listener.
python3 check_student.py
"""
from pathlib import Path
import base64
import json
import tempfile
import unittest
import student_task as task
PACKET = Path(__file__).with_name("signature-core")
META = json.loads((PACKET / "manifest.json").read_text())

class TrustControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="software-signature-check-")
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        for name in ["artifact.sig", "other-signer.sig"]:
            (self.dir / name).write_bytes(base64.b64decode((PACKET / (name + ".b64")).read_text(), validate=True))

    def test_trusted_positive(self):
        self.assertTrue(task.verify_artifact(PACKET / "artifact.txt", self.dir / "artifact.sig", PACKET / "trusted-signer.pub", META["trusted_key_sha256"]))

    def test_tamper_negative(self):
        changed = self.dir / "changed.txt"
        changed.write_bytes((PACKET / "artifact.txt").read_bytes() + b"tampered")
        self.assertFalse(task.verify_artifact(changed, self.dir / "artifact.sig", PACKET / "trusted-signer.pub", META["trusted_key_sha256"]))

    def test_valid_signature_from_wrong_signer_is_rejected(self):
        self.assertFalse(task.verify_artifact(PACKET / "artifact.txt", self.dir / "other-signer.sig", PACKET / "other-signer.pub", META["trusted_key_sha256"]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
