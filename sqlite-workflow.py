'''
Get codes

Get link for that code

Get HTML for code

Parse HTML

Insert into Parsed
'''
# from __future__ import print_function # Python 2/3 compatibility
from modules import pg8000
import configparser
import urllib.request
from bs4 import BeautifulSoup



def database_connect():
    connection = None
    try:
        connection = pg8000.connect(user=None, host='localhost', unix_sock=None, port=5432, database='usyd', password=None, ssl=False, timeout=None)
    except pg8000.OperationalError as e:
        print(e)
    return connection

def get_html(link):
    try:
        fp = urllib.request.urlopen(link)
        mybytes = fp.read()
        html = mybytes.decode("utf8")
        fp.close()
    except:
        print("error")
        return None
    return html

def get_codes():
    codes = []
    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT faculty, area_of_study, area_of_study_code, level, offered, unit_code, unit_name, more_info FROM Subjects
                            ORDER BY unit_code;""")
        codes = cursor.fetchall()
        cursor.close()
    except pg8000.OperationalError as e:
        print(e)

    results = []

    for course in codes:
        results.append(
            {   'faculty'               :   course[0],
                'area_of_study'         :   course[1],
                'area_of_study_code'    :   course[2],
                'level'                 :   course[3],
                'offered'               :   course[4],
                'unit_code'             :   course[5],
                'unit_name'             :   course[6],
                'more_info'             :   course[7]

                        }
                )

    return results

def prepare(results, code):

    done = {
        "code"      : code,
        "points"    : results['Credit points:'],
        "level"     : results['Unit of study level:'],
        "sem"       : results['Commencing semesters:'],
        "prereq"    : results['Prerequisites'],
        "assumed"   : results['Assumed knowledge'],
        "prohib"    : results['Prohibitions'],
        "coreq"     : results['Corequisites'],
        "info"      : results['Additional Information'],
        "about"     : results['UNIT OF STUDY']
     }

    return done


def insert_data(entry, results, code):




    print("Adding subject:", code)

    unit_code = entry['unit_code']
    unit_name =     entry['unit_name']
    faculty =     entry['faculty']
    area_of_study =     entry['area_of_study']
    area_of_study_code =    entry['area_of_study_code']
    level = entry['level']
    offered = entry['offered']
    link = entry['more_info']
    credit_points = results['Credit points:']
    old_level = results['Unit of study level:']
    semester = results['Commencing semesters:']
    prerequisite = results['Prerequisites']
    assumed_knowledge = results['Assumed knowledge']
    prohibitions = results['Prohibitions']
    corequisites = results['Corequisites']
    additional_info = results['Additional Information']
    about = results['UNIT OF STUDY']

    try:
        c = conn.cursor()
        c.execute("""INSERT INTO SubjectInfo VALUES
                         (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                         ?, ?, ?, ?, ?, ?, ?);
                         """, (unit_code, unit_name, faculty, area_of_study, area_of_study_code, level, offered, link, credit_points, old_level, semester, prerequisite, assumed_knowledge, prohibitions, corequisites, additional_info, about))
        conn.commit()
    except Exception as e:
        print("Error adding subject: " + code)
        print("Exception")
        print(e)



def get_text(tag, type, soup):
    try:
        loc = soup.find(string=tag)
    except Exception as e:
        print(e)


    if loc is None:
        return None
    text = loc.find_next(type).string
    return text




def parse_html(soup):
    tags_p = [
        'Prerequisites',
        'Assumed knowledge',
        'Prohibitions',
        'Corequisites',
        'Additional Information',
        'UNIT OF STUDY'
    ]
    tags_span = [
        'Credit points:',
        'Unit of study level:',
        'Commencing semesters:'
    ]
    results = {}

    for tag in tags_p:
        results[tag] = get_text(tag, 'p', soup)
        # print(tag)
        # print(get_text(tag, 'p'))

    for tag in tags_span:
        results[tag] = get_text(tag, 'span', soup)
        # print(tag)
        # print(get_text(tag, 'span'))


    return results






connection = database_connect()
pgsql_results = get_codes()



import sqlite3

conn = sqlite3.connect('CoursePlanner.db')



def delete_item(code):

    try:
        response = table.delete_item(
            Key={
                'code': code
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        print("DeleteItem succeeded:")


def test():
    uos = open('2129.html')
    old_soup = BeautifulSoup(uos, 'html.parser')

    results = parse_html(old_soup)
    # print(results)

    # TESTING delete and add funcionality

    # table.put_item(
    #    Item={
    #        "code"      : 'TEST1234',
    #        "points"    : '6 credit points'
    #     }
    # )

    # delete_item('test1234')


    # response = table.query(KeyConditionExpression=Key('code').eq('COMP2129'))
    #
    # for i in response['Items']:
    #     print(i)

    # insert_data(results, 'COMP2129')



    # print(results)
    exit()

print(pgsql_results[0]['unit_code'])

test_active = False
if test_active:
    test()



for entry in pgsql_results:
    link = entry['more_info']
    code = entry['unit_code']
    # print(code)
    # print(link)
    html = get_html(link)
    if html is None:
        continue

    soup = BeautifulSoup(html, 'html.parser')

    results = parse_html(soup)


    insert_data(entry, results, code)


conn.close()
