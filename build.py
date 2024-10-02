import os

from db import create_table, create_connection
from schema import *


def insert_to_person(conn, person_data):
    """ Insert a new person into the Person table. """
    sql = """
    INSERT INTO Person (FirstName, LastName, Email, Phone, LinkedIn, Summary)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cur = conn.cursor()
    cur.execute(sql, person_data)
    conn.commit()

def insert_to_education(conn, education_data):
    """ Insert a new education record into the Education table. """
    sql = """
    INSERT INTO Education (PersonID, Degree, Institution, StartDate, EndDate, Description)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cur = conn.cursor()
    cur.execute(sql, education_data)
    conn.commit()

def insert_to_work_experience(conn, work_experience_data):
    """ Insert a new work experience record into the WorkExperience table. """
    sql = """
    INSERT INTO WorkExperience (PersonID, JobTitle, CompanyName, StartDate, EndDate, JobDescription)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cur = conn.cursor()
    cur.execute(sql, work_experience_data)
    conn.commit()

def main():
    database = "./pythonsqlite.db"

    # Create a database connection
    conn = create_connection(database)

    # Create all tables defined in schema
    create_table(conn, sql_create_person_table)
    create_table(conn, sql_create_education_table)
    create_table(conn, sql_create_work_experience_table)

    # Insert sample data into tables
    insert_sample_data(conn)

    print("Database build successful!")


def insert_sample_data(conn):
    # Sample data for multiple people
    persons = [
        ('John', 'Doe', 'john.doe@email.com', '123-456-7890',
         'https://linkedin.com/in/johndoe',
         'Experienced software developer with a focus on backend technologies.'),

        ('Jane', 'Smith', 'jane.smith@email.com', '234-567-8901',
         'https://linkedin.com/in/janesmith',
         'Project manager with over 5 years of experience in agile methodologies.'),

        ('Mike', 'Johnson', 'mike.johnson@email.com', '345-678-9012',
         'https://linkedin.com/in/mikejohnson',
         'Data scientist specializing in machine learning and data analysis.'),

        ('Emily', 'Davis', 'emily.davis@email.com', '456-789-0123',
         'https://linkedin.com/in/emilydavis',
         'UX designer with a passion for creating intuitive user experiences.'),

        ('David', 'Brown', 'david.brown@email.com', '567-890-1234',
         'https://linkedin.com/in/davidbrown',
         'Full-stack developer experienced in both front-end and back-end technologies.')
    ]

    # Insert sample data into Person
    person_ids = []
    for person_data in persons:
        person_id = insert_to_person(conn, person_data)
        person_ids.append(person_id)  # Store the PersonID for later use

    # Sample data for Education
    educations = [
        (person_ids[0], 'Bachelor of Science in Computer Science', 'Tech University',
         '2015-09-01', '2019-06-01',
         'Focused on software engineering, databases, and algorithms.'),

        (person_ids[1], 'Master of Business Administration', 'Business School',
         '2017-09-01', '2019-06-01',
         'Specialized in project management and leadership.'),

        (person_ids[2], 'Master of Science in Data Science', 'Data Institute',
         '2018-09-01', '2020-06-01',
         'Concentrated on machine learning, statistics, and big data technologies.'),

        (person_ids[3], 'Bachelor of Arts in Graphic Design', 'Art University',
         '2016-09-01', '2020-06-01',
         'Emphasized visual communication and user interface design.'),

        (person_ids[4], 'Bachelor of Science in Information Technology', 'Tech University',
         '2014-09-01', '2018-06-01',
         'Studied software development, networking, and security.')
    ]

    # Insert sample data into Education
    for education_data in educations:
        insert_to_education(conn, education_data)

    # Sample data for Work Experience
    work_experiences = [
        (person_ids[0], 'Software Developer', 'Tech Corp',
         '2019-07-01', '2023-08-01',
         'Developed and maintained backend systems using Go and Python.'),

        (person_ids[1], 'Project Manager', 'Management Solutions',
         '2019-08-01', '2023-09-01',
         'Led cross-functional teams and managed project timelines and deliverables.'),

        (person_ids[2], 'Data Scientist', 'Analytics Co.',
         '2020-01-01', '2023-08-01',
         'Built predictive models and performed data analysis to drive business decisions.'),

        (person_ids[3], 'UX Designer', 'Creative Agency',
         '2020-05-01', '2023-09-01',
         'Designed user interfaces and conducted user testing to enhance product usability.'),

        (person_ids[4], 'Full-Stack Developer', 'Startup Inc.',
         '2018-09-01', '2023-09-01',
         'Implemented and managed web applications and APIs for various clients.')
    ]

    # Insert sample data into Work Experience
    for work_experience_data in work_experiences:
        insert_to_work_experience(conn, work_experience_data)


if __name__ == "__main__":
    main()


