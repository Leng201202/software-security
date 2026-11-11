"""Week 6 provided HTTP harness for two student-written security decisions."""
import datetime
import os
import jwt
from flask import Flask, request, jsonify
import student_patch

app = Flask(__name__)
SECRET = os.environ.get("JWT_SECRET") or os.urandom(32).hex()
AUDIENCE = "week06-student-lab"
USERS = {"alice": "alicepw", "bob": "bobpw"}
ORDERS = {1: {"owner": "alice", "item": "Laptop"}, 2: {"owner": "bob", "item": "Phone"}}


@app.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    user = body.get("user")
    if not isinstance(user, str) or user not in USERS or USERS[user] != body.get("pw"):
        return jsonify(error="bad credentials"), 401
    claims = {"sub": user, "aud": AUDIENCE, "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)}
    return jsonify(token=jwt.encode(claims, SECRET, algorithm="HS256"))


def current_user():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise jwt.InvalidTokenError("Bearer token required")
    return student_patch.decode_identity(header[7:], SECRET, AUDIENCE)


@app.get("/api/orders/<int:oid>")
def order(oid):
    try:
        user = current_user()
    except jwt.InvalidTokenError:
        return jsonify(error="invalid token"), 401
    item = ORDERS.get(oid)
    if item is None:
        return jsonify(error="not found"), 404
    if not student_patch.owns_order(user, item):
        return jsonify(error="forbidden"), 403
    return jsonify(item)


@app.get("/api/admin")
def admin():
    try:
        user = current_user()
    except jwt.InvalidTokenError:
        return jsonify(error="invalid token"), 401
    return (jsonify(ok=True), 200) if user == "admin" else (jsonify(error="forbidden"), 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
