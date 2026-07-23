from datetime import date
from app import app, db
from models import Exercise, Workout, WorkoutExercise

def seed_database():
    print(" Clearing out existing tables...")
    # Delete child rows first due to Foreign Key constraints
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("  Creating exercise definitions...")
    ex1 = Exercise(name="Push-Ups", category="Chest", equipment_needed=False)
    ex2 = Exercise(name="Bicep Curls", category="Arms", equipment_needed=True)
    ex3 = Exercise(name="Squats", category="Legs", equipment_needed=False)
    ex4 = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)
    
    db.session.add_all([ex1, ex2, ex3, ex4])
    db.session.commit()

    print(" Creating workout sessions...")
    w1 = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Morning upper body focus.")
    w2 = Workout(date=date(2026, 7, 22), duration_minutes=60, notes="Evening lower body and cardio.")
    
    db.session.add_all([w1, w2])
    db.session.commit()

    print("  Linking exercises to workouts via WorkoutExercise...")
    # Workout 1 Exercises
    we1 = WorkoutExercise(workout=w1, exercise=ex1, reps=15, sets=3, duration_seconds=120)
    we2 = WorkoutExercise(workout=w1, exercise=ex2, reps=12, sets=3, duration_seconds=90)
    
    # Workout 2 Exercises
    we3 = WorkoutExercise(workout=w2, exercise=ex3, reps=20, sets=4, duration_seconds=180)
    we4 = WorkoutExercise(workout=w2, exercise=ex4, reps=1, sets=1, duration_seconds=1200)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print(" Database successfully seeded!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()
