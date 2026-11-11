"""Run: python student_checks.py. In-process clients; no network listener."""
import datetime
import unittest
import jwt
import student_app as target


class PatchChecks(unittest.TestCase):
    def setUp(self):
        self.client = target.app.test_client()

    def headers(self, token):
        return {"Authorization": "Bearer " + token}

    def real_token(self, user):
        return self.client.post("/login", json={"user": user, "pw": user + "pw"}).get_json()["token"]

    def test_owner_access_and_cross_user_denial(self):
        alice = self.real_token("alice")
        bob = self.real_token("bob")
        self.assertEqual(self.client.get("/api/orders/1", headers=self.headers(alice)).status_code, 200)
        self.assertEqual(self.client.get("/api/orders/2", headers=self.headers(alice)).status_code, 403)
        self.assertEqual(self.client.get("/api/orders/2", headers=self.headers(bob)).status_code, 200)
        self.assertEqual(self.client.get("/api/admin", headers=self.headers(alice)).status_code, 403)

    def test_no_token_is_not_an_identity(self):
        self.assertEqual(self.client.get("/api/orders/1").status_code, 401)

    def test_forgeries_and_invalid_claims_are_refused(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        good = {"sub": "bob", "aud": target.AUDIENCE, "exp": now + datetime.timedelta(minutes=5)}
        bad_tokens = [jwt.encode({"sub": "bob"}, "", algorithm="none"), jwt.encode(good, "secret", algorithm="HS256")]
        for changes in [{"aud": "another-app"}, {"exp": now - datetime.timedelta(minutes=5)}, {"sub": ""}]:
            bad_tokens.append(jwt.encode(good | changes, target.SECRET, algorithm="HS256"))
        for missing in ["sub", "exp", "aud"]:
            bad_tokens.append(jwt.encode({k: v for k, v in good.items() if k != missing}, target.SECRET, algorithm="HS256"))
        for token in bad_tokens:
            with self.subTest(token=token[:16]):
                self.assertEqual(self.client.get("/api/orders/2", headers=self.headers(token)).status_code, 401)
                self.assertEqual(self.client.get("/api/admin", headers=self.headers(token)).status_code, 401)


if __name__ == "__main__":
    unittest.main()
