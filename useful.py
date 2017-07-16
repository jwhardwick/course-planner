def database_connect():
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

connection = database_connect()


user_data = []

try:

    cursor = connection.cursor()
    cursor.execute("""SELECT member_id, title, family_name, given_names, country_code, accommodation
                        FROM member_view
                        WHERE member_id=%s AND pass_word=%s""", (member_id, password))
    user_data = cursor.fetchall()
    cursor.close()

    if user_data is None:
        user_data = []
except:
    # This happens if there is an error executing the query
    print("This member does not exist or there is a password error.")



import httplib2

def get_page(link):
	http = httplib2.Http()
	status, response = http.request(link)
	return response
