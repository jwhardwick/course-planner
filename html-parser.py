'''


Description of subject
Courses that offer this subject

Prereqs
Assumed Knowledge
Prohibitions
Coreqs

Credit Points
Study Level
Commencing Semester


'''

from modules import pg8000
import configparser
import urllib.request

from bs4 import BeautifulSoup

uos = open('2129.html')

old_soup = BeautifulSoup(uos, 'html.parser')

# prereq = soup.find(string="Prerequisites").find_next("p").string
# print(prereq)
# assumed = soup.find(string="Assumed knowledge").find_next("p").string
# print(assumed)
# # prohibitions = soup.find(string="Prohibitions").find_next("p").string
# # print(prohibitions)


# get uos codes
# get html
# parse html
# insert into database



def database_connect():
    # Read the config file

    conn = pg8000.connect(user=None, host='localhost', unix_sock=None, port=5432, database='studreg', password=None, ssl=False, timeout=None)

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(user=None, host='localhost', unix_sock=None, port=5432, database='usyd', password=None, ssl=False, timeout=None)

    except pg8000.OperationalError as e:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(e)

    # return the connection to use
    return connection




def parse_db(uoscode):
    test_data = []

    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT more_info
                            FROM Subjects
                            WHERE unit_code=%s""", (uoscode,))
        test_data = cursor.fetchall()
        cursor.close()

        if test_data is None:
            test_data = []
    except:
        # This happens if there is an error executing the query
        print("This member does not exist or there is a password error.")


    try:
        html = get_html(test_data[0][0])
    except:
        print("HTML unable to be reached for " + uoscode)
        return

    try:
        cursor = connection.cursor()

        cursor.execute("BEGIN TRANSACTION;")

        cursor.execute("""INSERT INTO Html
                            VALUES (%s, %s);
                            """, (uoscode, html))

        cursor.execute("COMMIT;")
        cursor.close()

    except connection.Error as e:
        print('Exception inserting html')
        print(e)

def get_codes():
    codes = []

    try:
        cursor = connection.cursor()
        # cursor.execute("""SELECT unit_code
        #                     FROM Subjects
        #                     WHERE unit_code NOT IN (
        #                         SELECT unit_code FROM Html
        #                     )
        #                     ORDER BY unit_code
        #                     """)
        cursor.execute("""SELECT unit_code
                            FROM Html
                            ORDER BY unit_code
                            """)
        codes = cursor.fetchall()
        cursor.close()

        if codes is None:
            codes = []
    except:
        # This happens if there is an error executing the query
        print("This member does not exist or there is a password error.")

    return codes


def get_html(uoscode):
    html = []

    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT html
                            FROM html
                            WHERE unit_code=%s""", (uoscode,))
        html = cursor.fetchall()
        cursor.close()

        if html is None:
            html = []
    except Exception as e:
        # This happens if there is an error executing the query
        print(e)
        print("Error getting HTML")

    return html


def get_text(tag, type, soup):
    try:
        loc = soup.find(string=tag)
    except Exception as e:
        print(e)

    if loc is None:
        return None

    text = loc.find_next(type).string

    return text



def parse_html(html, soup):

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

# html = 1
#
# results = parse_html(html)




connection = database_connect()

codes = get_codes()
# print(codes)

i = 0
for code in codes:
    print(code[0])
    html = get_html(code[0])
    if html:
        print(html)
        x = 1
    else:
        continue
    soup = BeautifulSoup(html, 'html.parser')

    results = parse_html(html, soup)
    print(code)
    for key in results:
        print(key)
        print(results[key])

    i += 1
    if i > 1:
        break
