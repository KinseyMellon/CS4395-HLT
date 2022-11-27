import pickle
import sys
import os
import re

# person class to hold the employee info
class Person:

    # definition class that creates variables to hold the name, id, and phone number
    def __init__(self, ln, fn, m, i, p):
        self.last = ln
        self.first = fn
        self.mi = m
        self.id = i
        self.phone = p

    # display function that prints out all the info in the person object
    def display(self):
        print("Employee id: ", self.id)
        print('\t',self.first, self.mi, self.last)
        print('\t',self.phone,end='\n')


# function to read in the file and process the info and add it to a person object
def process_text(text):
    # read in the lines
    lines = text.readlines()

    # delete the header line
    del lines[0]

    # create a dict to hold the people
    people = {}

    # loop through each line and process the info
    for line in lines:
        # split the data by the commas
        p1 = line.split(',')

        # get first and last name and capitalize them
        fn = p1[1].capitalize()
        ln = p1[0].capitalize()

        # get middle initial
        if p1[2]:
            mi = p1[2].upper()
        else:
            mi = 'X'

        # get id number
        i_input = re.match('[^0-9][^0-9][0-9][0-9][0-9][0-9]', p1[3])
        if i_input:
            i = p1[3]
        else:
            print("invalid id: ", p1[3])
            i = input("Please enter correct id with 2 letters followed by 4 digits: ")
            print()

        # get phone number
        p1[4] = p1[4].rstrip('\n')

        p_input = re.match('[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]',p1[4])
        if p_input:
            p = p1[4]
        else:
            print("invalid phone number: ", p1[4])
            p = input("Please enter correct phone number in format 123-456-7890: ")
            print()

        # check if ID is already in use; if not create person object and add it to the dictionary
        if i not in people.keys():
            person = Person(ln,fn,mi,i,p)
            people[i] = person
        else:
            print("Duplicate id ", i)

    # return the dictionary of all the people from the file
    return people


def main():

    # check if the sysarg has a file path
    if len(sys.argv) > 1:
        # it does so read it
        arg_input = sys.argv[1]

        # open the file
        with open(os.path.join(os.getcwd(), arg_input), 'r') as f:
            people = process_text(f)

        # save the returned dictionary of people as a pickle then open it
        pickle.dump(people, open('dict.p','wb'))
        dict_in = pickle.load(open('dict.p','rb'))

        # print the employee list
        print("Employee List:")
        for p in dict_in.values():
            p.display()
    else:
        # error message if there was no file entered
        print("error, no file path entered")


if __name__ == "__main__":
    main()
