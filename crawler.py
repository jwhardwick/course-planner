#!/usr/bin/env python3

from modules import *
from modules import pg8000
import configparser
import urllib.request


def database_connect_config_parser():
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']


    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as e:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(e)

    # return the connection to use
    return connection

def database_connect():

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

def get_html(link):


    fp = urllib.request.urlopen(link)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    return mystr


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


    # PARSE HTML HERE!


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
        cursor.execute("""SELECT unit_code
                            FROM Subjects
                            WHERE unit_code NOT IN (
                                SELECT unit_code FROM Html
                            )
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



connection = database_connect()

codes = get_codes()

for code in codes:
    parse_db(code[0])
