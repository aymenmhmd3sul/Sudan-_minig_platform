def classify_deal(category: str):
    category = category.lower()
    score = 0

    if "mining" in category:
        score += 3
    if "drilling" in category:
        score += 3
    if "plant" in category:
        score += 2
    if "equipment" in category:
        score += 2
    if "factory" in category:
        score += 2
    if "heavy" in category:
        score += 1

    return score >= 3
