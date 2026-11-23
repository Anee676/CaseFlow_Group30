
CREATE TABLE IF NOT EXISTS Reports (
    Report_id        INT AUTO_INCREMENT PRIMARY KEY,
    Date_Start_Report DATE NOT NULL,
    DateEndReport    DATE NULL,
    ReportString     LONGTEXT NULL
);

CREATE TABLE IF NOT EXISTS Patients (
    Patient_id       VARCHAR(13) PRIMARY KEY,
    Patient_Name     VARCHAR(60) NOT NULL,
    Patient_Surname  VARCHAR(60) NOT NULL,
    Patient_DoB      DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Cases (
    Case_id          INT AUTO_INCREMENT PRIMARY KEY,
    Injury_date      DATE NULL,
    Accident_Details LONGTEXT NULL,
    Scans_Imagery    LONGTEXT NULL,
    Ankle_injury     BOOLEAN NOT NULL DEFAULT 0,
    Knee_injury      BOOLEAN NOT NULL DEFAULT 0,
    Hip_injury       BOOLEAN NOT NULL DEFAULT 0,
    Arm_injury       BOOLEAN NOT NULL DEFAULT 0,
    Wrist_injury     BOOLEAN NOT NULL DEFAULT 0,
    Ankle_details     LONGTEXT NULL,
    Knee_details      LONGTEXT NULL,
    Hip_details       LONGTEXT NULL,
    Arm_details       LONGTEXT NULL,
    Wrist_details     LONGTEXT NULL,
    Report_id        INT NOT NULL,
    Patient_id       VARCHAR(13) NULL,
    Case_progress    INT NOT NULL DEFAULT 0,
    Report_status    VARCHAR(20) NOT NULL DEFAULT 'Not Started',

    CONSTRAINT fk_cases_report  FOREIGN KEY (Report_id)  REFERENCES Reports (Report_id),
    CONSTRAINT fk_cases_patient FOREIGN KEY (Patient_id) REFERENCES Patients (Patient_id),
    CONSTRAINT uq_cases_report  UNIQUE (Report_id),
    CONSTRAINT chk_cases_ankle  CHECK (Ankle_injury IN (0, 1)),
    CONSTRAINT chk_cases_knee   CHECK (Knee_injury IN (0, 1)),
    CONSTRAINT chk_cases_hip    CHECK (Hip_injury IN (0, 1)),
    CONSTRAINT chk_cases_arm    CHECK (Arm_injury IN (0, 1)),
    CONSTRAINT chk_cases_wrist  CHECK (Wrist_injury IN (0, 1)),
    CONSTRAINT chk_cases_progress CHECK (Case_progress BETWEEN 0 AND 100)
);