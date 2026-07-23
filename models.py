from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    # Table Constraints 
    __table_args__ = (
        CheckConstraint('reps >= 0', name='check_reps_positive'),
        CheckConstraint('sets > 0', name='check_sets_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, default=0)
    sets = db.Column(db.Integer, default=1)
    duration_seconds = db.Column(db.Integer)

    # Relationships 
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships 
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    # "Through" relationship using secondary association proxy style
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    # Model Validations 
    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Exercise name cannot be empty.")
        return value


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # Relationships 
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    # "Through" relationship using secondary association proxy style
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    # Model Validations 
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return value
