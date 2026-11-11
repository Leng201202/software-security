"""Reference defense for the isolated Week 5 lab, not production authentication."""
import secrets

from flask import Flask, Response, render_template_string, request
from markupsafe import escape

app = Flask(__name__)
COMMENTS = []
SESSION = "abc123"  # Sandbox identity only; production sessions must be random and per user.
CSRF_TOKEN = secrets.token_urlsafe(32)


def secure(resp: Response) -> Response:
    resp.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none'"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    return secure(Response("<h1>Hello, " + str(escape(name)) + "!</h1>", mimetype="text/html"))


@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.cookies.get("session") != SESSION:
        return secure(Response("Session required", status=401, mimetype="text/plain"))
    if request.method == "POST":
        submitted = request.form.get("csrf_token", "")
        if not secrets.compare_digest(submitted, CSRF_TOKEN):
            return secure(Response("CSRF token required", status=403, mimetype="text/plain"))
        COMMENTS.append(request.form.get("body", ""))
    page = render_template_string("""<h2>Comments</h2>
    <form method=post><input name=body><input type=hidden name=csrf_token value="{{ token }}"><input type=submit value=Post></form><hr>
    {% for c in comments %}<div class=comment>{{ c }}</div>{% endfor %}""",
                                  comments=COMMENTS, token=CSRF_TOKEN)
    return secure(Response(page, mimetype="text/html"))


@app.route("/")
def index():
    resp = Response("<a href=/hello?name=you>hello</a> | <a href=/comments>comments</a>", mimetype="text/html")
    # Secure requires HTTPS in a deployment. Loopback HTTP is used only for this lab.
    resp.set_cookie("session", SESSION, httponly=True, samesite="Strict")
    return secure(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
