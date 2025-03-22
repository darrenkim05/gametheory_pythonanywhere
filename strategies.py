import random

def always_cooperate(user_history, ai_history):
    """Always cooperate."""
    return "C"

def always_defect(user_history, ai_history):
    """Always defect."""
    return "D"

def tit_for_tat(user_history, ai_history):
    """Cooperate on the first move, then mimic opponent's last move."""
    if not user_history:
        return "C"
    return user_history[-1]

def grudger(user_history, ai_history):
    """Cooperate unless the opponent has defected at least once."""
    if "D" in user_history:
        return "D"
    return "C"

def random_strategy(user_history, ai_history):
    """Choose randomly between cooperation and defection."""
    return random.choice(["C", "D"])

def grim_trigger(user_history, ai_history):
    """Cooperate until opponent defects once, then always defect."""
    if "D" in user_history:
        return "D"
    return "C"

def tit_for_two_tats(user_history, ai_history):
    """Defect only if opponent defects twice in a row."""
    if len(user_history) >= 2 and user_history[-1] == "D" and user_history[-2] == "D":
        return "D"
    return "C"

def pavlov(user_history, ai_history):
    """Repeat last move if both players did the same; switch otherwise."""
    if not ai_history or not user_history:
        return "C"
    if user_history[-1] == ai_history[-1]:
        return ai_history[-1]
    return "C" if ai_history[-1] == "D" else "D"

def suspicious_tit_for_tat(user_history, ai_history):
    """Start with defection, then mimic opponent’s last move."""
    if not user_history:
        return "D"
    return user_history[-1]

def generous_tit_for_tat(user_history, ai_history):
    """Tit for Tat with occasional forgiveness."""
    if not user_history:
        return "C"
    if user_history[-1] == "D" and random.random() < 0.3:
        return "C"
    return user_history[-1]

def prober(user_history, ai_history):
    """Defect early to test, then switch to Tit for Tat."""
    probing_moves = ["D", "C", "C"]
    if len(ai_history) < 3:
        return probing_moves[len(ai_history)]
    if "D" not in user_history[:3]:
        return user_history[-1]
    else:
        return "D"

# Strategy registry


def get_strategy(name):
    """Retrieve a strategy by name."""
    return STRATEGIES.get(name)

def joss(user_history, ai_history):
    """Tit for Tat with occasional random defection (10%)."""
    if not user_history:
        return "C"
    if user_history[-1] == "C":
        return "D" if random.random() < 0.1 else "C"
    return "D"

def spiteful(user_history, ai_history):
    """Defects for 3 rounds after a defection, then forgives."""
    if not hasattr(spiteful, "punish_timer"):
        spiteful.punish_timer = 0
    if "D" in user_history[-1:]:
        spiteful.punish_timer = 3
    if spiteful.punish_timer > 0:
        spiteful.punish_timer -= 1
        return "D"
    return "C"

def hit_and_run(user_history, ai_history):
    """Defect for first 5 rounds, then cooperate forever."""
    return "D" if len(ai_history) < 5 else "C"

def tricky_alternator(user_history, ai_history):
    """Alternates C/D, but defects twice if opponent cooperated twice in a row."""
    if len(user_history) >= 2 and user_history[-1] == "C" and user_history[-2] == "C":
        return "D"
    return "C" if len(ai_history) % 2 == 0 else "D"

def two_timer(user_history, ai_history):
    """Defects every third round, otherwise cooperates."""
    return "D" if (len(ai_history) + 1) % 3 == 0 else "C"

def anti_tit_for_tat(user_history, ai_history):
    """Defects if opponent cooperated, cooperates if opponent defected."""
    if not user_history:
        return "C"
    return "D" if user_history[-1] == "C" else "C"

def cycle_breaker(user_history, ai_history):
    """Breaks a repeating C/D pattern if detected."""
    if len(ai_history) >= 4 and ai_history[-4:] == ["C", "D", "C", "D"]:
        return "D"
    return "C"

def stubborn_defector(user_history, ai_history):
    """Defect first 10 rounds, then cooperate if opponent always cooperated."""
    if len(ai_history) < 10:
        return "D"
    if all(move == "C" for move in user_history[:10]):
        return "C"
    return "D"

def disloyal_friend(user_history, ai_history):
    """Acts like Tit for Tat, but randomly flips sides every 5 rounds."""
    if not user_history:
        return "C"
    if len(user_history) % 5 == 0:
        return "C" if user_history[-1] == "D" else "D"
    return user_history[-1]

def mirror_mirror(user_history, ai_history):
    """Always does the opposite of its own last move."""
    if not ai_history:
        return "C"
    return "D" if ai_history[-1] == "C" else "C"



def people_pleaser(user_history, ai_history):
    """Cooperate unless opponent defects twice in a row, then defect once and forgive."""
    if len(user_history) >= 2 and user_history[-1] == "D" and user_history[-2] == "D":
        return "D"
    return "C"

def opportunist(user_history, ai_history):
    """Defects if opponent cooperates 4 times in a row, then goes back to cooperating."""
    if len(user_history) >= 4 and user_history[-4:] == ["C", "C", "C", "C"]:
        return "D"
    return "C"

def guilt_tripper(user_history, ai_history):
    """Defects twice in response to a defection, then returns to cooperation."""
    if len(user_history) >= 1 and user_history[-1] == "D":
        return "D"
    if len(user_history) >= 2 and user_history[-2] == "D":
        return "D"
    return "C"

def slow_learner(user_history, ai_history):
    """Cooperates first 10 rounds, then mimics opponent’s most common move so far."""
    if len(user_history) < 10:
        return "C"
    return "C" if user_history[:10].count("C") >= user_history[:10].count("D") else "D"

def backstabber(user_history, ai_history):
    """Tit for Tat with a 1-in-7 chance of betrayal."""
    if not user_history:
        return "C"
    if random.randint(1, 7) == 1:
        return "D"
    return user_history[-1]

def mirror_narcissist(user_history, ai_history):
    """Mimics the opponent’s overall majority behavior."""
    if not user_history:
        return "C"
    return "C" if user_history.count("C") >= user_history.count("D") else "D"

def flatterer(user_history, ai_history):
    """Copies opponent’s move and does the opposite on the next round."""
    if len(user_history) < 2:
        return "C"
    return "D" if user_history[-2] == "C" else "C"

def standoffish(user_history, ai_history):
    """Defects unless it’s every 3rd round."""
    return "C" if len(ai_history) % 3 == 2 else "D"

def detective(user_history, ai_history):
    """Starts C, D, C, D to test opponent, then switches to Tit-for-Tat or Grudger."""
    probe_sequence = ["C", "D", "C", "D"]
    if len(ai_history) < len(probe_sequence):
        return probe_sequence[len(ai_history)]
    if "D" in user_history[:4]:
        return "D"
    return user_history[-1]

def peacemaker(user_history, ai_history):
    """Defects only if opponent has defected 3+ times. Never defects more than twice in a row."""
    if user_history.count("D") >= 2 and user_history[-1] == "D" and user_history[-2] == "D":
        return "C"
    return "D" if user_history.count("D") >= 3 else "C"

STRATEGIES = {
    #"always_cooperate": always_cooperate,
    #"always_defect": always_defect,
    "tit_for_tat": tit_for_tat,
    "grudger": grudger,
    "random": random_strategy,
    "grim_trigger": grim_trigger,
    "tit_for_two_tats": tit_for_two_tats,
    "pavlov": pavlov,
    "suspicious_tit_for_tat": suspicious_tit_for_tat,
    "generous_tit_for_tat": generous_tit_for_tat,
    "prober": prober,
    "joss": joss,
    "spiteful": spiteful,
    "hit_and_run": hit_and_run,
    "tricky_alternator": tricky_alternator,
    "two_timer": two_timer,
    "anti_tit_for_tat": anti_tit_for_tat,
    "cycle_breaker": cycle_breaker,
    "stubborn_defector": stubborn_defector,
    "disloyal_friend": disloyal_friend,
    "mirror_mirror": mirror_mirror,
    "people_pleaser": people_pleaser,
    "opportunist": opportunist,
    "guilt_tripper": guilt_tripper,
    "slow_learner": slow_learner,
    "backstabber": backstabber,
    "mirror_narcissist": mirror_narcissist,
    "flatterer": flatterer,
    "standoffish": standoffish,
    "detective": detective,
    "peacemaker": peacemaker
}
