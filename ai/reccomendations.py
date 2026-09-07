def recommend(data):
    heat = data["heat"]
    vegetation = data["vegetation"]
    built_up = data["built_up"]
    population = data["population"]
    road_density = data.get("road_density", 0)

    recommendations = []

    if heat > 70 and vegetation < 30:
        recommendations.append({
            "name": "Tree Planting / Green Corridor",
            "reason": "High heat combined with low vegetation.",
            "priority": "High"
        })

    if heat > 70 and built_up > 70:
        recommendations.append({
            "name": "Cool Roofs",
            "reason": "High heat and high built-up intensity.",
            "priority": "High"
        })

    if heat > 70 and road_density > 60:
        recommendations.append({
            "name": "Roadside Shade",
            "reason": "High heat and high road exposure.",
            "priority": "Medium"
        })

    if heat > 70 and population > 70:
        recommendations.append({
            "name": "Priority Cooling Intervention",
            "reason": "High heat affects a large population.",
            "priority": "High"
        })

    return recommendations
