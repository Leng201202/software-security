"""Student task: complete the two bounded injection defenses. Sandbox only."""


def authenticate(connection, username: str, password: str):
    """Return the matching (id, username) row or None.

    Bind the two values as SQLite parameters. Do not format input into SQL.
    The supplied connection has a users(id, username, password) table.
    """
    raise NotImplementedError("TODO: parameterized authentication query")


def ping_argv(host: str) -> list[str]:
    """Return ['ping', '-c', '1', host] for a single IPv4 address.

    This bounded task accepts IPv4 addresses, including 127.0.0.1, only.
    Reject command separators, extra arguments, hostnames and invalid addresses
    with ValueError. The caller always uses shell=False.
    """
    raise NotImplementedError("TODO: validate one IPv4 address and return argv")
