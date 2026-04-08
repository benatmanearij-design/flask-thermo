from flask import Flask, render_template, request
from database import init_db
from models import insert_operation, get_history

app = Flask(__name__)

init_db()

# ---------------- DASHBOARD ----------------
@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        try:
            x1 = float(request.form.get("x1"))
            x2 = float(request.form.get("x2"))
            P1 = float(request.form.get("P1"))
            P2 = float(request.form.get("P2"))

            P = x1 * P1 + x2 * P2

            if P == 0:
                return render_template(
                    "result.html",
                    valid=False,
                    message="❌ P = 0 → division par zéro impossible"
                )

            y1 = (x1 * P1) / P
            y2 = (x2 * P2) / P

            valid = True
            message = ""

            if abs((x1 + x2) - 1) > 1e-6:
                valid = False
                message = "❌ x1 + x2 ≠ 1 (la somme doit être égale à 1)"

            elif abs((y1 + y2) - 1) > 1e-6:
                valid = False
                message = "❌ y1 + y2 ≠ 1 (erreur dans le calcul)"

            else:
                message = "✅ Résultat valide ✔"

            insert_operation(x1, x2, P1, P2, P, y1, y2)

            return render_template(
                "result.html",
                P=round(P, 4),
                y1=round(y1, 4),
                y2=round(y2, 4),
                sum=round(y1 + y2, 4),
                valid=valid,
                message=message
            )

        except Exception:
            return render_template(
                "result.html",
                valid=False,
                message="❌ Valeurs invalides"
            )

    return render_template("dashboard.html")


# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    data = get_history()
    return render_template("history.html", data=data)


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)