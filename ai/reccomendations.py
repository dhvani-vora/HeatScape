def get_recommendation(heat, vegetation, built_up, population):

    scores = {
        "Tree Planting / Green Corridor": 0,
        "Cool Roofs": 0,
        "Roadside Shade": 0
    }

    if vegetation < 30:
        scores["Tree Planting / Green Corridor"] += 40

    if built_up > 70:
        scores["Cool Roofs"] += 40

    if heat > 70 and population > 70:
        scores["Roadside Shade"] += 20

    if heat > 70:
        scores["Cool Roofs"] += 20

    recommendation = max(scores, key=scores.get)

    reasons = {
        "Tree Planting / Green Corridor":
            "Low vegetation is the dominant cooling deficit.",

        "Cool Roofs":
            "High built-up intensity is a major contributor to heat.",

        "Roadside Shade":
            "High heat and population exposure make shaded public space a priority."
    }

    return recommendation, reasons[recommendation]
