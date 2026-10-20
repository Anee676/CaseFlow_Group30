/*
  File:    static/js/uploads.js
  Section: 2 
  Purpose: Runs the upload page: adds and removes specialist rows, colours
           each row by whether its file is chosen, and refuses Mark complete
           while any report is missing.
*/

const SPECIALISTS = ["Orthopaedic Surgeon", "Neurologist", "Psychologist", "Other"];

const rowsBox = document.getElementById("upload-rows");
const message = document.getElementById("upload-message");
const patientId = new URLSearchParams(window.location.search).get("id");

// Each row gets its own number so its label and inputs have unique ids.
let nextRowNumber = 1;

// ---------- Rows ----------

function addRow(specialist) {
  const n = nextRowNumber++;
  const options = SPECIALISTS.map(
    (s) => `<option ${s === specialist ? "selected" : ""}>${s}</option>`
  ).join("");

  rowsBox.insertAdjacentHTML("beforeend", `
    <div class="upload-row" id="row-${n}">
      <div>
        <label class="form-label small" for="specialist-${n}">Specialist</label>
        <select class="form-select form-select-sm" id="specialist-${n}">${options}</select>
      </div>
      <div>
        <label class="form-label small" for="file-${n}">Report file</label>
        <input class="form-control form-control-sm" type="file" id="file-${n}" accept=".pdf,.doc,.docx">
        <span class="upload-status" id="status-${n}">Outstanding</span>
      </div>
      <button class="btn btn-outline-danger btn-sm" type="button" data-remove="${n}"
              aria-label="Remove this specialist row">&minus;</button>
    </div>`);

  updateCount();
}

// A row turns green and says "Received" once a file is chosen.
rowsBox.addEventListener("change", (event) => {
  if (event.target.type !== "file") return;
  const n = event.target.id.split("-")[1];
  const hasFile = event.target.files.length > 0;
  document.getElementById(`row-${n}`).classList.toggle("has-file", hasFile);
  document.getElementById(`status-${n}`).textContent = hasFile
    ? `Received: ${event.target.files[0].name}`
    : "Outstanding";
  updateCount();
});

// The minus button removes its own row.
rowsBox.addEventListener("click", (event) => {
  const n = event.target.dataset.remove;
  if (!n) return;
  document.getElementById(`row-${n}`).remove();
  updateCount();
});

document.getElementById("add-row-btn").addEventListener("click", () => {
  addRow(SPECIALISTS[0]);
  // Put the cursor in the new row so the user can pick the specialist straight away.
  document.getElementById(`specialist-${nextRowNumber - 1}`).focus();
});

// ---------- Counting and checking ----------

function allRows() {
  return [...rowsBox.querySelectorAll(".upload-row")];
}

function missingRows() {
  return allRows().filter((row) => !row.classList.contains("has-file"));
}

function updateCount() {
  const total = allRows().length;
  document.getElementById("upload-count").textContent =
    `${total - missingRows().length} of ${total} received`;
}

function showMessage(type, html) {
  message.innerHTML = `<div class="alert alert-${type}">${html}</div>`;
}

// ---------- Buttons ----------

document.getElementById("save-btn").addEventListener("click", () => {
  showMessage("success", "Saved. (Demo only: files are not stored until the final project.)");
});

// Business rule from our planning notes: the step cannot be completed
// while any specialist report is still missing.
document.getElementById("complete-btn").addEventListener("click", () => {
  if (allRows().length === 0) {
    showMessage("danger", "Add at least one specialist report before marking this step complete.");
    return;
  }
  const missing = missingRows();
  if (missing.length > 0) {
    const names = missing
      .map((row) => `<li>${row.querySelector("select").value}</li>`)
      .join("");
    showMessage("danger", `These reports are still missing:<ul class="mb-0">${names}</ul>`);
    missing[0].querySelector('input[type="file"]').focus();
    return;
  }
  showMessage("success", "All reports received. This step is complete.");
});

// ---------- Start ----------

// Show which patient this is, and send Previous back to the same patient.
const existing = PATIENTS.find((p) => p.id === patientId);
if (existing) {
  document.getElementById("patient-label").textContent =
    `${existing.name} ${existing.surname} (${existing.id})`;
}
if (patientId) {
  document.getElementById("previous-btn").href = `patient.html?id=${encodeURIComponent(patientId)}`;
}

// Start with the three specialists most patients see.
addRow("Orthopaedic Surgeon");
addRow("Neurologist");
addRow("Psychologist");