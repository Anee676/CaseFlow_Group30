# CaseFlow (BFB321 Semester Project, group 30)

CaseFlow is a web tool to simplify the writing of medical reports by a speach therapist. It creates sections for 
all the relevat information and formats it in a string to be turned into a report. This process was much simplified 
for the sake of this project.

# Student Numbers and Names:
Anée van Eeden, u24585018
Beaulah Shaw, u24095398
Talia van Sittert, u23526531

## Setup

To run this web solution, the software required is Python 3.10+, Git, and a mySQL database (that has already been coded in schema.sql and seed.sql).

1. Clone the repository: in vs Code's terminal, type
git clone <repository link>
cd CaseFlow_Group 30 

2. Create the environment. In the terminal:
python -m venv venv
venv\Scripts\activate # for Windows operating systems
source venv/bin/activate # macOS/Linux operating systems

3. Install the required packages if they have not been installed yet, using the provided file requirements.txt:
pip install -r requirements.txt

4. Create your `.env` file** by copying the template, then fill in your own database details (host, port, user, password, database name) and a `SECRET_KEY`:

copy .env.example.env #For Windows operating systems
cp .env.example.env #macOS/Linux

5. **Add the CA certificate.** Download `ca.pem` from your Aiven service overview and save it in the project root (skip if it is already in the repository).

6. Create the required tables and sample data
python init_db.py

   Use `python init_db.py --reset` to drop everything and start again from the seed data

7. Run the app:
python app.py

Open 'http://127.0.0.1:5000/' in a browser.

## Project structure

CaseFlow_Group30/
├── app.py            Flask app and routes
├── db.py             Database connection and query helpers
├── init_db.py        Building the tables and loads sample data
├── schema.sql        Creating the tables and constraints
├── seed.sql          Sample data records
├── models/
│   └── caseflow.py   All SQL and other functions (validation, saving, report text)
├── templates/
│   ├── caseflowIndex.html   Homepage: counts and case table
│   ├── addinfo.html         Case details fields
│   └── finalReport.html     Compiled report page
├── static/
│   └── style.css     Style sheet
├── requirements.txt  Packages to install
├── .env.example      Template for your own .env
└── ca.pem            Aiven CA certificate

## End point table

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Count cases and filter the cases according to progress status |
| POST | `/cases/new` | Create a new case |
| GET | `/cases/<case_id>` | Pre-fill an existing case's details |
| POST | `/cases<case_id>` | Validate and save a case's details |
| GET | `/cases/<case_id>/report` | Display the compiled report |
| POST | `/cases/<case_id>/report` | Save and finalise the compiled report |
| POST | `/cases/<case_id>/delete` | Delete a case and its corresponding report and patient (if appropriate) |

## Blueprint structure

The three html user interfaces are stored in the templates folder. They communicate with the static/style.css style sheet and also to app.py, which stores the Flask routes that link the user interface with the functions written in caseflow.py. This structure of files are also connected to schema.sql and seed.sql, which contain the database tables in which the cases reports and associated records are stored. 

Here is a link to the ERD diagram describing the database, tables and their relationships.

![App Database ERD Diagram](./erd_diagram/ERD_diagram.png)


## Sections

| Section | Student | Files |
|---|---|---|
| 1. Layout and dashboard | Anée van Eeden | `README.md`, `static/css/style.css`, `static/js/sample-data.js`, `index.html`, `static/js/dashboard.js` |
| 2. Patient and upload forms | Beaulah Shaw | `patient.html`, `static/js/patient.js`, `uploads.html`, `static/js/uploads.js`, `static/css/forms.css` | 
| 3. Model and impact page | Talia van Sittert | `models/capacity.py`, `tests/test_capacity.py`, `impact.html` |

## Shared style

Every page links `static/css/style.css` and copies the navbar from `index.html`. Font is Times New Roman. Colours are navy `#14284b`, teal `#17878c` and white.

## AI assistance

AI help used:

Claude was used to create the first drafts of the html user interfaces and created javascript code for the functionality.
This Javascript was then simplified a lot and translated to python code, which we, the students, did ourselves. AI was also used to create some records for the database.

