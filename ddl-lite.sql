    -- entry['faculty']
    -- entry['area_of_study']
    -- entry['area_of_study_code']
    -- entry['level']
    -- entry['offered']
    -- entry['unit_code']
    -- entry['unit_name']
    -- entry['more_info']
    -- points   = results['Credit points:']
    -- level    = results['Unit of study level:']
    -- sem      = results['Commencing semesters:']
    -- prereq   = results['Prerequisites']
    -- assumed  = results['Assumed knowledge']
    -- prohib   = results['Prohibitions']
    -- coreq    = results['Corequisites']
    -- info     = results['Additional Information']
    -- about    = results['UNIT OF STUDY']


CREATE TABLE SubjectInfo(

    unit_code TEXT PRIMARY KEY NOT NULL,
    unit_name TEXT,
    faculty TEXT,
    area_of_study TEXT,
    area_of_study_code TEXT,
    level TEXT,
    offered TEXT,
    link TEXT,
    credit_points TEXT,
    old_level TEXT,
    semester TEXT,
    prerequisite TEXT,
    assumed_knowledge TEXT,
    prohibitions TEXT,
    corequisites TEXT,
    additional_info TEXT,
    about TEXT


)

-- unit_code, unit_name, faculty, area_of_study, area_of_study_code, level, offered, link, credit_points, old_level, semester, prerequisite, assumed_knowledge, prohibitions, corequisites, additional_info, about
