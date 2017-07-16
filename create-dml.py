
import csv


def escape_apostrophes(field):
  # replace occurrences of ' with ''
  return str.replace(field, "'", "''")

def csv_to_array():
    array = []
    with open("gdrive.csv", 'r', encoding='utf8') as file:
    # skip header field
        for _ in range(1):
            next(file)
        file = csv.reader(file, delimiter=',', quotechar='|')
        for row in file:
            if row: # skip blank lines
                print(row)
                array.append(row)
    return array

def prepare_statement(line):
    statement = ("INSERT INTO Subjects VALUES (")
    for i in range(0, len(line)):
        line[i] = escape_apostrophes(line[i])
        if line[i] == 'NULL':
            entry = ( "%s" % line[i] )
        else:
            entry = ( "'%s'" % line[i] )
        statement += entry
        if i != len(line) - 1:
            statement += ", "
    statement += ");\n"
    return statement

def write_to_file(statement):
    print(state)

file_insert = open('dml.sql', 'w')

array = csv_to_array()

for line in array:
    statement = prepare_statement(line)
    file_insert.write(statement)
