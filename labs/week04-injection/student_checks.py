"""Run in the prebuilt image: docker compose run --rm --no-deps --pull never injection-lab python student_checks.py. No listener or actual ping is used."""
import subprocess
import unittest
from unittest.mock import patch
import student_app


class PatchChecks(unittest.TestCase):
    def setUp(self):
        self.client = student_app.app.test_client()

    def test_legitimate_login_and_wrong_password(self):
        self.assertIn(b"Welcome alice", self.client.get("/login?user=alice&pw=alicepw").data)
        self.assertEqual(self.client.get("/login?user=alice&pw=wrong").status_code, 401)

    def test_sql_values_cannot_change_the_query(self):
        for name in ["alice'--", "' OR 1=1--", "bob' UNION SELECT 1,'admin'--"]:
            with self.subTest(username=name):
                self.assertEqual(self.client.get("/login", query_string={"user": name, "pw": "wrong"}).status_code, 401)

    def test_ping_control_uses_an_argument_list_without_a_shell(self):
        with patch.object(student_app.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "one reply", "")) as runner:
            response = self.client.get("/ping?host=127.0.0.1")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(runner.call_args.args[0], ["ping", "-c", "1", "127.0.0.1"])
            self.assertIs(runner.call_args.kwargs["shell"], False)

    def test_injected_or_invalid_host_never_starts_a_process(self):
        with patch.object(student_app.subprocess, "run") as runner:
            for host in ["127.0.0.1;id", "127.0.0.1 && id", "-c 99", "localhost", "999.2.3.4", ""]:
                with self.subTest(host=host):
                    self.assertEqual(self.client.get("/ping", query_string={"host": host}).status_code, 400)
            runner.assert_not_called()


if __name__ == "__main__":
    unittest.main()
