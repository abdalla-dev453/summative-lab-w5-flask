from marshmallow import Schema, fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Exercise, Workout, WorkoutExercise

class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True  # Includes foreign keys in serialization

    # Explicitly pull details from the relationship for nested lookups
    # using lambda to avoid circular import issues
    exercise = fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises', 'workouts')))
    workout = fields.Nested(lambda: WorkoutSchema(exclude=('workout_exercises', 'exercises')))

    # Schema Validations 
    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value < 0:
            raise ValidationError("Reps must be greater than or equal to 0.")

    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be greater than 0.")


class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True

    # Nested fields for structural depth
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, exclude=('exercise',))
    workouts = fields.Nested(lambda: WorkoutSchema(many=True, exclude=('workout_exercises', 'exercises')))

    # Schema Validations 
    @validates('name')
    def validate_name(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError("Exercise name cannot be blank.")


class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True

    # Nested fields to capture statistics (Addresses Step 7 GET /workouts/<id> stretch goal)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, exclude=('workout',))
    exercises = fields.Nested(ExerciseSchema, many=True, exclude=('workout_exercises', 'workouts'))
