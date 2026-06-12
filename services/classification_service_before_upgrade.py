def classify_deal(category: str):
    heavy_keywords = ["equipment", "factory", "mining", "plant", "drilling", "heavy"]
    return any(k in category.lower() for k in heavy_keywords)
