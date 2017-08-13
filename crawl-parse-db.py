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



def database_connect():
    connection = None
    try:
        connection = pg8000.connect(user=None, host='localhost', unix_sock=None, port=5432, database='usyd', password=None, ssl=False, timeout=None)
    except pg8000.OperationalError as e:
        print(e)
    return connection



def get_html(link):
    fp = urllib.request.urlopen(link)
    mybytes = fp.read()
    html = mybytes.decode("utf8")
    fp.close()
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


def jsonify(results):

    { 'body' : {

        }
     }

    for entry in results:


def insert_data(results, code):

    test = [code, results['Credit points:'], results['Unit of study level:'],   results['Commencing semesters:'], results['Prerequisites'], results['Assumed knowledge'], results['Prohibitions'], results['Corequisites'], results['Additional Information'], results['UNIT OF STUDY']]

    cp = str(results['Credit points:'])
    level = str(results['Unit of study level:'])
    sem = str(results['Commencing semesters:'])
    prereq = str(results['Prerequisites'])
    ass = str(results['Assumed knowledge'])
    pro = str(results['Prohibitions'])
    cor = str(results['Corequisites'])
    add = str(results['Additional Information'])
    uos = str(results['UNIT OF STUDY'])


    print("testing")
    for e in test:
        if e is None:
            print(e)
            e = "n/a"
            print(e)
        e = str(e)
        # print(e)
    # return

    cp = str(results['Credit points:'])
    level = str(results['Unit of study level:'])
    sem = str(results['Commencing semesters:'])
    prereq = str(results['Prerequisites'])
    ass = str(results['Assumed knowledge'])
    pro = str(results['Prohibitions'])
    cor = str(results['Corequisites'])
    add = str(results['Additional Information'])
    uos = str(results['UNIT OF STUDY'])
    print(code, cp, level, sem, prereq, ass, pro, cor, add, uos)

    try:
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION;")

        # cursor.execute("""INSERT INTO Parsed
        #                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "");
        #                     """, (code, results['Credit points:'], results['Unit of study level:'], results['Commencing semesters:'], results['Prerequisites'], results['Assumed knowledge'], results['Prohibitions'], results['Corequisites'], results['Additional Information'], results['UNIT OF STUDY']))

        cursor.execute("""INSERT INTO Parsed
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "");
                            """, (code, cp, level, sem, prereq, ass, pro, cor, add, uos))

        cursor.execute("COMMIT;")
        cursor.close()
    except Exception as e:
        print("error")
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
codes_links = get_codes()
# print(codes)

def test():
    uos = open('2129.html')
    old_soup = BeautifulSoup(uos, 'html.parser')

    results = parse_html(old_soup)

    insert_data(results, 'COMP2129')



    # print(results)

test()


exit()


i = 0
for code_link in codes_links:
    link = code_link[1]
    code = code_link[0]
    # print(code)
    # print(link)
    html = get_html(link)
    if html:
        print(html)
        x = 1
    else:
        continue
    soup = BeautifulSoup(html, 'html.parser')

    results = parse_html(soup)
    print(code)
    for key in results:
        print(key)
        print(results[key])

    i += 1
    if i > 1:
        break
