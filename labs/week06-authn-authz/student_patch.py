"""Student task: authenticate tokens and authorize each object. Sandbox only."""


def decode_identity(token: str, secret: str, audience: str) -> str:
    """Return the authenticated subject or raise jwt.InvalidTokenError.

    Use PyJWT verification with HS256 as the only allowed algorithm, the supplied
    secret/audience, and required sub, exp and aud claims. Do not read claims with
    signature verification disabled. Never accept an unsigned token.
    """
    raise NotImplementedError("TODO: verify JWT and return authenticated sub")


def owns_order(user: str, order: dict) -> bool:
    """Return True only when the authenticated user owns this order."""
    raise NotImplementedError("TODO: enforce ownership for the requested object")
