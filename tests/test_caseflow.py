#///////////////////////////////////////////////////////////////////////////////////////////////
# MOCK DATA
#///////////////////////////////////////////////////////////////////////////////////////////////
#The mock data that will be used to demonstrate the python code's functionality.
#The existing "database" of patients is in the form of a list of dictionaries.

#The four stages of writing a report: add patient to database, save your evaluation, generate report, finalise report

#Declare some sample data in the format of a list of dictionaries
patients = [
    {"id" : "6237732712998", "name": "Beaulah", "surname": "Shaw", "stageDone": 4, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"id" : "1153060156238", "name": "Anee", "surname": "van Eeden", "stageDone": 3, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"id" : "8758944319328", "name": "Pieter", "surname": "Botha", "stageDone": 2, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"id" : "5169484183376", "name": "Luka", "surname": "Wood", "stageDone": 1, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"id" : "7493595926423", "name": "Dean", "surname": "Zartmann", "stageDone": 0, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"id" : "9993792601664", "name": "Carine", "surname": "Pretorius", "stageDone": 4, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
    {"id" : "0005060772189", "name": "Chardi", "surname": "Snyman", "stageDone": 2, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False}
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

#/////////////////////////////////////////////////////////////////////////////////////
# functions executed in a specific order each time:
#/////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////
# functions executed in a specific order each time:
#/////////////////////////////////////////////////////////////////////////////////////