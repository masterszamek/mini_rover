import csv

f = open('gamepad_keys.csv', "r")

with f:
    reader = csv.reader(f, delimiter=" ")
    #print(list(reader))
    for row in list(reader)[1:]:
        print(row[0], row[1], row[2])
    f.close()
