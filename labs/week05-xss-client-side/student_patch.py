"""Week 5 student work: replace the three intentionally unsafe returns."""


def render_name(value: str) -> str:
    """Return text safe to insert into an HTML text node."""
    return value  # TODO: encode for HTML text context


def render_comment(value: str) -> str:
    """Return text safe to insert into an HTML text node."""
    return value  # TODO: encode for HTML text context


def allow_post(session_cookie: str | None, submitted_token: str, expected_token: str) -> bool:
    """Accept a comment only for the lab session with the matching secret token."""
    return True  # TODO: check session and compare the two tokens safely
