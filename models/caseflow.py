

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
    calc_total()
    calcInProgress()


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

def finalReport(patients, patientID):
    # 1. Find the patient in the list
    patient = next((p for p in patients if p.get("id") == patientID), None)
            
            #  Check and increment stageDone from 2 to 3
    if patient and patient.get("stageDone") == 3:
        patient["stageDone"] += 1
        #Do the relevant calculations again
    calcInProgress()
    calcCompleted()
    #return the report again to show what has been finalised
    return(reportOutput(patientID))
    










