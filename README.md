# Gym Tracker API

A lightweight, robust Flask RESTful API designed to manage physical training progress by tracking workouts, unique exercise movements, and capturing granular session metrics (reps, sets, durations) through localized schema validation.

##  Installation Instructions

Follow these sequential steps in your terminal to set up your isolated development environment and prepare the persistent storage layers:

### 1. Initialize Virtual Environment and Dependencies
This project uses explicit Python virtual management tools. Run the installation script matching your project architecture:

```bash
# Option A: standard pip deployment (Recommended for manual setups)
pip install -r requirements.txt

# Option B: if managing via Pipenv explicitly
pipenv install
pipenv shell
```

### 2. Run Database Migrations
Initialize the tracking configuration and execute structural schema generation directly through the Alembic core wrapper:

```bash
# Initialize tracking folder directory (Run once only)
flask db init

# Generate incremental migration versions using model tracking
flask db migrate -m "Create workout and exercise schemas with constraints"

# Apply version blueprints down to the persistent database binary
flask db upgrade
```

### 3. Seed Database Store
Populate the newly initialized schema layers with baseline dummy elements and check relationship structural paths:

```bash
python seed.py
```

---

##  Run Instructions

Start the localized development engine from your terminal workspace using standard Flask environment routing variables:

```bash
# Set runtime target pointer flags
export FLASK_APP=app.py
export FLASK_ENV=development

# Initiate the live environment engine
flask run --port=5555
```
The API server will launch locally at `http://127.0.0`.

---

##  API Endpoints Reference

### Workout Endpoints

* **`GET /workouts`**
  * *Description:* Fetches an array block of all recorded workout instances. Returns basic metadata (id, date, duration_minutes, notes) without complex nested tree recursion for performance scalability.
* **`GET /workouts/<id>`**
  * *Description:* Fetches details for a single target workout entry. *(Stretch Goal Complete)*: Incorporates nested tracking matrices pulling performance statistics (`reps`, `sets`, `duration_seconds`) explicitly out of `WorkoutExercises` data joins.
* **`POST /workouts`**
  * *Description:* Creates a single workout entry using incoming structured JSON payloads. Runs explicit model-side `@validates` check confirming that runtime tracking spans greater than 0 minutes.
* **`DELETE /workouts/<id>`**
  * *Description:* Purges a target workout record by absolute identifier. *(Stretch Goal Complete)*: Employs structural `cascade='all, delete-orphan'` logic blocks to clean matching associations out of dependency lookup tables automatically.

### Exercise Endpoints

* **`GET /exercises`**
  * *Description:* Fetches an array overview listing of all exercise profiles globally registered in the tracker index.
* **`GET /exercises/<id>`**
  * *Description:* Fetches profile parameters for a specific individual exercise lookup, generating structured arrays tracking historic workout loops linked to that execution style.
* **`POST /exercises`**
  * *Description:* Appends an individual exercise definition profile to the catalog stack. Includes validation intercepts blocking white-space data structures or empty string entries.
* **`DELETE /exercises/<id>`**
  * *Description:* Purges a specific exercise template entry by identifier, removing references in join structures to preserve data consistency.

### WorkoutExercise (Join Table) Endpoints

* **`POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`**
  * *Description:* Appends structural performance data (`reps`, `sets`, `duration_seconds`) to create a relationship intersection map linking a specific exercise execution instance to an overall workout event timeline tracking frame.

---

##  Pipfile Dependencies

For environments using `pipenv`, your **`Pipfile`** requires the following package registry specifications to resolve architecture dependency tracks accurately:

```toml
[[source]]
url = "https://pypi.org"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-sqlalchemy = "*"
flask-migrate = "*"
marshmallow = "*"
marshmallow-sqlalchemy = "*"

[dev-packages]
pytest = "*"

[requires]
python_version = "3.12"
```

---

##  Test Execution (If Applicable)

If you have test configurations set up in your folder structure, evaluate the integrity of validation decorators and HTTP route responses by invoking your testing framework:

```bash
# Execute suite checks with error readout flags
pytest -v
```
