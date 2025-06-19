from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# NutritionRecommendation Class
class NutritionRecommendation:
    def __init__(self, age, weight, height, gender, activity_level, goal, diet_type):
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender
        self.activity_level = activity_level
        self.goal = goal
        self.diet_type = diet_type

        self.bmr = self.calculate_bmr()
        self.calorie_needs = self.calculate_calorie_needs()
        self.macro_distribution = self.get_macronutrient_distribution()

    def calculate_bmr(self):
        if self.gender == 'male':
            return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            return 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)

    def calculate_calorie_needs(self):
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }

        calorie_needs = self.bmr * activity_multipliers.get(self.activity_level, 1.2)

        if self.goal == 'weight_loss':
            calorie_needs -= 500
        elif self.goal == 'muscle_gain':
            calorie_needs += 300

        return calorie_needs

    def get_macronutrient_distribution(self):
        if self.goal == 'weight_loss':
            return {'protein': 0.30, 'fat': 0.25, 'carb': 0.45}
        elif self.goal == 'muscle_gain':
            return {'protein': 0.35, 'fat': 0.25, 'carb': 0.40}
        else:
            return {'protein': 0.30, 'fat': 0.30, 'carb': 0.40}

    def display_recommendations(self):
        protein_grams = (self.calorie_needs * self.macro_distribution['protein']) / 4
        fat_grams = (self.calorie_needs * self.macro_distribution['fat']) / 9
        carb_grams = (self.calorie_needs * self.macro_distribution['carb']) / 4

        return {
            'calories': round(self.calorie_needs, 2),
            'protein': round(protein_grams, 2),
            'fat': round(fat_grams, 2),
            'carbs': round(carb_grams, 2)
        }

    def generate_meal_plan(self):
        meals = {
            'vegetarian': {
                'breakfast': ['Oats with almonds', 'Greek yogurt with berries'],
                'lunch': ['Lentil curry with rice', 'Quinoa salad with chickpeas'],
                'dinner': ['Vegetable pasta', 'Grilled tofu with veggies']
            },
            'non_vegetarian': {
                'breakfast': ['Eggs with spinach', 'Scrambled eggs with avocado'],
                'lunch': ['Chicken breast with quinoa', 'Grilled fish with veggies'],
                'dinner': ['Salmon with sweet potato', 'Beef stir-fry with broccoli']
            }
        }

        return {
            'breakfast': random.choice(meals[self.diet_type]['breakfast']),
            'lunch': random.choice(meals[self.diet_type]['lunch']),
            'dinner': random.choice(meals[self.diet_type]['dinner'])
        }

    def suggest_exercises(self):
        exercises = {
            'weight_loss': [
                ('Jumping Jacks', 'https://www.youtube.com/watch?v=c4D2tFNEHkg'),
                ('Burpees', 'https://www.youtube.com/watch?v=auBLPXO8Fww')
            ],
            'muscle_gain': [
                ('Push-ups', 'https://www.youtube.com/watch?v=IODxDxX7oi4'),
                ('Squats', 'https://www.youtube.com/watch?v=aclHkVaku9U')
            ],
            'maintenance': [
                ('Plank', 'https://www.youtube.com/watch?v=pSHjTRCQxIw'),
                ('Lunges', 'https://www.youtube.com/watch?v=QOVaHwm-Q6U')
            ]
        }

        return exercises[self.goal]

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    # Parse form data
    age = int(data['age'])
    weight = float(data['weight'])
    height = float(data['height'])
    gender = data['gender']
    activity_level = data['activity_level']
    goal = data['goal']
    diet_type = data['diet_type']

    nutrition = NutritionRecommendation(age, weight, height, gender, activity_level, goal, diet_type)

    recommendations = nutrition.display_recommendations()
    meal_plan = nutrition.generate_meal_plan()
    exercises = nutrition.suggest_exercises()

    return jsonify({
        'calories': recommendations['calories'],
        'protein': recommendations['protein'],
        'fat': recommendations['fat'],
        'carbs': recommendations['carbs'],
        'meal_plan': meal_plan,
        'exercises': exercises
    })

if __name__ == '__main__':
    app.run(debug=True)
