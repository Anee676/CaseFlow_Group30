# CaseFlow (BFB321 Semester Project, group 30)

CaseFlow is a web tool to simplify the writing of medical reports by a speach therapist. It creates sections for 
all the relevat information and formats it in a string to be turned into a report. This process was much simplified 
for the sake of this project.

# Student Numbers and Names:
Anée van Eeden, u24585018
Beaulah Shaw, u24095398
Talia van Sittert, u23526531

## How to open it

Open the folder in VS Code and open the html pages in a browser. They will be properly linked to each other in 
the final submission
It is important that the functions, excluding the calculations, are executed in order to ensure they work correctly.
In the final submission, more validation will be set in place to make the code more robust.

The three functions calcTotal, calcInProgress and calcCompleted can be executed at any point and are there to give 
the user an overview of the patients in the database.
Then, the following functions are executed in order to create a new report:
1. addPatient, 
2. finaliseEval, 
3. reportOutput, 
4. finalReport

In the main python model, the following variables have been created to demonstrate the creation of a report:

patientName = "Anica"
patientSurname = "Ferreira"
patientID = "1423576436475"
bAnkle = True
bKnee = False
bHip = True
bArm = False
bWrist = False
sAnkleSeverity = "Mild"
sKneeSeverity = ""
sHipSeverity = "Moderate"
sArmSeverity = ""
sWristSeverity = ""
sAnkleNotes = "Patient has mild ankle pain. The injury might grow worse if not treated."
sKneeNotes = ""
sHipNotes = "Patient has moderate hip pain. The cause is still unclear."
sArmNotes = ""
sWristNotes = ""


To run the model tests:

```
a pytest file was created with some tests, but it returned an error and I (Anée) could not fix it. There is mock data
provided in the main python model that can be used in something like jupyter notebook to test the functions.
```

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



