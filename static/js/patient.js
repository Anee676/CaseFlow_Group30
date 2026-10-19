/*
  File:    static/js/patient.js
  Section: 2 (patient and upload forms)
  Owner:   Beaulah Shaw
  Drafted: with AI assistance (Claude). See README, AI assistance.
  Purpose: Runs the patient form: builds the module side panel, shows and
           hides each module's fields, and checks the form before it moves on.
           There is no database in the Semester Project, so Save only checks
           the form and shows a message.
*/

// The report modules the therapist can tick. Adding a module to this list
// adds it to the side panel and the form, with no other changes needed.
const MODULES = [
  { code: "accident", name: "Accident details", field: "Role in accident",
    options: ["Driver", "Passenger", "Pedestrian", "Cyclist"] },
  { code: "imaging", name: "Scans & imaging", field: "Imaging type",
    options: ["X-ray", "MRI", "CT", "Multiple"] },
  { code: "ankle", name: "Ankle", field: "Severity", options: ["Mild", "Moderate", "Severe"] },
  { code: "knee", name: "Knee", field: "Severity", options: ["Mild", "Moderate", "Severe"] },
  { code: "hip", name: "Hip", field: "Severity", options: ["Mild", "Moderate", "Severe"] },
  { code: "arm", name: "Arm", field: "Severity", options: ["Mild", "Moderate", "Severe"] },
  { code: "wrist", name: "Wrist", field: "Severity", options: ["Mild", "Moderate", "Severe"] },
];

const message = document.getElementById("form-message");
const patientId = new URLSearchParams(window.location.search).get("id");

// ---------- Build the side panel and the module cards ----------

function buildModules() {
  const list = document.getElementById("module-list");
  const cards = document.getElementById("module-cards");

  MODULES.forEach((m) => {
    list.insertAdjacentHTML("beforeend", `
      <div class="form-check">
        <input class="form-check-input" type="checkbox" id="tick-${m.code}" data-module="${m.code}">
        <label class="form-check-label" for="tick-${m.code}">${m.name}</label>
      </div>`);

    // Each card starts hidden. It only appears once its module is ticked.
    const options = m.options.map((o) => `<option>${o}</option>`).join("");
    cards.insertAdjacentHTML("beforeend", `
      <div class="form-card module-card" id="card-${m.code}" hidden>
        <h2 class="h6">${m.name}</h2>
        <div class="row g-2">
          <div class="col-sm-5">
            <label class="form-label small" for="field-${m.code}">${m.field}</label>
            <select class="form-select form-select-sm" id="field-${m.code}" aria-describedby="field-${m.code}-error">
              <option value="">Choose...</option>${options}
            </select>
            <div class="invalid-feedback" id="field-${m.code}-error"></div>
          </div>
          <div class="col-sm-7">
            <label class="form-label small" for="notes-${m.code}">Evaluation notes</label>
            <textarea class="form-control form-control-sm" id="notes-${m.code}" rows="2"></textarea>
          </div>
        </div>
      </div>`);
  });

  // Ticking or unticking a module shows or hides its card.
  list.addEventListener("change", (event) => {
    const code = event.target.dataset.module;
    if (!code) return;
    document.getElementById(`card-${code}`).hidden = !event.target.checked;
    document.getElementById("no-modules-hint").hidden = tickedModules().length > 0;
  });
}

function tickedModules() {
  return MODULES.filter((m) => document.getElementById(`tick-${m.code}`).checked);
}

// ---------- Validation helpers ----------

// Mark a field as wrong and put the reason in its error box.
function showError(fieldId, text) {
  const field = document.getElementById(fieldId);
  if (field) field.classList.add("is-invalid");
  const box = document.getElementById(`${fieldId}-error`);
  box.textContent = text;
  box.classList.add("d-block");
}

function clearErrors() {
  document.querySelectorAll(".is-invalid").forEach((el) => el.classList.remove("is-invalid"));
  document.querySelectorAll(".invalid-feedback").forEach((el) => {
    el.textContent = "";
    el.classList.remove("d-block");
  });
  message.innerHTML = "";
}

// Checks the general information. Returns a list of the field ids that failed.
function checkGeneralInfo() {
  const failed = [];

  ["name", "surname"].forEach((id) => {
    if (document.getElementById(id).value.trim() === "") {
      showError(id, `${id === "name" ? "Name" : "Surname"} is required.`);
      failed.push(id);
    }
  });

  // A South African ID number is exactly 13 digits.
  const idNumber = document.getElementById("id-number").value.trim();
  if (!/^\d{13}$/.test(idNumber)) {
    showError("id-number", "The ID number must be exactly 13 digits.");
    failed.push("id-number");
  }

  if (!document.querySelector('input[name="gender"]:checked')) {
    showError("gender", "Choose male or female.");
    failed.push("gender-male");
  }

  // The date is optional, but an injury cannot happen in the future.
  const injuryDate = document.getElementById("injury-date").value;
  if (injuryDate && new Date(injuryDate) > new Date()) {
    showError("injury-date", "The date of injury cannot be in the future.");
    failed.push("injury-date");
  }

  return failed;
}

// Mark complete needs more than Save: at least one module, each with a value.
function checkModules() {
  const failed = [];
  const ticked = tickedModules();

  if (ticked.length === 0) {
    message.innerHTML = '<div class="alert alert-danger">Tick at least one report module before marking the evaluation complete.</div>';
    failed.push(`tick-${MODULES[0].code}`);
  }

  ticked.forEach((m) => {
    if (document.getElementById(`field-${m.code}`).value === "") {
      showError(`field-${m.code}`, `Choose a ${m.field.toLowerCase()} for ${m.name}.`);
      failed.push(`field-${m.code}`);
    }
  });

  return failed;
}

// Move the cursor to the first problem so keyboard users find it at once.
function focusFirst(failed) {
  if (failed.length > 0) document.getElementById(failed[0]).focus();
}

function showSuccess(text) {
  message.innerHTML = `<div class="alert alert-success">${text}</div>`;
}

// ---------- Buttons ----------

document.getElementById("save-btn").addEventListener("click", () => {
  clearErrors();
  const failed = checkGeneralInfo();
  if (failed.length > 0) return focusFirst(failed);
  showSuccess("Saved. (Demo only: nothing is stored until the database is added in the final project.)");
});

document.getElementById("complete-btn").addEventListener("click", () => {
  clearErrors();
  const failed = [...checkGeneralInfo(), ...checkModules()];
  if (failed.length > 0) return focusFirst(failed);
  showSuccess(`Evaluation marked complete with ${tickedModules().length} module(s). Next, upload the specialist reports.`);
});

// Next checks the general information, then opens the upload page for this patient.
document.getElementById("next-btn").addEventListener("click", () => {
  clearErrors();
  const failed = checkGeneralInfo();
  if (failed.length > 0) return focusFirst(failed);
  const id = patientId || "new";
  window.location.href = `uploads.html?id=${encodeURIComponent(id)}`;
});

// ---------- Start ----------

buildModules();

// When the page is opened from the dashboard, fill in that patient's name.
const existing = PATIENTS.find((p) => p.id === patientId);
if (existing) {
  document.getElementById("page-title").textContent = `${existing.name} ${existing.surname} (${existing.id})`;
  document.getElementById("name").value = existing.name;
  document.getElementById("surname").value = existing.surname;
}