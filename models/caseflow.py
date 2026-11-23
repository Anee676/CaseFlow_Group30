
#Importing the required libraries and modules
import math
from datetime import date
import pymysql
from db import query_all, query_one, execute, get_db

#///////////////////////////////////////////////////////////////////////////////////
#Do the following calculations to give the therapist an overview of work to be done, displayed on home page
#////////////////////////////////////////////////////////////////////////////////////

#Default query that will be added to
select_query = """
    SELECT c.Case_id, p.Patient_Name, p.Patient_Surname, c.Case_progress, c.Report_status
    FROM Cases c
    LEFT JOIN Patients p ON c.Patient_id = p.Patient_id
    """

#Total cases
def count_cases():
    return query_one("SELECT COUNT(*) AS n FROM Cases")["n"]

#Display all the records
def display_all():
    sql = select_query + " ORDER BY Case_id ASC"
    return query_all(sql)

#Reports in progress
def count_in_progress():
    return query_one("SELECT COUNT(*) AS n FROM Cases WHERE Case_progress < 100")["n"]

#Display the cases in progress
def display_in_progress():
    sql = select_query + " WHERE Case_progress < 100 ORDER BY Case_id ASC"
    return query_all(sql)

#Reports completed
def count_completed():
    return query_one("SELECT COUNT(*) AS n FROM Cases WHERE Case_progress = 100")["n"]

#Display the completed cases
def display_completed():
    sql = select_query + " WHERE Case_progress = 100 ORDER BY Case_id ASC"
    return query_all(sql)

#////////////////////////////////////////////////////////////////////////////////////////////////////////
# STEP 1: A CASE RECORD IS EDITED OR CONTINUED WITH
# When a specific case is clicked in the table on the home page.
#///////////////////////////////////////////////////////////////////////////////////////////////////////

def get_case(case_id):
    return query_one("""
        SELECT c.Case_id, c.Injury_date, c.Accident_Details, c.Scans_Imagery,
               c.Ankle_injury, c.Knee_injury, c.Hip_injury,
               c.Arm_injury, c.Wrist_injury, c.Ankle_details, c.Knee_details, c.Hip_details, c.Arm_details, c.Wrist_details,
               c.Case_progress, c.Report_status,
               p.Patient_id, p.Patient_name, p.Patient_surname, p.Patient_DoB,
               r.Report_id, r.Date_Start_Report, r.DateEndReport, r.ReportString
        FROM Cases c
        LEFT JOIN Patients p ON p.Patient_id = c.Patient_id
        JOIN Reports  r ON r.Report_id  = c.Report_id
        WHERE c.Case_id = %s
    """, (case_id,))

#////////////////////////////////////////////////////////////////////////////////////////////////////////
# STEP 1: A NEW PATIENT IS ADDED
# When the "new patient" button on the home page is clicked.
#///////////////////////////////////////////////////////////////////////////////////////////////////////

def add_case():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO Reports (Date_Start_Report) VALUES (CURDATE())")
        report_id = cursor.lastrowid
        cursor.execute(
        "INSERT INTO Cases (Report_id, Case_progress, Report_status) VALUES (%s, %s, %s)",
                            (report_id, 25, "Incomplete"),
                             )
        case_id = cursor.lastrowid
    db.commit()
    return case_id
    

#When the save button is clicked on the details page, the information is validated and then saved to the database.

MODULES = ["Ankle", "Knee", "Hip", "Arm", "Wrist"]

def validate_case(form):
    errors = []
    name = form.get("firstName", "").strip()
    surname = form.get("surname", "").strip()
    accident = form.get("accident_details", "").strip()
    id_number = form.get("idNumber", "").strip()
    if not name:
        errors.append("Name is required.")
    if not surname:
        errors.append("Surname is required.")
    if not accident:
        errors.append("Accident details are required.")
    if not (id_number.isdigit() and len(id_number) == 13):
            errors.append("ID number must be exactly 13 digits.")

    def valid_date(field, label, required):
        text = form.get(field, "").strip()
        if not text:
            if required:
                errors.append(f"{label} is required.")
            return None
        try:
            date.fromisoformat(text)
            return text
        except ValueError:
            errors.append(f"{label} is not a valid date.")

    values = dict(
        Patient_id=id_number,
        Patient_name=name, Patient_surname=surname,
        Patient_DoB=valid_date("dateOfBirth", "Date of birth", True),
        Injury_date=valid_date("dateOfInjury", "Date of injury", True),
        Accident_Details=accident,
        Scans_Imagery=form.get("scans_imagery", "").strip() or None,
        #Date_Start_Report=valid_date("date_start_report", "Report start date", True),
        DateEndReport=valid_date("date_end_report", "Report end date", False),
        ReportString=form.get("report_string", "").strip() or None,
    )
    # injury modules: an unticked box means flag 0 and no details
    for m in MODULES:
        ticked = m.lower() in form
        values[f"{m}_injury"] = 1 if ticked else 0
        values[f"{m}_details"] = (form.get(f"{m.lower()}_details", "").strip() or None) if ticked else None

    if (values["DateEndReport"]and values["DateEndReport"] < values["Date_Start_Report"]):
        errors.append("The report cannot end before it starts.")
    return values, errors

#After the validation, the values from the form are saved to the tables in the database.

def update_case(case_id, v, progress=None, status=None):
    db = get_db()

    with db.cursor() as cur:
        # lock the case row and read its current state
        cur.execute("""SELECT Report_id, Patient_id, Case_progress, Report_status
                        FROM Cases WHERE Case_id = %s FOR UPDATE""", (case_id,))
        case = cur.fetchone()

        if case is None:
            db.rollback()
            return False, "Case not found."

        if case["Report_status"] == "Report finalised":
            db.rollback()
            return False, "This report is finalised and can no longer be edited."

        # a case that already has a patient keeps that patient
        patient_id = case["Patient_id"] or v["Patient_id"]

        # does this patient already exist?
        cur.execute("SELECT Patient_id FROM Patients WHERE Patient_id = %s FOR UPDATE",
                        (patient_id,))
        if cur.fetchone() is None:
            cur.execute("""INSERT INTO Patients
                                (Patient_id, Patient_name, Patient_surname, Patient_DoB)
                            VALUES (%s, %s, %s, %s)""",
                        (patient_id, v["Patient_name"], v["Patient_surname"], v["Patient_DoB"]))
            message = "New patient added and case saved."
        else:
            cur.execute("""UPDATE Patients
                            SET Patient_name = %s, Patient_surname = %s, Patient_DoB = %s
                            WHERE Patient_id = %s""",
                        (v["Patient_name"], v["Patient_surname"], v["Patient_DoB"], patient_id))
            message = "Existing patient found. Case saved."

        cur.execute("""UPDATE Reports
                        SET DateEndReport = %s, ReportString = COALESCE(%s, ReportString)
                        WHERE Report_id = %s""",
                    (v["DateEndReport"], v["ReportString"],
                        case["Report_id"]))

        cur.execute("""UPDATE Cases SET Patient_id = %s, Injury_date = %s,
                            Accident_Details = %s, Scans_Imagery = %s,
                            Ankle_injury = %s, Knee_injury = %s, Hip_injury = %s,
                            Arm_injury = %s, Wrist_injury = %s,
                            Ankle_details = %s, Knee_details = %s, Hip_details = %s,
                            Arm_details = %s, Wrist_details = %s
                        WHERE Case_id = %s""",
                    (patient_id, v["Injury_date"], v["Accident_Details"], v["Scans_Imagery"],
                        v["Ankle_injury"], v["Knee_injury"], v["Hip_injury"],
                        v["Arm_injury"], v["Wrist_injury"],
                        v["Ankle_details"], v["Knee_details"], v["Hip_details"],
                        v["Arm_details"], v["Wrist_details"],
                        case_id))

        if progress is not None and progress >= case["Case_progress"]:
            cur.execute("""UPDATE Cases SET Case_progress = %s, Report_status = %s
                           WHERE Case_id = %s""", (progress, status, case_id))
    db.commit()          # patient, report and case saved together
    return True, message


#The report string is built and passed to the report string, as well as displayed on the final report page 
def build_report_text(v):
    lines = [
        f"Patient Name: {v['Patient_name']} {v['Patient_surname']}",
        f"ID Number: {v['Patient_id']}",
        f"Date of birth: {v['Patient_DoB']}",
        f"Date of injury: {v['Injury_date']}",
        f"Accident details: {v['Accident_Details']}",
        f"Scans & Imagery: {v['Scans_Imagery'] or 'None'}",
    ]
    for m in MODULES:                       # Ankle, Knee, Hip, Arm, Wrist
        if v[f"{m}_injury"]:                # only the ticked modules
            lines.append(f"{m}: {v[f'{m}_details'] or 'No details entered'}")
    return "\n".join(lines)


#For the final save button before the report is finalised:
def update_report_string(case_id, text):
    execute("""UPDATE Reports r JOIN Cases c ON c.Report_id = r.Report_id
               SET r.ReportString = %s
               WHERE c.Case_id = %s""",
            (text.strip() or None, case_id))

#For the final saving and locking of the report when the finalise button is clicked:
def finalise_report(case_id, text):
    db = get_db()

    with db.cursor() as cur:
        cur.execute("""UPDATE Reports r JOIN Cases c ON c.Report_id = r.Report_id
                        SET r.ReportString = %s, r.DateEndReport = CURDATE()
                        WHERE c.Case_id = %s""",
                    (text.strip() or None, case_id))
        cur.execute("""UPDATE Cases SET Case_progress = 100,
                                        Report_status = 'Report finalised'
                        WHERE Case_id = %s""", (case_id,))
        db.commit()          # text, progress and status saved together

#Ensure that no one can edit a completed report.
def update_report_string(case_id, text):
    execute("""UPDATE Reports r JOIN Cases c ON c.Report_id = r.Report_id
               SET r.ReportString = %s
               WHERE c.Case_id = %s AND c.Report_status <> 'Report finalised'""",
            (text.strip() or None, case_id))


#Delete the selected case by clicking the delete button

def delete_case(case_id):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("""SELECT Report_id, Patient_id FROM Cases
                           WHERE Case_id = %s FOR UPDATE""", (case_id,))
            case = cur.fetchone()
            if case is None:
                db.rollback()
                return False, "Case not found."

            # 1. the case (child entity) must be deleted first.
            cur.execute("DELETE FROM Cases WHERE Case_id = %s", (case_id,))

            # 2. its report (one-to-one, so nobody else uses it)
            cur.execute("DELETE FROM Reports WHERE Report_id = %s", (case["Report_id"],))

            # 3. the patient, only if no other case still uses them
            if case["Patient_id"]:
                cur.execute("SELECT COUNT(*) AS n FROM Cases WHERE Patient_id = %s",
                            (case["Patient_id"],))
                if cur.fetchone()["n"] == 0:
                    cur.execute("DELETE FROM Patients WHERE Patient_id = %s",
                                (case["Patient_id"],))
        db.commit()           # all deletes saved together
        return True, "Case deleted."
    except Exception:
        db.rollback()         # nothing deleted
        raise

#///////////////////////////////////////////////////////////////////////////////////////////////////
# STEP 2: WHEN THE PATIENT DETAILS ARE FINALISED
# When the "mark complete" button on the new patient page is clicked
#/////////////////////////////////////////////////////////////////////////////////////////////////////

#This function creates a new report and increments the stagesDone field in the patients list of dictionaries

def finaliseEval(patients, reports, patientID, patientName, patientSurname, bAnkle, bKnee, bHip, bArm, bWrist,
                 sAnkleSeverity, sAnkleNotes, sKneeSeverity, sKneeNotes, sHipSeverity, sHipNotes, 
                 sArmSeverity, sArmNotes, sWristSeverity, sWristNotes):
    # Find the dictionary with the matching 'id'
        patient = next((p for p in patients if p.get("id") == patientID), None)
        
         # Check if patient exists and if stageDone is originally 1
        if patient and patient.get("stageDone") == 1:
            patient["stageDone"] += 1
            #A new report is created in the reports list, with the patient's details
            # and strings for the relevant modules.
            newReport = ["ID: " + patientID, "Name : " + patientName, "Surname : " + patientSurname]
        
            #Use the boolean variables to determine which modules are relevant.
            #NOTE: here, validation will be incorporated later on
            if bAnkle:
                newReport.append("Severity : " + sAnkleSeverity)
                newReport.append("Notes : " + sAnkleNotes)
        
            if bKnee:
                newReport.append("Severity : " + sKneeSeverity)
                newReport.append("Notes : " + sKneeNotes)
        
            if bHip:
                newReport.append("Severity : " + sHipSeverity)
                newReport.append("Notes : " + sHipNotes)
        
            if bArm:
                newReport.append("Severity : " + sArmSeverity)
                newReport.append("Notes : " + sArmNotes)
        
            if bWrist:
                newReport.append("Severity : " + sWristSeverity)
                newReport.append("Notes : " + sWristNotes)
        
            #Now, add the dictionary containing the new report to the list of reports.
            reports.append(newReport)
        

#///////////////////////////////////////////////////////////////////////////////////////////////////
# OUTPUT  FORMATTED REPORT/GENERATE REPORT
# When the "next" button on the new patient page is clicked
#/////////////////////////////////////////////////////////////////////////////////////////////////////

#Search for the report with matching ID using a standard loop, then give output as a summary of evaluation


def reportOutput(patients, reports, patientID):
    found_report = None
    for report in reports:
        if report[0] == "ID: " + patientID:
            found_report = report
            break  # Stop searching once found

    #  Print each line neatly if found
    if found_report != None:
        # 1. Find the patient in the list
        patient = next((p for p in patients if p.get("id") == patientID), None)
        
        #  Check and increment stageDone from 2 to 3
        if patient and patient.get("stageDone") == 2:
            patient["stageDone"] += 1

        #  Print the report
        print("--- REPORT DETAILS ---")
        for line in found_report:
            print(line)
        print("----------------------")
    else:
        print("Report not found.")


#///////////////////////////////////////////////////////////////////////////////////////////////////
# WHEN A REPORT IS FINALISED
#/////////////////////////////////////////////////////////////////////////////////////////////////////

def finalReport(patients, reports, patientID):
    # 1. Find the patient in the list
    patient = next((p for p in patients if p.get("id") == patientID), None)
            
            #  Check and increment stageDone from 2 to 3
    if patient and patient.get("stageDone") == 3:
        patient["stageDone"] += 1
        #Do the relevant calculations again
    calcInProgress(patients)
    calcCompleted(patients)
    #return the report again to show what has been finalised
    return(reportOutput(patients, reports, patientID))
    










