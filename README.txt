https://github.com/cotovieur/kuztagis_employees

This application provides handy assigning edu-workers to the specialities and professions they teach.
Assigning is required to finally form documents with list of working staff of each item and showing on the web-site of the educational department

*REQUIRES*
	python
	import json
	import sqlite3
	import shutil
	import os
	from datetime import datetime, timedelta
	import atexit
	from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
	from werkzeug.security import generate_password_hash, check_password_hash
	from dotenv import load_dotenv
	import threading
	import time

*INPUT DATA*
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

*OUTPUT RESULT DATA — /item_workers page, spoilers, showing "items" and "workers" assigned to them


*HOW DOES IT WORK*
	app.py opens secretkey.env {SECRET_KEY='secret_key'} which is generated in secretkey_gen.py and gets SECRET_KEY
	loads users from users.json
	defines the change_count to provide backing up every 20 changes
	distributes routes to render correspondant .html templates, if not signed in, shows /login.html
	{User fills login/password fields on the /login.html
	app checks login/password, redirects to /index.html if succesful}
	login_required checks every route for being signed in
	/workers page shows a table of workers, taken from "workers" of workers.db
	it is placed buttons for editing worker information (checks if worker_id is 5 to 6 symbols, and checks worker_id and fio if it doubles, throws error this case) and firing them, records in .db
	/add performs the same form as editing with the same checking principles, records in .db
	/items shows "items" from .db
	/assign permits to drag&drop needed worker to assign for correspondant item, removing workers from the item though, added search of workers
	/item_workers shows the resulted view, which items contain which workers assigned. And the code to easily copy it and then put
	app.py runs on the localhost or in the shared folder of our department (commented option)

*BACKUPS*
	workers.db is backing up every 20 new/removed/changed records, once a week, and when app is closed (not required to run it always for us) in the 'backups' folder
	change_count is counted in every function working with .db

*LOGGING*
	logging performs whilst new worker added, worker edited or fired

*APPLIED STUFF*
	.bat files run correspondant .py's
	db_setup.py pulls data from your file, mind re-writing of the database
	inspect_database.py shows data, saved in database: workers, items and connexions workers-items

