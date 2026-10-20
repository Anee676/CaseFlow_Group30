/*
  File: static/js/sample-data.js
  Section: 1 
  Purpose: Invented patients for the demo. There is no database in the
           Semester Project, so every page reads its patients from here.
           No real patient data may ever be added to this file (POPIA).
*/

// The four stages a medico-legal report moves through, in order.
const STAGES = ["Evaluation", "Upload reports", "Extraction & compiling", "Finalised"];

// stagesDone holds one true/false value per stage, in the same order as STAGES.
const PATIENTS = [
  { id: "CF-0001", name: "Thabo", surname: "Mokoena", stagesDone: [true, true, true, true] },
  { id: "CF-0002", name: "Johan", surname: "van der Merwe", stagesDone: [true, true, true, false] },
  { id: "CF-0003", name: "Lerato", surname: "Dlamini", stagesDone: [true, true, false, false] },
  { id: "CF-0004", name: "Pieter", surname: "Botha", stagesDone: [true, false, false, false] },
  { id: "CF-0005", name: "Ayesha", surname: "Patel", stagesDone: [false, false, false, false] },
  { id: "CF-0006", name: "Marike", surname: "Steyn", stagesDone: [true, true, true, true] },
];

// A report counts as completed only once the last stage (Finalised) is done.
function isCompleted(patient) {
  return patient.stagesDone[STAGES.length - 1];
}

