This application provides handy assigning edu-workers to the specialities and professions they teach.
Assigning is required to finally form documents with list of working staff of each item and showing on the web-site of the educational department

*REQUIRES*
	python
	flask
	flask-login
	python-dotenv
	from functools import wraps
	pip install schedule
	from datetime import datetime
	import atexit
	import shutil

*INPUT DATA*
	*Database structure*
	-- "items@ contains specialities and professions, educational programms
	CREATE TABLE "items" (
		"item_id"	INTEGER,
		"name"	TEXT NOT NULL,
		"is_specialty"	BOOLEAN NOT NULL,
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

*OUTPUT RESULT DATA — /item_workers page, spoilers, showing "items" and "workers" assigned to them


*HOW DOES IT WORK*
	app.py opens secretkey.env {SECRET_KEY='secret_key'} which is generated in secretkey_gen.py
	

*BACKUPS*
	workers.db is backing up every 20 new/removed/changed records, once a week, and when app is closed (not required to run it always for us) in the 'backups' folder

*APPLIED STUFF*
	.bat files run correspondant .py's
	db_setup.py pulls data from your file, do not run it to avoid re-writing of the database
	inspect_database.py shows data, saved in database: workers, items and connexions workers-items
