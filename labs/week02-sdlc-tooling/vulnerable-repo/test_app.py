"""Regression tests for the remediated Week 2 application."""

import os
import sqlite3
import tempfile
import unittest
from unittest import mock

import app as vulnerable_app


class RemediationTests(unittest.TestCase):
    def setUp(self):
        database = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.database_path = database.name
        database.close()

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
            )
            connection.executemany(
                "INSERT INTO users (name) VALUES (?)",
                [("alice",), ("bob",)],
            )

        self.path_patch = mock.patch.object(
            vulnerable_app, "DB_PATH", self.database_path
        )
        self.path_patch.start()
        vulnerable_app.app.config.update(TESTING=True)
        self.client = vulnerable_app.app.test_client()

    def tearDown(self):
        self.path_patch.stop()
        os.unlink(self.database_path)

    def test_user_lookup_uses_parameterized_query(self):
        response = self.client.get("/user", query_string={"name": "alice"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("alice", response.get_data(as_text=True))

        injection = self.client.get(
            "/user", query_string={"name": "' OR 1=1 --"}
        )
        self.assertEqual(injection.status_code, 200)
        self.assertEqual(injection.get_data(as_text=True), "[]")

    @mock.patch.object(vulnerable_app.subprocess, "run")
    def test_ping_passes_an_argument_list_without_a_shell(self, run):
        run.return_value = vulnerable_app.subprocess.CompletedProcess(
            args=["ping", "-c", "1", "127.0.0.1"],
            returncode=0,
            stdout="reachable\n",
        )

        response = self.client.get("/ping", query_string={"host": "127.0.0.1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "reachable\n")
        run.assert_called_once_with(
            ["ping", "-c", "1", "127.0.0.1"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )

    @mock.patch.object(vulnerable_app.subprocess, "run")
    def test_ping_rejects_command_injection(self, run):
        response = self.client.get(
            "/ping", query_string={"host": "127.0.0.1; id"}
        )

        self.assertEqual(response.status_code, 400)
        run.assert_not_called()

    def test_passwords_use_argon2_and_verify(self):
        stored_hash = vulnerable_app.store_password("correct horse battery staple")

        self.assertTrue(stored_hash.startswith("$argon2id$"))
        self.assertTrue(
            vulnerable_app.verify_password(stored_hash, "correct horse battery staple")
        )
        self.assertFalse(vulnerable_app.verify_password(stored_hash, "wrong password"))

    def test_secrets_must_come_from_the_environment(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                vulnerable_app.external_credentials()

        supplied = {
            "AWS_SECRET_ACCESS_KEY": "test-aws-value",
            "DB_PASSWORD": "test-db-value",
        }
        with mock.patch.dict(os.environ, supplied, clear=True):
            self.assertEqual(
                vulnerable_app.external_credentials(),
                {
                    "aws_secret_access_key": "test-aws-value",
                    "db_password": "test-db-value",
                },
            )


if __name__ == "__main__":
    unittest.main()
