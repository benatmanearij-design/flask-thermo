from flask import Flask, render_template, request, redirect, session, url_for
from database import init_db
from models import (
    create_user,
    check_user,
    get_user_by_email,
    update_password_by_email,
    insert_operation,
    get_history
)
import random

app = Flask(__name__)
app.secret_key = "arij_secret_key"

init_db()

reset_codes = {}
requests_count = {}


@app.before_request
def limit_requests():
    ip = request.remote_addr
    requests_count[ip] = requests_count.get(ip, 0) + 1
    if requests_count[ip] > 300:
        return "Too many requests from this IP"


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if check_user(username, password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Wrong username or password"

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm", "").strip()

        if not username or not email or not password or not confirm:
            error = "Please fill in all fields"
        elif password != confirm:
            error = "Passwords do not match"
        elif create_user(username, email, password):
            return redirect(url_for("login"))
        else:
            error = "User or email already exists"

    return render_template("register.html", error=error)


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    message = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user = get_user_by_email(email)

        if user:
            code = str(random.randint(100000, 999999))
            reset_codes[email] = code
            message = f"Confirmation code: {code}"
        else:
            message = "Email not found"

    return render_template("forgot_password.html", message=message)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        code = request.form.get("code", "").strip()
        new_password = request.form.get("new_password", "").strip()

        if reset_codes.get(email) == code:
            update_password_by_email(email, new_password)
            reset_codes.pop(email, None)
            return redirect(url_for("login"))
        else:
            error = "Invalid confirmation code"

    return render_template("reset_password.html", error=error)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    error = None
    ip = request.remote_addr

    if request.method == "POST":
        try:
            x1_text = request.form.get("x1", "").strip()
            x2_text = request.form.get("x2", "").strip()
            p1_text = request.form.get("P1", "").strip()
            p2_text = request.form.get("P2", "").strip()

            if not x1_text or not x2_text or not p1_text or not p2_text:
                error = "Please fill in all fields"
                return render_template("dashboard.html", username=session["username"], error=error, ip=ip)

            x1 = float(x1_text)
            x2 = float(x2_text)
            p1 = float(p1_text)
            p2 = float(p2_text)

            P = x1 * p1 + x2 * p2

            if P == 0:
                error = "P total cannot be zero"
                return render_template("dashboard.html", username=session["username"], error=error, ip=ip)

            y1 = (x1 * p1) / P
            y2 = (x2 * p2) / P

            insert_operation(session["username"], x1, x2, p1, p2, P, y1, y2)

            chart_labels = ["P", "y1", "y2"]
            chart_values = [round(P, 4), round(y1, 4), round(y2, 4)]

            return render_template(
                "result.html",
                P=round(P, 4),
                y1=round(y1, 4),
                y2=round(y2, 4),
                ip=ip,
                chart_labels=chart_labels,
                chart_values=chart_values
            )

        except ValueError:
            error = "Use numbers only, for example 0.4 and 25.16"
        except Exception as e:
            error = f"Error: {e}"

    return render_template("dashboard.html", username=session["username"], error=error, ip=ip)


@app.route("/history")
def history():
    if "username" not in session:
        return redirect(url_for("login"))

    data = get_history(session["username"])
    return render_template("history.html", data=data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)