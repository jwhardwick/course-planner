
import re

def remove_punctuation(token):

    punctuation = [',', '.', '"', '-', '+', '!', ';', ':', '\\', '&', '/', "'"]

    cleaned = []
    for char in token:
        if char not in punctuation:
            cleaned.append(char)
    print(cleaned)

def test_remove_punctuation():

    remove_punctuation('COMP2129.')
    remove_punctuation('CO,MP.2129.')

def is_valid(code):
    uos = re.compile('[a-z]{4}[0-9]{4}', re.IGNORECASE)

    match = uos.match(code)

    if match:
        return True
    elif match is None:
        return False

def create_link(code):
    return '<a href="http://sydney.edu.au/courses/uos/' + code +'">' + code + '</a>'


def convert_line(line):
    # split
    tokens = line.split(' ')

    for token in tokens:
        if is_valid(token):
            # print("valid token")
            token = create_link(token)
            # print(token)

    # print(tokens)


# Punctuation


line_test = ['INFO1103 or INFO1903.',
            'INFO1105 OR INFO1905.']

for line in line_test:
    convert_line(line)



valid_codes = ["COMP2129",
               "INFO2820",
               "math1001",
               "abcd1234"]

non_valid_codes = ["ABC12345",
                   "CHEM123",
                   "A1B2C3D4",
                   "2129COMP",
                   "SUBJECTS",
                   "12345678"]

# http://sydney.edu.au/courses/uos/ACCT1006

for code in valid_codes:
    assert(is_valid(code) == True)
    # print(create_link(code))

for code in non_valid_codes:
    assert(is_valid(code) == False)

test_remove_punctuation()
