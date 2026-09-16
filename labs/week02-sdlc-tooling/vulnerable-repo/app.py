"""Remediated Week 2 sample application."""
import ipaddress
import os
import sqlite3
import subprocess

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from flask import Flask, request

app = Flask(__name__)
ph = PasswordHasher()
DB_PATH = os.environ.get("APP_DB_PATH", "app.db")


def required_secret(name):
    """Load a required secret without providing an insecure fallback value."""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} must be provided through the environment")
    return value


def external_credentials():
    """Load credentials only at the point where an external service needs them."""
    return {
        "aws_secret_access_key": required_secret("AWS_SECRET_ACCESS_KEY"),
        "db_password": required_secret("DB_PASSWORD"),
    }

@app.route("/user")
def user():
    name = request.args.get("name", "")
    with sqlite3.connect(DB_PATH) as con:
        rows = con.execute(
            "SELECT * FROM users WHERE name = ?",
            (name,),
        ).fetchall()
    return str(rows)

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    try:
        # This endpoint only needs IP literals. Restricting the input also prevents
        # command-option injection such as a hostname beginning with "-".
        ipaddress.ip_address(host)
    except ValueError:
        return "invalid IP address", 400

    try:
        result = subprocess.run(
            ["ping", "-c", "1", host],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "host unreachable", 502
    return result.stdout


def store_password(pw):
    return ph.hash(pw)


def verify_password(stored_hash, pw):
    try:
        return ph.verify(stored_hash, pw)
    except (InvalidHashError, VerificationError, VerifyMismatchError):
        return False

if __name__ == "__main__":
    app.run(debug=False)
