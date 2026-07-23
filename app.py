from flask import Flask, jsonify, request, Blueprint
from flask_migrate import Migrate
from models import db, Workout, WorkoutExercise, Exercise


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api_bp = Blueprint('api', __name__)

# Endpoits
@api_bp('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([workout.to_dict() for workout in workouts]), 200

@api_bp("/workouts/<int:workout_id>", methods=['GET'])
def get_workout_by_id(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return jsonify(workout.to_dict()), 200


@api_bp("/workouts", methods=['POST'])
def create_workout():
    data = request.get_json()
    new_workout = Workout(**data)
    db.session.add(new_workout)
    db.session.commit()
    return jsonify(new_workout.to_dict()), 201

@api_bp("/workouts/<int:workout_id>", methods=['PUT'])
def update_workout(workout_id):
    data = request.get_json()
    workout = Workout.query.get_or_404(workout_id)
    for key, value in data.items():
        setattr(workout, key, value)
    db.session.commit()
    return jsonify(workout.to_dict()), 200

@api_bp("/workouts/<int:workout_id>", methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200

# Exercise endpoints
@api_bp("/exercises", methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([exercise.to_dict() for exercise in exercises]), 200

@api_bp("/exercises/<int:exercise_id>", methods=['GET'])
def get_exercise_by_id(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify(exercise.to_dict()), 200


@api_bp("/exercises", methods=['POST'])
def create_exercise():
    data = request.get_json()
    new_exercise = Exercise(**data)
    db.session.add(new_exercise)
    db.session.commit()
    return jsonify(new_exercise.to_dict()), 201

@api_bp("/exercises/<int:exercise_id>", methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200


# workoutexercise (join table endpoint)
@api_bp("/workouts/<int:workout_id>/exercises", methods=['POST'])
def add_exercise_to_workout(workout_id):
    data = request.get_json()
    new_workout_exercise = WorkoutExercise(**data)
    db.session.add(new_workout_exercise)
    db.session.commit()
    return jsonify(new_workout_exercise.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True)