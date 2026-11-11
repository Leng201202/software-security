"""Bounded local policy checks, NOT AWS IAM policy simulation.
It understands only the Allow/Action/Resource/StringLike subset in this task;
SCPs, boundaries, explicit Deny and AWS context are not implemented.
"""
import fnmatch
import unittest
import student_task as task

def allowed(policy, action, resource, prefix=None):
    for s in policy.get("Statement", []):
        if s.get("Effect") != "Allow":
            continue
        actions = s.get("Action", [])
        resources = s.get("Resource", [])
        if isinstance(actions, str): actions = [actions]
        if isinstance(resources, str): resources = [resources]
        if not any(fnmatch.fnmatchcase(action, p) for p in actions): continue
        if not any(fnmatch.fnmatchcase(resource, p) for p in resources): continue
        condition = s.get("Condition", {})
        if condition:
            patterns = condition.get("StringLike", {}).get("s3:prefix", [])
            if isinstance(patterns, str): patterns = [patterns]
            if prefix is None or not any(fnmatch.fnmatchcase(prefix, p) for p in patterns): continue
        return True
    return False

class PolicyControls(unittest.TestCase):
    def setUp(self):
        self.policy = task.build_policy("lab-app-bucket", "app/")

    def test_positive_get_and_list(self):
        self.assertTrue(allowed(self.policy, "s3:GetObject", "arn:aws:s3:::lab-app-bucket/app/file.txt"))
        self.assertTrue(allowed(self.policy, "s3:ListBucket", "arn:aws:s3:::lab-app-bucket", "app/"))

    def test_other_prefix_and_bucket_denied(self):
        self.assertFalse(allowed(self.policy, "s3:GetObject", "arn:aws:s3:::lab-app-bucket/private/file.txt"))
        self.assertFalse(allowed(self.policy, "s3:GetObject", "arn:aws:s3:::other-bucket/app/file.txt"))
        self.assertFalse(allowed(self.policy, "s3:ListBucket", "arn:aws:s3:::lab-app-bucket", "private/"))

    def test_mutation_action_denied(self):
        self.assertFalse(allowed(self.policy, "s3:DeleteObject", "arn:aws:s3:::lab-app-bucket/app/file.txt"))
        self.assertFalse(allowed(self.policy, "s3:PutObject", "arn:aws:s3:::lab-app-bucket/app/file.txt"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
