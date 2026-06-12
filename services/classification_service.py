def classify_deal(category: str, specs: str = ""):
    text = (category + " " + specs).lower()

    rules = {
        "mining": 4,
        "drilling": 4,
        "excavator": 4,
        "plant": 3,
        "factory": 3,
        "equipment": 3,
        "heavy": 2,
        "spare parts": 1,
        "parts": 1,
        "maintenance": 2
    }

    score = 0

    for keyword, weight in rules.items():
        if keyword in text:
            score += weight

    if len(text.split()) >= 3:
        score += 1

    return score >= 4
