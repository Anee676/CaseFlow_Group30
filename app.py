import os
from flask import Flask, flash, redirect, render_template, request, url_for
import db
from models import caseflow as models

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-me")
db.init_app(app)

@app.route("/")
def index():
    status = request.args.get("status", "all")
    if status == "in_progress":
        cases = models.display_in_progress()
    elif status == "completed":
        cases = models.display_completed()
    else:
        status = "all"
        cases = models.display_all()

    return render_template(
            "caseflowIndex.html",
            total_cases=models.count_cases(),
            in_progress=models.count_in_progress(),
            completed=models.count_completed(),
            cases=cases,
            status=status,
        )

@app.route("/cases/new", methods=["POST"])
def case_new():
    case_id = models.add_case()
    flash("New case created. Fill in the details and save.", "success")
    return redirect(url_for("case_details", case_id=case_id))

# button value: (progress, status)
ACTIONS = {
    "save": (50, "Report in progress"),
    "next":     (75,  "Report drafted"),
    "finalise": (100, "Report finalised"),
}

@app.route("/cases/<int:case_id>", methods=["GET", "POST"])
def case_details(case_id):
    case = models.get_case(case_id)
    if case is None:
        flash("Case not found.", "error")
        return redirect(url_for("index"))

    finalised = case["Report_status"] == "Report finalised"
    patient_locked = bool(case["Patient_id"])   # decided from the database, not the form

    if request.method == "POST":
        if finalised:
            if request.form.get("action") == "next":
                return redirect(url_for("case_details", case_id=case_id))
            flash("This report is finalised and can no longer be edited.", "error")
            return redirect(url_for("case_details", case_id=case_id))
         
        values, errors = models.validate_case(request.form)   # this creates errors and values

        if not errors:
            action = request.form.get("action", "save")
            if action not in ACTIONS:
                action = "save"
            progress, status = ACTIONS[action]

            progress, status = ACTIONS[action]

            if action == "next":
                values["ReportString"] = models.build_report_text(values)

            ok, message = models.update_case(case_id, values, progress, status)
            flash(message, "success" if ok else "error")
            if ok and action == "next":
                return redirect(url_for("case_details", case_id=case_id))
            return redirect(url_for("case_details", case_id=case_id))

        for e in errors:                  # validation failed: show each message
            flash(e, "error")
        case = {**case, **values}         # keep what the user typed

    return render_template("addinfo.html", case=case, patient_locked=patient_locked, finalised=finalised)


@app.route("/cases/<int:case_id>/report", methods=["GET", "POST"])
def final_report(case_id):
    case = models.get_case(case_id)
    if case is None:
        flash("Case not found.", "error")
        return redirect(url_for("index"))

    finalised = case["Report_status"] == "Report finalised"

    if request.method == "POST":
        if finalised:
            flash("This report is finalised and can no longer be edited.", "error")
        elif request.form.get("action") == "finalise":
            models.finalise_report(case_id, request.form.get("report_string", ""))
            flash("Report finalised.", "success")
        else:
            models.update_report_string(case_id, request.form.get("report_string", ""))
            flash("Report saved.", "success")
        return redirect(url_for("final_report", case_id=case_id))

    return render_template("finalReport.html", case=case, finalised=finalised)

#Post only route, to delete a case and its associated records
@app.route("/cases/<int:case_id>/delete", methods=["POST"])
def case_delete(case_id):
    ok, message = models.delete_case(case_id)
    flash(message, "success" if ok else "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

