CREATE TABLE IF NOT EXISTS Department (
    DepartmentName VARCHAR(255),
    DepartmentCode CHAR(4) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Program (
    ProgramName VARCHAR(255) PRIMARY KEY,
    PersonInChargeUniversityID INT,
    DepartmentCode CHAR(4),
    FOREIGN KEY (PersonInChargeUniversityID) REFERENCES Faculty(FacultyID),
    FOREIGN KEY (DepartmentCode) REFERENCES Department(DepartmentCode)
);

CREATE TABLE IF NOT EXISTS Faculty (
    FacultyID INT PRIMARY KEY,
    FacultyName VARCHAR(255),
    FacultyEmail VARCHAR(255),
    FacultyRank ENUM('full', 'associate', 'assistant', 'adjunct'),
    DepartmentCode CHAR(4),
    FOREIGN KEY (DepartmentCode) REFERENCES Department(DepartmentCode)
);

CREATE TABLE IF NOT EXISTS Course (
    CourseID CHAR(8) PRIMARY KEY,
    CourseTitle VARCHAR(255),
    CourseDescription TEXT,
    DepartmentCode CHAR(4),
    FOREIGN KEY (DepartmentCode) REFERENCES Department(DepartmentCode)
);

CREATE TABLE IF NOT EXISTS Section (
    SectionNumber CHAR(3),
    Semester ENUM('Fall', 'Spring', 'Summer'),
    Year YEAR,
    CourseID CHAR(8),
    FacultyID INT,
    NumberOfStudents INT,
    PRIMARY KEY (SectionNumber, CourseID, Semester, Year),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- added course ID as primary key
CREATE TABLE IF NOT EXISTS LearningObjective (
    ObjectiveCode CHAR(8) PRIMARY KEY,
    ObjectiveDescription TEXT,
    ProgramName VARCHAR(255),
    FOREIGN KEY (ProgramName) REFERENCES Program(ProgramName)
);

CREATE TABLE IF NOT EXISTS SubObjective (
    SubObjectiveCode CHAR(10) PRIMARY KEY,
    SubObjectiveDescription TEXT,
    ObjectiveCode CHAR(8),
    FOREIGN KEY (ObjectiveCode) REFERENCES LearningObjective(ObjectiveCode)
);

-- Dont need this 
-- CREATE TABLE IF NOT EXISTS ProgramCourse (
--     ProgramName VARCHAR(255),
--     CourseID CHAR(8),
--     PRIMARY KEY (ProgramName, CourseID),
--     FOREIGN KEY (ProgramName) REFERENCES Program(ProgramName),
--     FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
-- );

-- fixed to make objectivecode not part of the key
CREATE TABLE IF NOT EXISTS ProgramCourseObjective (
    ProgramName VARCHAR(255),
    CourseID CHAR(8),
    ObjectiveCode CHAR(8),
    PRIMARY KEY (ProgramName, CourseID),
    FOREIGN KEY (ProgramName) REFERENCES Program(ProgramName),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (ObjectiveCode) REFERENCES LearningObjective(ObjectiveCode)
);


CREATE TABLE IF NOT EXISTS SectionObjective (
    SectionNumber CHAR(3),
    CourseID CHAR(8),
    Semester ENUM('Fall', 'Spring', 'Summer'),
    Year YEAR,
    ObjectiveCode CHAR(8),
    EvaluationMethod VARCHAR(255),
    NumberOfStudentsMet INT,
    PRIMARY KEY (SectionNumber, Semester, Year, ObjectiveCode),
    FOREIGN KEY (SectionNumber, CourseID, Semester, Year) REFERENCES Section(SectionNumber, CourseID, Semester, Year),
    FOREIGN KEY (ObjectiveCode) REFERENCES LearningObjective(ObjectiveCode)
);