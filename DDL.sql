


DROP TABLE IF EXISTS Subjects;
DROP TABLE IF EXISTS Html;

CREATE TABLE Subjects (

    faculty VARCHAR,

    area_of_study VARCHAR,

    area_of_study_code VARCHAR,

    level VARCHAR,

    offered VARCHAR,

    unit_code VARCHAR PRIMARY KEY,

    unit_name VARCHAR,

    more_info VARCHAR

);

CREATE TABLE Html (

    unit_code VARCHAR PRIMARY KEY REFERENCES Subjects(unit_code),

    html VARCHAR
);
