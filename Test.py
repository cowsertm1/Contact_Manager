# Is this working?
output_file = open("contacts.dat", "w")
print("Enter a few strings to write to the file, and type quit when finished.")
done = False
while not done:
    st = input("> ")
    if st == "quit":
        done = True
    else:
        output_file.write("{0}\n".format(st))
output_file.close()
print("All done!")

crm_dict= {

}

valid_keys = []
for key in contacts_obj[0].keys():
    valid_keys.append(key)
key_choice = ""
while key_choice != "quit":
    print("Available searches: {0}".format(valid_keys))
    key_choice = input("Enter the type of search you would like to perform, or type quit: ")
    if key_choice in valid_keys:
        value_choice = input("Enter the value you would like to search for: ")
        for contact in contacts_obj:
            if str(contact[key_choice]).lower() == value_choice.lower():
                print("{0} {1} ({2}): {3}".format(
                contact["first_name"], contact["last_name"],
                contact["town"], contact["phone"]))


contacts_obj = [
    {"first_name": "Alexander",
     "last_name": "Coder",
     "phone": 5551763,
     "town": "Kingston"},
    {"first_name": "Michael"},
    {"first_name": "Elaine",
     "last_name": "Benes"},
    {"first_name": "Tobias",
     "town": "Newport Beach"},
]

valid_keys = []
for key in contacts_obj[0].keys():
    valid_keys.append(key)
key_choice = ""
while key_choice != "quit":
    print("Available searches: {0}".format(valid_keys))
    key_choice = input("Enter the type of search you would like to perform, or type quit: ")
    if key_choice in valid_keys:
        value_choice = input("Enter the value you would like to search for: ")
        for contact in contacts_obj:
            if str(contact.get(key_choice)).lower() == value_choice.lower():
            print("{0} {1} ({2}): {3}".format(
                contact.get("first_name"), contact.get("last_name"),
                contact.get("town"), contact.get("phone")))


input_file = open("contacts.dat", "r")
lines = input_file.readlines()
input_file.close()
print("The entire contacts.dat file:")
print(lines)
print("The contacts.dat file, line-by-line:")
for x in lines:
    print(x)
print("All done!")

input_file = open("pg35.txt", "r")
words = []
for line in input_file:
    new_string = ""
    for x in line:
        if x.isalpha() or x == " ":
            new_string = "{0}{1}".format(new_string, x.lower())
        else:
            new_string = "{0} ".format(new_string)
    while new_string.find(" ") >= 0:
        new_string = new_string.replace(" ", " ")
    new_string = new_string.strip()
    if len(new_string) > 0:
        for word in new_string.split(" "):
            words.append(word)
words.sort()
print("There are {0} words in the file.".format(len(words)))
print("Some of the words in your file are:")
print(words[:10])
print(words[10000:10010])

input_string = input("Enter a string: ")
new_string = ""
for x in input_string:
    if x.isalpha() or x == " ":
        new_string = "{0}{1}".format(new_string, x.lower())
while new_string.find(" ") >= 0:
    new_string = new_string.replace(" ", " ")
new_string = new_string.strip()
words = new_string.split(" ")
words.sort()
print("The words in your string are:")
print(words)

##Need to update this code to do what I need it to do

phone_contacts = {}


def print_contacts():
    if not phone_contacts:
        print("No Contacts within directory")
        return

    for name, number, email in sorted(phone_contacts.items()):
        print(name, number, email)  # explicit is better than implicit


def add_contact():
    name = input("Enter a name\n")
    number = input("Enter a number\n")
    email = input("Enter an email\n")

    if name and number and email:
        phone_contacts[name] = number
        print("Contact added: {0}, {1}, {2}".format(name, number, email))


def remove_contacts():
    print_contacts()
    removing_contact = input("Enter a contact to remove\n")
    if removing_contact in phone_contacts:
        del phone_contacts[removing_contact]
        print("Contact has been deleted!")
    else:
        print("There is no '%s' contact!") % (removing_contact)


def load_contacts():
    global phone_contacts
    try:
        with open('contacts.dat', 'r') as file:
            phone_contacts = file.read()
    except (ValueError, OSError):  # OSError catches FileNotFoundError
        phone_contacts = {}


def save_contacts():
    with open('contacts.dat', 'w+') as file:
        (phone_contacts, file)


load_contacts()
while True:
    print("0. Exit")
    print("1. Menu")
    print("2. Add contact")
    print("3. Remove contacts")

    choose = input("Select option: ")

    if choose == "0":
        print("Exiting program...")
        break
    elif choose == "1":
        print_contacts()
    elif choose == "2":
        add_contact()
    elif choose == "3":
        remove_contacts()
    else:
        print("You didn't type a valid option!")

    # moved this block out as it's common to all options
    choose_2 = input("End/Back to MENU\n").lower()
    if choose_2 == "end":
        break
    # even if user typed anything different of menu
    # he/she would continue in the loop so that else was needless
save_contacts()


import pickle
import sqlite3
from collections import namedtuple

# Simple class representing a record in our database.
MemoRecord = namedtuple("MemoRecord", "key, task")

class DBPickler(pickle.Pickler):

    def persistent_id(self, obj):
        # Instead of pickling MemoRecord as a regular class instance, we emit a
        # persistent ID.
        if isinstance(obj, MemoRecord):
            # Here, our persistent ID is simply a tuple, containing a tag and a
            # key, which refers to a specific record in the database.
            return ("MemoRecord", obj.key)
        else:
            # If obj does not have a persistent ID, return None. This means obj
            # needs to be pickled as usual.
            return None


class DBUnpickler(pickle.Unpickler):

    def __init__(self, file, connection):
        super().__init__(file)
        self.connection = connection

    def persistent_load(self, pid):
        # This method is invoked whenever a persistent ID is encountered.
        # Here, pid is the tuple returned by DBPickler.
        cursor = self.connection.cursor()
        type_tag, key_id = pid
        if type_tag == "MemoRecord":
            # Fetch the referenced record from the database and return it.
            cursor.execute("SELECT * FROM memos WHERE key=?", (str(key_id),))
            key, task = cursor.fetchone()
            return MemoRecord(key, task)
        else:
            # Always raises an error if you cannot return the correct object.
            # Otherwise, the unpickler will think None is the object referenced
            # by the persistent ID.
            raise pickle.UnpicklingError("unsupported persistent object")


def main():
    import io
    import pprint

    # Initialize and populate our database.
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE memos(key INTEGER PRIMARY KEY, task TEXT)")
    tasks = (
        'give food to fish',
        'prepare group meeting',
        'fight with a zebra',
        )
    for task in tasks:
        cursor.execute("INSERT INTO memos VALUES(NULL, ?)", (task,))

    # Fetch the records to be pickled.
    cursor.execute("SELECT * FROM memos")
    memos = [MemoRecord(key, task) for key, task in cursor]
    # Save the records using our custom DBPickler.
    file = io.BytesIO()
    DBPickler(file).dump(memos)

    print("Pickled records:")
    pprint.pprint(memos)

    # Update a record, just for good measure.
    cursor.execute("UPDATE memos SET task='learn italian' WHERE key=1")

    # Load the records from the pickle data stream.
    file.seek(0)
    memos = DBUnpickler(file, conn).load()

    print("Unpickled records:")
    pprint.pprint(memos)


if __name__ == '__main__':
    main()

    ################################################################################
    # File Name:	ContactManager.py
    # Author:		Debbie Heisler
    # Date:			April 4, 2014
    # Description:
    #	This is the contact manager main driver function/file.
    ###############################################################################
    """ Contact Manager main driver functions/files """

    from Person import Person
    from List import List
    import Menus

    quit = False  # global variable to make getting out of here easier
    contactList = List()


    def readInContacts():
        """ Read in the default contact list file """
        file = open('contacts.txt', 'r')
        for line in file:
            fields = line.split(',')
            peep = Person(fields[0].strip(), fields[1].strip(), fields[2].strip())
            contactList.addPerson(peep)


    def printContactsToFile():
        """ Print the contacts to a file.  Will loop until get a good file name """
        while True:
            print("File Name")
            fn = input()
            try:
                file = open(fn, 'w')
                contactList.printToFile(file)
                print("Contacts written to " + fn)
                break
            except IOError:
                continue


    def addNewContact():
        """ Adds a new contact to the contact manager. Does no error checking """
        global contactList
        print("First Name:", )
        fn = input()
        print("Last Name:", )
        ln = input()
        print("Email:", )
        email = input()
        peep = Person(fn, ln, email)
        contactList.addPerson(peep)


    def handleFoundPerson(person, option):
        """ Error checks person.  Prints it or an error """
        if person is None:
            print("No one matches that criteria")
        elif option == "search":
            person.printToScreen()
        elif option == "delete":
            contactList.deletePerson(person)


    def checkSearchInput(selected, option):
        """ Handles the input for searching. """
        if selected == 0:
            Menus.printSearchCriteria("First Name")
            searchStr = input()
            peep = contactList.matchPersonByFirstName(searchStr)
            handleFoundPerson(peep, option)
        elif selected == 1:
            Menus.printSearchCriteria("Last Name")
            searchStr = input()
            peep = contactList.matchPersonByLastName(searchStr)
            handleFoundPerson(peep, option)
        elif selected == 2:
            Menus.printSearchCriteria("Email")
            searchStr = input()
            peep = contactList.matchPersonByEmail(searchStr)
            handleFoundPerson(peep, option)
        else:
            print("That is not a valid selection")


    def searchForPerson(option):
        """ Handles the option to search for a person to print or delete """
        Menus.printSearchMenu()
        while True:
            try:
                selection = int(input())
                checkSearchInput(selection, option)
                break
            except ValueError:
                print("Numbers only.  Try again")
                continue


    def checkInput(selected):
        """ Checks the input to make sure it is a valid main menu option """
        global quit
        if selected == 1:
            contactList.printToScreen()
        elif selected == 2:
            searchForPerson("search")
        elif selected == 3:
            addNewContact()
        elif selected == 4:
            searchForPerson("delete")
        elif selected == 5:
            printContactsToFile()
        elif selected == 6:
            quit = True
        else:
            Menus.printInvalidOption(selected)


    #####################
    # The Main function
    ####################

    if __name__ == "__main__":
        readInContacts()

        while (quit == False):
            Menus.printMainMenu()
            try:
                selection = int(input())
                checkInput(selection)
            except ValueError:
                continue