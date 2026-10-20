/*
  File: static/js/dashboard.js
  Section: 1 
  Purpose: Builds the patient database page from sample-data.js: the summary
           counts, the sorted patient table and the search filter.
*/

const tableBody = document.getElementById("patient-rows");
const searchBox = document.getElementById("search");
const tableBox = document.getElementById("table-box");
const emptyState = document.getElementById("empty-state");

// Count total, in-progress and completed patients for the summary bar.
function showSummary() {
  const completed = PATIENTS.filter(isCompleted).length;
  document.getElementById("count-total").textContent = PATIENTS.length;
  document.getElementById("count-progress").textContent = PATIENTS.length - completed;
  document.getElementById("count-completed").textContent = completed;
}

// Incomplete records go to the top, as our notes ask. Within each group the
// patient with the fewest stages done comes first, because they need the most work.
function sortPatients(list) {
  return [...list].sort((a, b) => {
    if (isCompleted(a) !== isCompleted(b)) {
      return isCompleted(a) ? 1 : -1;
    }
    const doneA = a.stagesDone.filter(Boolean).length;
    const doneB = b.stagesDone.filter(Boolean).length;
    return doneA - doneB;
  });
}

// One coloured block per stage. The hidden text lets screen readers say
// which stages are done, since colour alone is not enough.
function progressBlocks(patient) {
  const blocks = patient.stagesDone
    .map((done, i) => {
      const state = done ? "done" : "not-done";
      return `<span class="block ${state}" title="${STAGES[i]}: ${done ? "done" : "not done"}"></span>`;
    })
    .join("");
  const doneCount = patient.stagesDone.filter(Boolean).length;
  return `<span class="progress-blocks">${blocks}</span>
          <span class="visually-hidden">${doneCount} of ${STAGES.length} stages done</span>`;
}

function statusBadge(patient) {
  return isCompleted(patient)
    ? '<span class="badge badge-completed">Completed</span>'
    : '<span class="badge badge-progress">In progress</span>';
}

// Draw the table rows for the patients that match the search.
function showTable(searchText) {
  const text = searchText.trim().toLowerCase();
  const matches = PATIENTS.filter((p) =>
    `${p.id} ${p.name} ${p.surname}`.toLowerCase().includes(text)
  );

  // Show the empty state instead of an empty table when nothing matches.
  tableBox.hidden = matches.length === 0;
  emptyState.hidden = matches.length > 0;

  tableBody.innerHTML = sortPatients(matches)
    .map(
      (p) => `
      <tr tabindex="0" data-id="${p.id}">
        <td>${p.id}</td>
        <td>${p.name}</td>
        <td>${p.surname}</td>
        <td>${progressBlocks(p)}</td>
        <td>${statusBadge(p)}</td>
      </tr>`
    )
    .join("");
}

// Clicking a row, or pressing Enter on it, opens that patient for editing.
function openPatient(row) {
  window.location.href = `patient.html?id=${encodeURIComponent(row.dataset.id)}`;
}

tableBody.addEventListener("click", (event) => {
  const row = event.target.closest("tr");
  if (row) openPatient(row);
});

tableBody.addEventListener("keydown", (event) => {
  const row = event.target.closest("tr");
  if (row && event.key === "Enter") openPatient(row);
});

// Filter as the user types.
searchBox.addEventListener("input", () => showTable(searchBox.value));

document.getElementById("clear-search").addEventListener("click", () => {
  searchBox.value = "";
  showTable("");
  searchBox.focus();
});

showSummary();
showTable("");