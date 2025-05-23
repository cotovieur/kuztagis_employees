This application provides handy assigning edu-workers to the specialities and professions they teach

*REQUIRES*
python
flask
flask-login
python-dotenv
from functools import wraps

*WHAT IS WHAT*
Workers contains edu-workers (teachers)
Items containt specialities and professions, educational programms
Assigning is required to finally form documents with list of working staff of each item and showing on the web-site of the educational department
users.json contains user logins and hashed passwords

*DATABASE STRUCTURE*
CREATE TABLE "items" (
	"item_id"	INTEGER,
	"name"	TEXT NOT NULL,
	"is_specialty"	BOOLEAN NOT NULL,
	"code"	TEXT NOT NULL DEFAULT 'code',
	"programm"	TEXT NOT NULL DEFAULT 'programm',
	PRIMARY KEY("item_id")
);
CREATE TABLE "worker_item" (
	"worker_id"	INTEGER,
	"item_id"	INTEGER,
	PRIMARY KEY("worker_id","item_id"),
	FOREIGN KEY("item_id") REFERENCES "items"("item_id"),
	FOREIGN KEY("worker_id") REFERENCES "workers"("worker_id")
);
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

*HOWTO*
use run_app.bat to run application
db_setup.py pulls data from your file, do not run it to avoid re-writing of the database
app.py provides functions, pushing db tables to the .html/s, handling adding new workers, assigning and unassigning workers
to items
inspect_database.py shows data, saved in database: workers, items and connexions workers-items