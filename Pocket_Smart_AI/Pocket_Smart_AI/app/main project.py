from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "pocket-smart-secret-key"


# =========================
# HOME PAGE
# =========================

@app.route("/")
def index():
    return render_template("index.html")


# =========================
# WELCOME
# =========================

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


# =========================
# PLANNERS
# =========================

@app.route("/planners")
def planners():
    return render_template("planners.html")


# =========================
# HOME BUDGET PLANNER
# =========================

@app.route("/home", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        budget = request.form.get("budget", "")
        rooms = request.form.get("rooms", "")
        home_type = request.form.get("home_type", "")
        additional = request.form.get("additional", "")

        requirements = request.form.getlist("requirements")

        session["home_data"] = {
            "budget": budget,
            "rooms": rooms,
            "home_type": home_type,
            "requirements": requirements,
            "additional": additional
        }

        return redirect(url_for("home_recommendations"))

    return render_template("home.html")


@app.route("/home/recommendations")
def home_recommendations():

    data = session.get("home_data", {})

    return render_template(
        "home.html",
        show_results=True,
        budget=data.get("budget", "Not specified"),
        rooms=data.get("rooms", "Not specified"),
        home_type=data.get("home_type", "Not specified"),
        requirements=data.get("requirements", []),
        additional=data.get("additional", "")
    )


# =========================
# PARTY BUDGET PLANNER
# =========================

@app.route("/party", methods=["GET", "POST"])
def party():

    if request.method == "POST":

        budget = request.form.get("budget", "")
        guests = request.form.get("guests", "")
        event_type = request.form.get("event_type", "")
        venue = request.form.get("venue", "")
        additional = request.form.get("additional", "")

        requirements = request.form.getlist("requirements")

        session["party_data"] = {
            "budget": budget,
            "guests": guests,
            "event_type": event_type,
            "venue": venue,
            "requirements": requirements,
            "additional": additional
        }

        return redirect(url_for("party_recommendations"))

    return render_template("party.html")


@app.route("/party/recommendations")
def party_recommendations():

    data = session.get("party_data", {})

    return render_template(
        "party.html",
        show_results=True,
        budget=data.get("budget", "Not specified"),
        guests=data.get("guests", "Not specified"),
        event_type=data.get("event_type", "Not specified"),
        venue=data.get("venue", "Not specified"),
        requirements=data.get("requirements", []),
        additional=data.get("additional", "")
    )


# =========================
# JEWELLERY BUDGET PLANNER
# =========================

@app.route("/jewellery", methods=["GET", "POST"])
def jewellery():

    if request.method == "POST":

        budget = request.form.get("budget", "")
        occasion = request.form.get("occasion", "")
        style = request.form.get("style", "")
        additional = request.form.get("additional", "")

        outfit = request.files.get("outfit")

        session["jewellery_data"] = {
            "budget": budget,
            "occasion": occasion,
            "style": style,
            "additional": additional,
            "outfit": outfit.filename if outfit else ""
        }

        return redirect(url_for("jewellery_recommendations"))

    return render_template("jewellery.html")


@app.route("/jewellery/recommendations")
def jewellery_recommendations():

    data = session.get("jewellery_data", {})

    return render_template(
        "jewellery.html",
        show_results=True,
        budget=data.get("budget", "Not specified"),
        occasion=data.get("occasion", "Not specified"),
        style=data.get("style", "Not specified"),
        additional=data.get("additional", "")
    )


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:

            session["user"] = username

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Please enter username and password."
        )

    return render_template("login.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        if not username or not email or not password:

            return render_template(
                "register.html",
                error="Please fill in all fields."
            )

        session["user"] = username

        return redirect(url_for("dashboard"))

    return render_template("register.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    user = session.get("user", "User")

    return render_template(
        "dashboard.html",
        username=user
    )


# =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    return render_template("history.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )