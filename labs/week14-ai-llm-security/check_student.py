"""Deterministic output-control tests; no model or account required."""
import unittest
import student_task as task
SECRET = "FLAG{local_output_control}"

class OutputControls(unittest.TestCase):
    def test_legitimate_text(self):
        self.assertEqual(task.render_model_output("Hello, student", SECRET), "Hello, student")

    def test_script_is_text(self):
        out = task.render_model_output('<script>alert(1)</script>', SECRET)
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)

    def test_secret_redacted_before_sink(self):
        out = task.render_model_output("Echo " + SECRET, SECRET)
        self.assertNotIn(SECRET, out)
        self.assertIn("[REDACTED]", out)

    def test_mixed_and_ampersand(self):
        out = task.render_model_output('<img src=x onerror=alert(1)>' + SECRET + ' & hello', SECRET)
        self.assertNotIn("<img", out)
        self.assertNotIn(SECRET, out)
        self.assertIn("&amp; hello", out)

if __name__ == "__main__":
    unittest.main(verbosity=2)
