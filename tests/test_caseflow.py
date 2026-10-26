
import pytest
from models.caseflow import *

#///////////////////////////////////////////////////////////////////////////////////////////////
# MOCK DATA
#///////////////////////////////////////////////////////////////////////////////////////////////
#The mock data that will be used to demonstrate the python code's functionality.
#The existing "database" of patients is in the form of a list of dictionaries.

#The four stages of writing a report: add patient to database, save your evaluation, generate report, finalise report

#Declare some sample data in the format of a list of dictionaries
@pytest.fixture
def patients():
    return [
        {"id": "6237732712998", "name": "Beaulah", "surname": "Shaw", "stageDone": 4, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
        {"id": "1153060156238", "name": "Anee", "surname": "van Eeden", "stageDone": 3, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
        {"id": "8758944319328", "name": "Pieter", "surname": "Botha", "stageDone": 2, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
        {"id": "5169484183376", "name": "Luka", "surname": "Wood", "stageDone": 1, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
        {"id": "7493595926423", "name": "Dean", "surname": "Zartmann", "stageDone": 0, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
        {"id": "9993792601664", "name": "Carine", "surname": "Pretorius", "stageDone": 4, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False},
        {"id": "0005060772189", "name": "Chardi", "surname": "Snyman", "stageDone": 2, "Ankle": True, "Knee": False, "Hip": True, "Arm": False, "Wrist": False}
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

def test_calc_total(patients):
    assert calc_total(patients) == 7

def test_calc_in_progress(patients):
    assert calcInProgress(patients) == 5

def test_calc_completed(patients):
    assert calcCompleted(patients) == 2

def test_add_patient(patients):
    original_count = len(patients)

    add_patient(
        patients,
        "1423576436475",
        "Anica",
        "Ferreira",
        True,
        False,
        True,
        False,
        False
    )

    assert len(patients) == original_count + 1

    new_patient = patients[-1]

    assert new_patient["id"] == "1423576436475"
    assert new_patient["name"] == "Anica"
    assert new_patient["surname"] == "Ferreira"
    assert new_patient["stageDone"] == 1

def test_finalise_eval_creates_report(patients):

    reports = []

    finaliseEval(
        patients,
        reports,
        "5169484183376",
        "Luka",
        "Wood",
        True,
        False,
        True,
        False,
        False,
        "Mild",
        "Ankle note",
        "",
        "",
        "Moderate",
        "Hip note",
        "",
        "",
        "",
        ""
    )

    patient = next(
        p for p in patients
        if p["id"] == "5169484183376"
    )

    assert patient["stageDone"] == 2

    assert len(reports) == 1

def test_report_output_advances_stage(patients, capsys):

    reports = [
        [
            "ID: 8758944319328",
            "Name : Pieter",
            "Surname : Botha"
        ]
    ]

    reportOutput(
        patients,
        reports,
        "8758944319328"
    )

    patient = next(
        p for p in patients
        if p["id"] == "8758944319328"
    )

    assert patient["stageDone"] == 3

    captured = capsys.readouterr()

    assert "REPORT DETAILS" in captured.out

def test_final_report_advances_stage(patients):

    patient = next(
        p for p in patients
        if p["id"] == "1153060156238"
    )

    assert patient["stageDone"] == 3

    try:
        finalReport(
            patients,
            reports,
            "1153060156238"
        )
    except TypeError:
        pass

    assert patient["stageDone"] == 4

def test_complete_patient_workflow(patients):

    reports = []

    add_patient(
        patients,
        "1423576436475",
        "Anica",
        "Ferreira",
        True,
        False,
        True,
        False,
        False
    )

    patient = next(
        p for p in patients
        if p["id"] == "1423576436475"
    )

    assert patient["stageDone"] == 1

    finaliseEval(
        patients,
        reports,
        "1423576436475",
        "Anica",
        "Ferreira",
        True,
        False,
        True,
        False,
        False,
        "Mild",
        "Ankle injury",
        "",
        "",
        "Moderate",
        "Hip injury",
        "",
        "",
        "",
        ""
    )

    assert patient["stageDone"] == 2

    reportOutput(
        patients,
        reports,
        "1423576436475"
    )

    assert patient["stageDone"] == 3

finalReport(patients, reports, patientID)

assert patients["stageDone"] == 4
