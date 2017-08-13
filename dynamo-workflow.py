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


import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

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

    print("Adding subject:", code)

    points   = results['Credit points:']
    level    = results['Unit of study level:']
    sem      = results['Commencing semesters:']
    prereq   = results['Prerequisites']
    assumed  = results['Assumed knowledge']
    prohib   = results['Prohibitions']
    coreq    = results['Corequisites']
    info     = results['Additional Information']
    about    = results['UNIT OF STUDY']

    # print(points, level, sem, prereq, assumed, prohib, coreq, info, about)

    # table.put_item(
    #    Item={
    #        "code"    : code,
    #        "info"    : results
    #     }
    # )

    table.put_item(
       Item={
           "code"      : code,
           "points"    : str(points),
           "level"     : str(level),
           "sem"       : str(sem),
           "prereq"    : str(prereq),
           "assumed"   : str(assumed),
           "prohib"    : str(prohib),
           "coreq"     : str(coreq),
           "info"      : str(info),
           "about"     : str(about)
        }
    )



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

# LOCAL
# dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Subjects')


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
    print("test")
    uos = open('2129.html')
    old_soup = BeautifulSoup(uos, 'html.parser')

    results = parse_html(old_soup)
    print(results)

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

test_active = True
if test_active:
    test()



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
