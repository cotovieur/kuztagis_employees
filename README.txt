This application provides handy assigning edu-workers to the specialities and professions they teach

*WHAT IS WHAT*
Workers contains edu-workers (teachers)
Items containt specialities and professions, educational programms
Assigning is required to finally form documents with list of working staff of each item and showing on the web-site of
the educational department

*HOWTO*
use run_app.bat to run application
db_setup.py pulls data from your file, do not run it to avoid re-writing of the database
app.py provides functions, pushing db tables to the .html/s, handling adding new workers, assigning and unassigning workers
to items
inspect_database.py shows data, saved in database: workers, items and connexions workers-items