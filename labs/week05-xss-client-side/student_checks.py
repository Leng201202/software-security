"""Functional controls for the student's patch; run with python student_checks.py."""
import html

from student_patch import allow_post, render_comment, render_name


def check_render(fn):
    assert fn("Alice") == "Alice", "Legitimate text must remain readable"
    for payload in ("<script>alert(1)</script>", '<img src=x onerror=alert(1)>'):
        result = fn(payload)
        assert "<script" not in result and "<img" not in result, "HTML tags must render as text"
        assert payload in html.unescape(result), "Do not drop user text"


check_render(render_name)
check_render(render_comment)
assert allow_post("abc123", "known-token", "known-token"), "Valid session and token must work"
assert not allow_post(None, "known-token", "known-token"), "Missing session must fail"
assert not allow_post("wrong-session", "known-token", "known-token"), "Wrong session must fail"
assert not allow_post("abc123", "", "known-token"), "Missing token must fail"
assert not allow_post("abc123", "", ""), "Empty submitted and expected tokens must fail"
assert not allow_post("abc123", "wrong", "known-token"), "Wrong token must fail"
print("Week 5 controls passed")
