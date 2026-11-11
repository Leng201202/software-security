"""Run this harness after editing student_patch.py; do not edit the harness."""
import secrets

from flask import Flask, Response, request
from student_patch import allow_post, render_comment, render_name

app = Flask(__name__)
COMMENTS = []
CSRF_TOKEN = secrets.token_urlsafe(32)


@app.route("/")
def index():
    resp = Response("<a href=/hello?name=you>hello</a> | <a href=/comments>comments</a>", mimetype="text/html")
    resp.set_cookie("session", "abc123", httponly=True, samesite="Strict")
    return resp


@app.route("/hello")
def hello():
    return Response("<h1>Hello, " + render_name(request.args.get("name", "world")) + "!</h1>", mimetype="text/html")


@app.route("/comments", methods=["GET", "POST"])
def comments():
    cookie = request.cookies.get("session")
    if cookie != "abc123":
        return Response("Session required", status=401)
    if request.method == "POST":
        if not allow_post(cookie, request.form.get("csrf_token", ""), CSRF_TOKEN):
            return Response("CSRF token required", status=403)
        COMMENTS.append(request.form.get("body", ""))
    body = '<form method=post><input name=body><input type=hidden name=csrf_token value="' + CSRF_TOKEN + '"><input type=submit value=Post></form><hr>'
    body += "".join("<div class=comment>" + render_comment(c) + "</div>" for c in COMMENTS)
    return Response("<h2>Comments</h2>" + body, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
