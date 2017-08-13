'''
Get codes

Get link for that code

Get HTML for code

Parse HTML

Insert into Parsed
'''
from modules import pg8000

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

def get_all():
    codes = []
    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM Subjects
                            ORDER BY unit_code;""")
        codes = cursor.fetchall()
        cursor.close()
    except pg8000.OperationalError as e:
        print(e)
    return codes


def update_data(thing):
    client = MongoClient('localhost', 27017)
    db = client.test_data

    subjects = db.subjects


    db.subjects.update_one({"code": thing[5]}, {'$set' :
                                              {"faculty"        : thing[0] ,
                                              "area_of_study"  : thing[1] ,
                                              "area_code"      : thing[2] ,
                                              "grad_level"     : thing[3] ,
                                              "offered"        : thing[4] ,
                                              "unit_name"      : thing[6] ,
                                              "link"           : thing[7] ,
                                              }
                                              })


connection = database_connect()
things = get_all()
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




for thing in things:

    # print(thing[0], thing[1], thing[2], thing[3], thing[4], thing[6], thing[7])

    update_data(thing)
    # break
