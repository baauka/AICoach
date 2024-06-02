def calculate_bmr(gender, weight, height, age):
    if gender == 'Male':
        return (weight*10) + (height*6.25) - (age*5) + 5
    else:
        return (weight*10) + (height*6.25) - (age*5) - 161


def get_activity_level_multiplier(activity):
    activity_levels = {
        'Sedentary(little or no exercise)': 1.25,
        'Light(light exercise/sports 1-3 days​/week)': 1.375,
        'Moderate(moderate exercise/sports 3-5 days/week)': 1.55,
        'Active(hard exercise/sports 6-7 days a week)': 1.725,
    }
    return activity_levels.get(activity)

def calculate_caloric_needs(bmr, multiplier):
    maintain = round(bmr * multiplier)
    lose_250 = maintain - 250
    lose_500 = maintain - 500
    lose_1000 = maintain - 1000
    
    return {
        "maintain": maintain,
        "lose_250": lose_250,
        "lose_500": lose_500,
        "lose_1000": lose_1000
    }


def total_calculation_calorie(bmr, activity):
    multiplier = get_activity_level_multiplier(activity)
    needs = calculate_caloric_needs(bmr, multiplier)
    
    return (
        f"You need to eat {needs['maintain']} calories a day to maintain your current weight. \n"
        f"You need to eat {needs['lose_250']} calories a day to lose 250 gram per week. \n"
        f"You need to eat {needs['lose_500']} calories a day to lose 500 gram per week. \n"
        f"You need to eat {needs['lose_1000']} calories a day to lose 1 kg per week."
    )
