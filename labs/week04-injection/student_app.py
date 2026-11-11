"""Small student-patched target for the Week 4 core; provided harness, not a solution."""
import sqlite3
import subprocess
from flask import Flask, request, jsonify
import student_patch

app = Flask(__name__)


def connect():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    con.executemany("INSERT INTO users VALUES (?, ?, ?)", [(1, "alice", "alicepw"), (2, "bob", "bobpw")])
    return con


@app.get("/login")
def login():
    with connect() as con:
        row = student_patch.authenticate(con, request.args.get("user", ""), request.args.get("pw", ""))
    return ("Welcome " + row[1] + "\n") if row else ("Login failed\n", 401)


@app.get("/ping")
def ping():
    try:
        argv = student_patch.ping_argv(request.args.get("host", "127.0.0.1"))
    except ValueError:
        return jsonify(error="invalid IPv4 address"), 400
    # The harness owns process execution. A list is data, never a shell program.
    if not isinstance(argv, list) or len(argv) != 4 or argv[:3] != ["ping", "-c", "1"]:
        return jsonify(error="patch must return the specified argv list"), 400
    result = subprocess.run(argv, shell=False, capture_output=True, text=True, timeout=5)
    return jsonify(output=result.stdout + result.stderr, exit_code=result.returncode)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
