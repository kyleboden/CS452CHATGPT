sql_create_person_table = """
    CREATE TABLE IF NOT EXISTS Person (
        PersonID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        Phone TEXT,
        LinkedIn TEXT,
        Summary TEXT
    );
"""

sql_create_education_table = """
    CREATE TABLE IF NOT EXISTS Education (
        EducationID INTEGER PRIMARY KEY AUTOINCREMENT,
        PersonID INTEGER,
        Degree TEXT NOT NULL,
        Institution TEXT NOT NULL,
        StartDate DATE NOT NULL,
        EndDate DATE,
        Description TEXT,
        FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
    );
"""

sql_create_work_experience_table = """
    CREATE TABLE IF NOT EXISTS WorkExperience (
        WorkExperienceID INTEGER PRIMARY KEY AUTOINCREMENT,
        PersonID INTEGER,
        JobTitle TEXT NOT NULL,
        CompanyName TEXT NOT NULL,
        StartDate DATE NOT NULL,
        EndDate DATE,
        JobDescription TEXT,
        FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
    );
"""