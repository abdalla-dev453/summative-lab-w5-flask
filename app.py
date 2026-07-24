from flask import Flask, jsonify, request, Blueprint
from flask_migrate import Migrate
from models import db, Workout, WorkoutExercise, Exercise
from schemas import WorkoutSchema, WorkoutExerciseSchema, ExerciseSchema
from marshmallow import ValidationError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api_bp = Blueprint('api', __name__)

# Initialize isolated schema instances
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

# ==========================================
# WORKOUT ENDPOINTS
# ==========================================

@api_bp.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    # Simple list layout excluding deep loops for bulk performance
    schema = WorkoutSchema(many=True, exclude=('workout_exercises', 'exercises'))
    return jsonify(schema.dump(workouts)), 200


@api_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get_or_4004(id) if hasattr(Workout.query, 'get_or_404') else db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    # Stretch Goal Met: Returns workout + workout_exercises (reps, sets, duration) + exercise info
    return jsonify(workout_schema.dump(workout)), 200


@api_bp.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    try:
        # Deserialization and validation
        new_workout = workout_schema.load(json_data, session=db.session)
        db.session.add(new_workout)
        db.session.commit()
        return jsonify(workout_schema.dump(new_workout)), 201
    except ValidationError as err:
        return jsonify(err.messages), 420


@api_bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    # Stretch Goal Met: cascade='all, delete-orphan' automatically deletes workout_exercises
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {id} and all related exercise entries successfully deleted"}), 200


# ==========================================
# EXERCISE ENDPOINTS
# ==========================================

@api_bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    schema = ExerciseSchema(many=True, exclude=('workout_exercises', 'workouts'))
    return jsonify(schema.dump(exercises)), 200


@api_bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@api_bp.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    try:
        new_exercise = exercise_schema.load(json_data, session=db.session)
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201
    except ValidationError as err:
        return jsonify(err.messages), 422


@api_bp.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    # Stretch Goal Met: cascade layout purges matching join table connections safely
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {id} and all associated logs deleted"}), 200


# ==========================================
# WORKOUTEXERCISE JOIN ENDPOINT
# ==========================================

@api_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    # Verify both parents exist first
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return jsonify({"error": "Specified Workout or Exercise does not exist"}), 404

    json_data = request.get_json() or {}
    # Inject foreign keys from URL path variables directly into processing payload
    json_data['workout_id'] = workout_id
    json_data['exercise_id'] = exercise_id

    try:
        new_relation = workout_exercise_schema.load(json_data, session=db.session)
        db.session.add(new_relation)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(new_relation)), 201
    except ValidationError as err:
        return jsonify(err.messages), 422

app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run(debug=True)