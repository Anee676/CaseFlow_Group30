# CaseFlow (BFB321 Semester Project, group 30)

CaseFlow is a web tool for the medico-legal reporting workflow at an occupational therapy practice. It replaces a "delete what doesn't apply" report template with modules the therapist ticks, and it shows where every patient's report stands.

This is the Semester Project submission. It covers the two semester deliverables from the BFB321 development guide: the frontend build and the supply chain model.

## How to open it

Open the folder in VS Code and open `index.html` in a browser. The Live Server extension works too. There is no login, server or database in this version. Patients come from `static/js/sample-data.js` and are invented.

To run the model tests (section 3):

```
python -m pytest
```

## Sections

| Section | Student | Files |
|---|---|---|
| 1. Layout and dashboard | Anée van Eeden | `README.md`, `static/css/style.css`, `static/js/sample-data.js`, `index.html`, `static/js/dashboard.js` |
| 2. Patient and upload forms | Beaulah Shaw | `patient.html`, `static/js/patient.js`, `uploads.html`, `static/js/uploads.js`, `static/css/forms.css` | 
| 3. Model and impact page | Talia van Sittert | `models/capacity.py`, `tests/test_capacity.py`, `impact.html` |

## Shared style

Every page links `static/css/style.css` and copies the navbar from `index.html`. Font is Times New Roman. Colours are navy `#14284b`, teal `#17878c` and white. Use the colour, font-size and spacing variables at the top of `style.css` rather than new values.

## AI assistance

Record here any AI help used, as the BFB321 rules require.

- Section 1: the first draft of the stylesheet, sample data, dashboard page and script was generated with Claude (Anthropic) from our planning notes and the development guide. Changes made after that are in the commit history.

- Section 2: the first draft of the patient form, upload page, their scripts and forms.css was generated with Claude (Anthropic) from our planning notes and the development guide. Changes made after that are in the commit history.

