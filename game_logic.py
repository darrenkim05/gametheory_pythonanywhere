# Use (user_move, ai_move): (user_score, ai_score)
PAYOFF_MATRIX = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}

def init_game(opponents_list):
    return {
        "current_opponent_index": 0,
        "opponents": opponents_list,
        "current_opponent": opponents_list[0],
        "round": 1,
        "user_score": 0,
        "ai_score": 0,
        "user_moves": [],
        "ai_moves": [],
        "completed_opponents": [],
        "game_over": False,
        "round_history": [],
        "results": []
    }

def evaluate_round(user_move, ai_move):
    return PAYOFF_MATRIX.get((user_move, ai_move), (0, 0))

def update_game_state(game_state, user_move, ai_move):
    user_points, ai_points = evaluate_round(user_move, ai_move)

    game_state["user_moves"].append(user_move)
    game_state["ai_moves"].append(ai_move)
    game_state["user_score"] += user_points
    game_state["ai_score"] += ai_points
    game_state["round_history"].append((game_state["round"], user_move, ai_move))
    game_state["round"] += 1

    if game_state["round"] >= 25:
        advance_opponent(game_state)

    return game_state

def advance_opponent(game_state):
        # Save the current opponent's results
    game_state["results"].append({
        "opponent": game_state["current_opponent"],
        "user_score": game_state["user_score"],
        "ai_score": game_state["ai_score"],
        "user_moves": game_state["user_moves"][:],
        "ai_moves": game_state["ai_moves"][:]
    })

    game_state["completed_opponents"].append(game_state["current_opponent"])
    game_state["current_opponent_index"] += 1

    if game_state["current_opponent_index"] < len(game_state["opponents"]):
        game_state["current_opponent"] = game_state["opponents"][game_state["current_opponent_index"]]
        game_state["round"] = 1
        game_state["user_score"] = 0
        game_state["ai_score"] = 0
        game_state["user_moves"] = []
        game_state["ai_moves"] = []
        game_state["round_history"] = []
    else:
        game_state["game_over"] = True

def calculate_total_user_score(game_state):
    """
    Calculate the cumulative score for the user across all opponents.
    """
    results = game_state.get("results", [])
    return sum(result.get("user_score", 0) for result in results)
