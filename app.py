import mysql.connector
from difflib import get_close_matches

con = mysql.connector.connect(
    user = "ardit700_student",
    password = "ardit700_student",
    host = "108.167.140.122",
    database = "ardit700_pm1database"
)

def read_data(word):
    cursor = con.cursor()

    query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word.lower())
    data = cursor.fetchall()

    if data:            # small letters search
        for item in data:
            return data

    query = cursor.execute("SELECT Expression FROM Dictionary")
    close = [b[0] for b in cursor.fetchall()]

    if len(get_close_matches(word, close)) > 0:                     #   close match check/suggestion
        confirm = input("Did you mean %s instead? (Y / N)" % get_close_matches(word, close)[0])
        if confirm.lower() == 'y':
            query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % get_close_matches(word, close)[0])
            data = cursor.fetchall()
            return data
        elif confirm.lower() == 'n':
            return "That word does not exist in the dictionary, please enter another word."
        else:
            return "Command not recognized."

    query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word.title())
    data = cursor.fetchall()

    if data:            # Capital letter search
        for item in data:
            return data

    query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression = '%s'" % word.upper())
    data = cursor.fetchall()

    if data:            # Upper case search
        for item in data:
            return data

    else:
        return "That word does not exist in the dictionary, please enter another word."

while True:
    print("""
    1) Search for a word definition
    2) Quit
    """)
    choice = input("Enter option: ")
    if choice == '1':
        word = input("Search for a word: ")
        output = read_data(word)  # if word has many definitions the output is a list of tuples
        if type(output) == str:
            print(output)
        else:
            for line in output:  # want to get all the lines/definitions
                print("-" + ''.join(line))  # print user-friendly
    elif choice == '2':                 #   quit program
        break