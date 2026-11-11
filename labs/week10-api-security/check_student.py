"""Run with the lab's Flask dependency installed: python3 check_student.py."""
import unittest
import student_task as task

class StudentControls(unittest.TestCase):
    def setUp(self):
        self.client = task.create_app().test_client()

    def test_missing_identity(self):
        self.assertEqual(self.client.get("/api/users/3/orders").status_code, 401)

    def test_own_and_other_objects(self):
        h = {"X-User-Id": "1"}
        self.assertEqual(self.client.get("/api/users/1/orders", headers=h).status_code, 200)
        self.assertEqual(self.client.get("/api/users/3/orders", headers=h).status_code, 403)

    def test_admin_control(self):
        self.assertEqual(self.client.get("/api/users/2/orders", headers={"X-User-Id": "3"}).status_code, 200)

    def test_server_fields_cannot_be_bound(self):
        body = {"username": "mallory", "password": "local-example", "is_admin": True, "balance": 999, "id": 3}
        bound = task.bind_creation_fields(body)
        self.assertEqual(bound, {"username": "mallory", "password": "local-example"})
        r = self.client.post("/api/users", json=body)
        self.assertEqual(r.status_code, 201)
        self.assertFalse(r.json["is_admin"])
        self.assertEqual(r.json["balance"], 0)
        self.assertEqual(r.json["id"], 4)

    def test_required_field_control(self):
        self.assertEqual(self.client.post("/api/users", json={"username": "m"}).status_code, 400)

if __name__ == "__main__":
    unittest.main(verbosity=2)
