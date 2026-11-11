"""Student API control task. Local sandbox; X-User-Id is a supplied identity
fixture, not real authentication. Complete the two policy functions yourself.
Run the checks through Flask's in-process client; no listener is started.
"""

def may_read_orders(caller_id, target_id, is_admin):
    """Permit an authenticated fixture user to read own orders, or an admin."""
    raise NotImplementedError("implement object-level authorization")


def bind_creation_fields(body):
    """Return only username/password; server sets id, balance and is_admin."""
    raise NotImplementedError("implement allow-list binding")


def create_app():
    from flask import Flask, jsonify, request
    app = Flask(__name__)
    users = {1: {"is_admin": False}, 2: {"is_admin": False}, 3: {"is_admin": True}}

    @app.get("/api/users/<int:uid>/orders")
    def orders(uid):
        try:
            caller_id = int(request.headers.get("X-User-Id", "0"))
        except ValueError:
            caller_id = 0
        caller = users.get(caller_id)
        if caller is None:
            return jsonify(error="authentication fixture required"), 401
        if not may_read_orders(caller_id, uid, caller["is_admin"]):
            return jsonify(error="forbidden"), 403
        return jsonify(owner=uid, orders=["bounded teaching example"]), 200

    @app.post("/api/users")
    def create_user():
        safe = bind_creation_fields(request.get_json(silent=True) or {})
        if not safe.get("username") or not safe.get("password"):
            return jsonify(error="username and password required"), 400
        safe.update(id=4, is_admin=False, balance=0)
        return jsonify(safe), 201

    return app
