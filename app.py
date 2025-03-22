import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session

from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from game_logic import init_game, update_game_state, calculate_total_user_score
from strategies import get_strategy, STRATEGIES  # ensure full STRATEGIES is imported


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQL("sqlite:////home/darrenkim05/mysite/gametheory/finance.db")
STRATEGY_DESCRIPTIONS = {row["name"]: row["description"] for row in db.execute("SELECT * FROM strategy_explanations")}

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def home(): 
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        if not request.form.get("username"):
            return apology("must provide username")
        
        elif not request.form.get("password"):
            return apology("must provide password")

        else:
            # check if password and confirmation matches
            if request.form.get("password") != request.form.get("confirmation"):
                return apology("password and confirmation doesn't match")

            else:
                # check if username is already taken
                if len(db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))) != 0:
                    return apology("Username already taken")
                else:
                    password_hash = generate_password_hash(request.form.get("password"))

                    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                               request.form.get("username"), password_hash)

                    return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    if "game" not in session:
        import random
        all_opponents = list(STRATEGIES.keys())
        random.shuffle(all_opponents)
        session["game"] = init_game(all_opponents[:5])  # pick 5 random strategies
        session.modified = True

    game = session["game"]

    if request.method == "POST":
        print("METHOD:", request.method)

        user_move = request.form.get("move")
        if user_move not in ["C", "D"]:
            return apology("Invalid move")

        if not game or game.get("game_over"):
            return redirect("/result")

        strategy_func = get_strategy(game["current_opponent"])
        ai_move = strategy_func(game["user_moves"], game["ai_moves"])

        game = update_game_state(game, user_move, ai_move)
        session["game"] = game
        session.modified = True

        if game.get("game_over"):
            print(game["results"])
            return redirect("/result")
            

    return render_template("play.html", game=session["game"])

@app.route("/clear", methods=["POST"])
@login_required
def clear():
    session.pop("game", None)
    return redirect("/play")

@app.route("/explanation")
def explanation():
    if request.method == 'POST':
            return apology("TODO")
    else:
        return render_template("explanation.html")

@app.route("/history")
@login_required
def history():
    rows = db.execute(
        """
        
        SELECT timestamp,
               SUM(rounds_played) AS total_rounds,
               SUM(user_score) AS total_score,
               GROUP_CONCAT(opponent, ', ') AS opponents
        FROM games
        WHERE user_id = ?
        GROUP BY timestamp
        ORDER BY timestamp DESC
    """, session["user_id"])
    return render_template("history.html", games=rows)

@app.route("/result")
@login_required
def result():
    game = session.get("game")

    if not game or not game.get("game_over"):
        return redirect("/play")

    results = game.get("results", [])
    total_score = calculate_total_user_score(game)

    # Save to database if not already saved
    for match in results:
        db.execute(
            "INSERT INTO games (user_id, opponent, rounds_played, user_score, opponent_score) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            match["opponent"],
            len(match["user_moves"]),
            match["user_score"],
            match["ai_score"]
        )

    # Clear the session so duplicate inserts don't occur on refresh
    session.pop("game", None)

    return render_template("result.html", results=results, total_score=total_score, strategy_descriptions=STRATEGY_DESCRIPTIONS)

@app.route("/insights")
def insights():
    return render_template("insights.html")

@app.route("/highscores")
def highscores():
    scores = db.execute(
        """
        SELECT users.username, MAX(session_scores.total_score) AS high_score
        FROM users
        JOIN (
            SELECT user_id, timestamp, SUM(user_score) AS total_score
            FROM games
            GROUP BY user_id, timestamp
        ) AS session_scores ON users.id = session_scores.user_id
        GROUP BY users.username
        ORDER BY high_score DESC
        """
    )
    return render_template("highscores.html", scores=scores)
