"""Bounded fail-closed/logging patch. No server or GitHub request is made.
Call the supplied identity lookup; errors, unknown tokens and non-admins deny.
Record only a stable error type, never raw exception messages or tokens.
"""
def authorize(lookup_user, token, admins):
    raise NotImplementedError("implement fail-closed authorization")


def event_fields(allowed, error=None):
    raise NotImplementedError("produce a minimal safe allow/deny log record")
