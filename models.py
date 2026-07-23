from unicodedata import category

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    equipement_needed = db.Column(db.Boolean)# boolean

    def to_dict(self, name, category, equipement_needed):
        self.name = name
        self.category = category
        self.equipement_needed = equipement_needed

    def __repr__(self):
        return '<Exercise %r>' % self.name

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Coulmn(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(1000), nullable=False)

    def to_dict(self, date, duration_minutes, notes):
        self.date = date
        self.duration_minutes = duration_minutes
        self.notes = notes

    def __repr__(self):
        return '<Workout %r>' % self.date

# Join table
class WorkoutExercises(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)

    def to_dict(self, exercise_id, workout_id):
        self.exercise_id = exercise_id
        self.workout_id = workout_id

    def __repr__(self):
        return '<WorkoutExercises %r>' % self.id