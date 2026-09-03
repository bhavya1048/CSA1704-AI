# Custom forward-chaining rule engine
# Rules are based on the rule structure described in the report.

RULES = [
    {
        "id": "R1",
        "disease": "Healthy",
        "cf": 0.95,
        "condition": lambda f: (
            f["lesion_area"] == "low" and
            f["lesion_colour"] == "none"
        ),
        "description": "Low lesion area + no lesion colour"
    },
    {
        "id": "R2",
        "disease": "Early Blight",
        "cf": 0.80,
        "condition": lambda f: (
            f["lesion_colour"] == "brown" and
            f["lesion_shape"] in ["compact", "irregular"]
        ),
        "description": "Brown lesions + structured/irregular shape"
    },
    {
        "id": "R3",
        "disease": "Early Blight",
        "cf": 0.60,
        "condition": lambda f: (
            f["halo_colour"] == "yellow"
        ),
        "description": "Yellow halo detected"
    },
    {
        "id": "R4",
        "disease": "Late Blight",
        "cf": 0.75,
        "condition": lambda f: (
            f["lesion_colour"] == "dark-green/brown" and
            f["texture"] == "water-soaked"
        ),
        "description": "Dark green/brown lesions + rough water-soaked texture"
    },
    {
        "id": "R5",
        "disease": "Late Blight",
        "cf": 0.70,
        "condition": lambda f: (
            f["edge_growth"] == "white-mould"
        ),
        "description": "White mould-like edge condition"
    },
    {
        "id": "R6",
        "disease": "Bacterial Spot",
        "cf": 0.70,
        "condition": lambda f: (
            f["lesion_shape"] == "angular" and
            f["lesion_count"] == "high"
        ),
        "description": "Angular lesions + high lesion count"
    }
]

def combine_cf(old, new):
    """MYCIN-style combination for positive certainty factors."""
    return old + new * (1 - old)

def diagnose(facts):
    scores = {}
    fired = []

    # Forward chaining: check every rule against current facts
    for rule in RULES:
        if rule["condition"](facts):
            disease = rule["disease"]

            if disease not in scores:
                scores[disease] = 0.0

            scores[disease] = combine_cf(scores[disease], rule["cf"])

            fired.append(
                f'{rule["id"]}: {rule["description"]} -> '
                f'{disease} (CF={rule["cf"]:.2f})'
            )

    if not scores:
        return "Unknown / Needs Expert Review", 0.0, fired

    disease = max(scores, key=scores.get)
    cf = scores[disease]

    # Minimum acceptance threshold from the report
    if cf < 0.50:
        disease = "Unknown / Needs Expert Review"

    return disease, cf, fired
