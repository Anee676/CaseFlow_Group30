INSERT INTO Reports (Date_Start_Report, DateEndReport, ReportString) VALUES
('2024-01-16', '2024-02-20', 'Patient presented with a lateral ankle sprain. Physiotherapy recommended for 6 weeks. Full recovery expected.'),
('2024-03-05', NULL,         'Suspected ACL tear following a fall during a rugby match. MRI scheduled - surgical consult pending.'),
('2024-04-12', '2024-06-30', 'Fractured wrist sustained in a cycling accident. Cast applied for 6 weeks, followed by rehabilitation.'),
('2024-05-22', NULL,         'Hip pain following a vehicle collision. Ongoing monitoring - imaging shows no fracture.'),
('2024-07-08', '2024-08-15', 'Multiple injuries (arm and knee) from a workplace fall. Soft tissue damage only. Cleared for light duties.'),
('2024-09-01', NULL,         NULL);

INSERT INTO Patients (Patient_id, Patient_Name, Patient_Surname, Patient_DoB) VALUES
('9003145123083', 'Thabo',  'Mokoena',      '1990-03-14'),
('8511020234087', 'Sarah',  'van der Merwe', '1985-11-02'),
('9807230345084', 'Priya',  'Naidoo',       '1998-07-23'),
('7201305456081', 'James',  'Smith',        '1972-01-30'),
('0309090567085', 'Lerato', 'Dlamini',      '2003-09-09');

INSERT INTO Cases
    (Injury_date, Accident_Details, Scans_Imagery,
     Ankle_injury, Knee_injury, Hip_injury, Arm_injury, Wrist_injury, 
     Ankle_details, Knee_details, Hip_details, Arm_details, Wrist_details,
     Report_id, Patient_id, Case_progress, Report_status)
VALUES
('2024-01-10', 'Rolled ankle while playing five-a-side football on an uneven pitch.',
    'scans/case1_ankle_xray.jpg',
    1, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, 1, '9003145123083', 75, 'Report drafted'),

('2024-03-02', 'Twisted knee after being tackled during a rugby match.',
    'scans/case2_knee_mri.dcm',
    0, 1, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, 2, '8511020234087', 50, 'Report in Progress'),

('2024-04-09', 'Fell off a bicycle at speed, landing on an outstretched hand.',
    'scans/case3_wrist_xray.jpg',
    0, 0, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, 3, '9807230345084', 100, 'Report finalised'),

('2024-05-18', 'Rear-ended at a traffic light, causing impact to the hip.',
    'scans/case4_hip_ct.dcm',
    0, 0, 1, 0, 0, NULL, NULL, NULL, NULL, NULL, 4, '7201305456081', 50, 'Report in Progress'),

('2024-07-04', 'Slipped from a ladder at work, landing on the right arm and knee.',
    NULL,
    0, 1, 0, 1, 0, NULL, NULL, NULL, NULL, NULL, 5, '0309090567085', 50, 'Report in Progress'),

('2024-08-28', 'Second ankle injury, rolled it again on a trail run.',
    'scans/case6_ankle_xray.jpg',
    1, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, 6, '9003145123083', 50, 'Report in progress');