import os
import sys
import re
import pickle

# Person class that contains the value of the first name, middle inital, last name, id, and phone number
class Person:
    # last, first, mi, id, and phone
    # init method to store parameter in the person class
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # Display method, displaying
    # Employee id: (ID)
    #       (First) (MI) (Last Name
    #       (Phone)
    def display(self):
        print('Employee id: {0}\n\t\t{1} {2} {3}\n\t\t{4}\n'.format(self.id, self.first, self.mi, self.last, self.phone))

# Method to open csv file, process the data within, and store data in a dict
def openFile(filepath):
    myDict = {}

    # Opens according to filepath and type of os
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        count = 0
        for line in f.readlines():
            # If statement to skip header
            if count != 0:
                # Split line into list sepreated by , and processes text
                tokens = line.split(',')
                tokens[4] = tokens[4].replace('\n', '')
                tokens[0] = tokens[0].capitalize()
                tokens[1] = tokens[1].capitalize()
                if tokens[2] == '':
                    tokens[2] = 'X'
                else:
                    tokens[2] = tokens[2][0].upper()
                # Regrex to check ID
                x = re.findall("[a-zA-Z]{2}\d{4}",tokens[3])
                if len(x) == 0:
                    print("ID invalid: {0}\nID is two letters followed by 4 digits".format(tokens[3]))
                    string = ""
                    # Loop till user input correct ID
                    while (len(x) == 0):
                        string = input("Please enter a valid id: ")
                        x = re.findall("[a-zA-Z]{2}\d{4}", string)
                    tokens[3] = string
                # Regrex to check Phone Number
                y = re.findall("\d{2}-\d{2}-\d{2}", tokens[4])
                if len(y) == 0:
                    print("Phone {0} is invalid\nEnter phone number in form 123-456-7890".format(tokens[4]))
                    string = ""
                    # Loop till user input correct Phone Number
                    while (len(y) == 0):
                        string = input("Enter phone number: ")
                        y = re.findall("\d{3}-\d{3}-\d{4}", string)
                    tokens[4] = string
                # Creates Person Object
                tempPerson = Person(tokens[1], tokens[0], tokens[2], tokens[3], tokens[4])
                # Check for Duplicate and if Duplicate, omit data
                if not (tokens[3] in myDict):
                    myDict[tokens[3]] = tempPerson
                else:
                    print("Error: Duplicate ID detected, Person not taken")
            count += 1
        # Close file for data corrput protection
        f.close()
    return myDict




def main():
    if len(sys.argv) < 2:
        print("No arguments in command, quiting program...")
    else:
        fp = sys.argv [1]
        myDict = openFile(fp)
        # Stores myDict into pickle
        pickle.dump(myDict, open('dict.p', 'wb'))

        # Open pickle and store into dict_in
        dict_in = pickle.load(open('dict.p', 'rb'))
        print("\n\nEmployee List:\n")

        # Loop and display all Person in Dict
        for key in dict_in:
            dict_in[key].display()

main()