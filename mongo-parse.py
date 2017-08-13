'''
Get codes

Get link for that code

Get HTML for code

Parse HTML

Insert into Parsed
'''
from modules import pg8000
import configparser
import urllib.request
from bs4 import BeautifulSoup

import pymongo
from pymongo import MongoClient

def database_connect():
    connection = None
    try:
        connection = pg8000.connect(user=None, host='localhost', unix_sock=None, port=5432, database='usyd', password=None, ssl=False, timeout=None)
    except pg8000.OperationalError as e:
        print(e)
    return connection

def mongo_connect():
    client = MongoClient('localhost', 27017)
    db = client.test_data
    return db

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
        cursor.execute("""SELECT unit_code, more_info FROM Subjects
                            ORDER BY unit_code;""")
        codes = cursor.fetchall()
        cursor.close()
    except pg8000.OperationalError as e:
        print(e)
    return codes


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


def insert_data(results, code):

    # test = [code, results['Credit points:'], results['Unit of study level:'],   results['Commencing semesters:'], results['Prerequisites'], results['Assumed knowledge'], results['Prohibitions'], results['Corequisites'], results['Additional Information'], results['UNIT OF STUDY']]




    subject = prepare(results, code)

    client = MongoClient('localhost', 27017)
    db = client.test_data

    subjects = db.subjects
    code_id = subjects.insert_one(subject).inserted_id


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
codes_links = get_codes()
# print(codes)

# def test():
#     uos = open('2129.html')
#     old_soup = BeautifulSoup(uos, 'html.parser')
#
#     results = parse_html(old_soup)
#
#     insert_data(results, 'COMP2129')
#
#
#
#     # print(results)
#
# test()


# exit()




for code_link in codes_links:
    link = code_link[1]
    code = code_link[0]
    # print(code)
    # print(link)
    html = get_html(link)
    if html is None:
        continue

    soup = BeautifulSoup(html, 'html.parser')

    results = parse_html(soup)

    insert_data(results, code)
