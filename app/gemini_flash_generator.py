def generate_nutrition_tip(goal, intensity):

    tips = [
        "Drink enough water throughout the day and include a variety of nutritious foods in your regular meals.",
        "Try to include fruits, vegetables, whole grains and protein-rich foods as part of balanced meals.",
        "Stay hydrated and give your body enough time to rest and recover after physical activity.",
        "Choose regular balanced meals and snacks that help you stay energized throughout the day.",
        "Good sleep, hydration and balanced meals are important parts of a healthy fitness routine."
    ]

    goal_text = str(goal).lower()
    intensity_text = str(intensity).lower()

    if "strength" in goal_text:
        return (
            "Include balanced meals with protein-rich foods, "
            "whole grains, fruits and vegetables. Stay hydrated "
            "and allow enough time for recovery."
        )

    if "energy" in goal_text or "fitness" in goal_text:
        return (
            "Stay hydrated and choose balanced meals with "
            "fruits, vegetables, whole grains and protein-rich foods."
        )

    if intensity_text == "high":
        return (
            "Stay well hydrated and make sure you eat regular "
            "balanced meals. Rest and recovery are also important."
        )

    return tips[0]