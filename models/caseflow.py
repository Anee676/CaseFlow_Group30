#///////////////////////////////////////////////////////////////////////////////////////////////
# MOCK DATA
#///////////////////////////////////////////////////////////////////////////////////////////////
#The mock data that will be used to demonstrate the python code's functionality.
#The existing "database" of patients is in the form of a list of dictionaries.

#The four stages of writing a report: add patient to database, save your evaluation, generate report, finalise report

#Declare some sample data in the format of a list of dictionaries
patients = [
    {"6237732712998" : "1", "name": "Beaulah", "surname": "Shaw", "stageDone": 4, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"1153060156238" : "2", "name": "Anee", "surname": "van Eeden", "stageDone": 3, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"8758944319328" : "3", "name": "Pieter", "surname": "Botha", "stageDone": 2, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"5169484183376" : "4", "name": "Luka", "surname": "Wood", "stageDone": 1, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"7493595926423" : "5", "name": "Dean", "surname": "Zartmann", "stageDone": 0, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"9993792601664" : "6", "name": "Carine", "surname": "Pretorius", "stageDone": 4, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"0005060772189" : "7", "name": "Chardi", "surname": "Snyman", "stageDone": 2, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False}
]

#An empty list of dictionaries for the reports that will be generated.
reports = []

#The new patient's details. The notes are kept very short for demonstration's sake, but it will usually have more content
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

#///////////////////////////////////////////////////////////////////////////////////
#Do the following calculations to give the therapist an overview of work to be done, displayed on home page
#////////////////////////////////////////////////////////////////////////////////////

#Total patients
def calc_total(patients):
    return len(patients)

#Reports in progress

def calcInProgress(patients):
    count = 0
    for patient in patients:
        if patient["stageDone"] < 4:
            count += 1
    return count

#Reports completed

def calcCompleted(patients):
    count = 0
    for patient in patients:
        if patient["stageDone"] == 4:
            count += 1
    return count

#////////////////////////////////////////////////////////////////////////////////////////////////////////
# STEP 1: A NEW PATIENT IS ADDED
# When the "save" button is clicked on the "new patient" page
#///////////////////////////////////////////////////////////////////////////////////////////////////////

def add_patient(patients, patientID, patientName, patientSurname, bAnkle, bKnee, bHip, bArm, bWrist):

    #When the button is clicked to save on the new patient page,
    # new records are added to the lists of dictionaries, both patients and reports

    #Database for patients gets a new record, with id, name, surname, booleans for the modules,
    # and stageDone = 1.
    patients.append({"id": patientID, "name": patientName, "surname": patientSurname, "stageDone": 1, "Ankle": bAnkle, "Knee": bKnee, "Hip": bHip, "Arm": bArm, "Wrist": bWrist})
    calc_total(patients)
    calcInProgress(patients)


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
    










