"""This deterministic command can be the red/green job step in a prepared CI repo."""
import unittest
import student_task as task

def lookup(token):
    return {"alice-token": "alice", "bob-token": "bob"}.get(token)

def broken(_token):
    raise RuntimeError("sensitive upstream detail: local-example-token")

class GateControls(unittest.TestCase):
    def test_legitimate_admin(self):
        self.assertTrue(task.authorize(lookup, "alice-token", {"alice"}))

    def test_missing_unknown_nonadmin(self):
        for token in [None, "", "unknown-token", "bob-token"]:
            self.assertFalse(task.authorize(lookup, token, {"alice"}))

    def test_lookup_failure_denies(self):
        self.assertFalse(task.authorize(broken, "alice-token", {"alice"}))

    def test_safe_log_fields(self):
        self.assertEqual(task.event_fields(True), {"outcome": "allow"})
        err = RuntimeError("sensitive upstream detail: local-example-token")
        record = task.event_fields(False, err)
        self.assertEqual(record, {"outcome": "deny", "error_type": "RuntimeError"})
        self.assertNotIn("local-example-token", repr(record))

if __name__ == "__main__":
    unittest.main(verbosity=2)
