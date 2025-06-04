https://github.com/cotovieur/kuztagis_employees

# KuzTagis Employees Application

This application facilitates the assignment of educational workers to the specialties and professions they teach. It is essential for generating documents that list the working staff for each item and displaying them on the educational department's website.


## Requirements
- python
- import `json`
- import `sqlite3`
- import `shutil`
- import `os`
- from `datetime` import `datetime`, `timedelta`
- import `atexit`
- from `flask` import `Flask`, `render_template`, `request`, `redirect`, `url_for`, `session`, `flash`, `jsonify`
- from `werkzeug.security` import `generate_password_hash`, `check_password_hash`
- from `dotenv` import `load_dotenv`
- import `threading`
- import `time`

## Input data
	*Database structure*
	-- "items@ contains specialities and professions, educational programms
	CREATE TABLE "items" (
		"item_id"	INTEGER,
		"name"	TEXT NOT NULL,
		"is_specialty"	BOOLEAN NOT NULL, --2 types of item - specialty and profession
		"code"	TEXT NOT NULL DEFAULT 'code',
		"programm"	TEXT NOT NULL DEFAULT 'programm',
		PRIMARY KEY("item_id")
	);
	-- "workers" contains edu-workers (teachers)
	CREATE TABLE "workers" (
		"worker_id"	INTEGER,
		"fio"	TEXT NOT NULL,
		"position"	TEXT,
		"education_level"	TEXT,
		"specialty"	TEXT,
		"qualification"	TEXT,
		"academic_degree"	TEXT,
		"academic_title"	TEXT,
		"professional_retraining"	TEXT,
		"total_experience"	TEXT,
		"specialty_experience"	TEXT,
		"courses"	TEXT,
		PRIMARY KEY("worker_id")
	);
	-- "worker_item" contains connexion how workers are assigned to their items
	CREATE TABLE "worker_item" (
		"worker_id"	INTEGER,
		"item_id"	INTEGER,
		PRIMARY KEY("worker_id","item_id"),
		FOREIGN KEY("item_id") REFERENCES "items"("item_id"),
		FOREIGN KEY("worker_id") REFERENCES "workers"("worker_id")
	);

## Output Result Data

- **/item_workers page**: Spoilers showing "items" and "workers" assigned to them.


## How It Works
- `app.py` loads the secret key from `secretkey.env` and retrieves users from `users.json`.
- It defines `change_count` to provide backups every 20 changes.
- Routes are distributed to render corresponding `.html` templates.
- If not signed in, it shows `/login.html`.
- User fills in login/password fields on `/login.html`.
- The app checks login/password and redirects to `/index.html` if successful.
- `login_required` checks every route for being signed in.
- `/workers` page shows a table of workers from the `workers` table in `workers.db`.
- Buttons for editing worker information and firing them are provided.
- `/add` performs the same form as editing with the same checking principles to add new workers.
- `/items` shows "items" from the database.
- `/assign` permits drag & drop of needed workers to assign to corresponding items.
- `/item_workers` shows the resulted view, which items contain which workers assigned. And the code to easily copy it and then put
- `app.py` runs on the localhost or in the shared folder of our department (commented option)

## Backups
- `workers.db` is backed up every 20 new/removed/changed records, once a week, and when the app is closed (not required to run it always for us) in the 'backups' folder
- `change_count` is counted in every function working with .db


## Logging
- Logging is performed when a new worker is added, edited, or fired.


## Applied Stuff
- `.bat` files run correspondant `.py`s
- `db_setup.py` pulls data from your file, mind re-writing of the database
- `inspect_database.py` shows data, saved in database: workers, items and connexions workers-items