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


from bs4 import BeautifulSoup

uos = open('2129.html')

soup = BeautifulSoup(uos, 'html.parser')

# prereq = soup.find(string="Prerequisites").find_next("p").string
# print(prereq)
# assumed = soup.find(string="Assumed knowledge").find_next("p").string
# print(assumed)
# # prohibitions = soup.find(string="Prohibitions").find_next("p").string
# # print(prohibitions)





def get_text(tag, type):
    try:
        loc = soup.find(string=tag)
    except Exception as e:
        print(e)

    if loc is None:
        return None

    text = loc.find_next(type).string

    return text

def get_p(tag):
    try:
        loc = soup.find(string=tag)
    except Exception as e:
        print(e)

    if loc is None:
        return None

    text = loc.find_next("p").string

    return text

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

for tag in tags_p:
    print(get_text(tag, 'p'))

for tag in tags_span:
    print(get_text(tag, 'span'))
