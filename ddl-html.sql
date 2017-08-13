





DROP TABLE Parsed;

CREATE TABLE Parsed (

    unit_code VARCHAR PRIMARY KEY REFERENCES Subjects(unit_code),

    dump JSON

);
