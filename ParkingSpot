# Parking spot winner randomizer
from random import shuffle
import csv
import os

employeedict = {}

pastwinners = []

def parkingspot():
    count = 0


    with open("OOTEmployees.csv", 'r') as f:
        for line in f:
            items = line.split(',')
            count += 1

            lastname, firstname = items[0], items[1:]
            employeedict[count] = lastname , firstname

        print("There are {0} current Denton campus OOT employees".format(count))




        number = list(range(1,count))
        shuffle(number)

        draw = number [1]

        print ("[{0}]".format(draw))
        with open("pastwinners.txt","r") as f:
                if "[{0}]".format(draw) in f.read():
                    print("This person has perviously won the parking spot, redrawing...")
                    shuffle(number)
                    draw = number [1]

    pastwinners.append(draw)

    with open("pastwinners.txt","a") as f:
        f.write('%s' % pastwinners)


    print("The winning number is lucky number....{0}!!!".format(draw))
    print("That corresponds to {0}! Congratulations!".format(employeedict[draw]))
    print (pastwinners)
    return

exists = os.path.isfile('pastwinners.txt')
if (exists == True): parkingspot()
else: open("pastwinners.txt","w") , parkingspot()
