import os
from pathlib import Path


# Helper functions to test if a user input is valid
def isnumber(test_string):
    try:
        float(test_string)
        return True
    except ValueError:
        return False


def islat(test_string):
    if isnumber(test_string):
        lat = float(test_string)
        if -90 <= lat <= 90:
            return True
        else:
            return False
    else:
        return False


def islon(test_string):
    if isnumber(test_string):
        lon = float(test_string)
        if -180 <= lon <= 180:
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    # Print Current Working Directory
    print(f'{Path.cwd()}: Current Working Directory')

    # Create new directory
    newdir = os.path.join(str(Path.cwd()), 'locations')
    try:
        os.mkdir(newdir)
        print(f'{newdir}: created')
    except FileExistsError:
        print(f'{newdir}: already exists')

    # Change cwd to new directory
    os.chdir(newdir)
    print(f'{Path.cwd()}: Current Working Directory')
    # Print out the names of all the files in new directory
    print('The Following Files are in this Directory:')
    for i in os.listdir(str(Path.cwd())):
        print(i)

    # Get Someones Name
    name = ''
    while len(name.strip()) < 1:
        name = input('Who are you adding a location for?:')

    # Create (or open) a file with user-input name
    with open(name.lower() + '.txt', 'a') as file:
        lat = ''
        lon = ''
        while not islat(lat):
            lat = input(f'Enter {name}\'s latitude :')
        while not islon(lon):
            lon = input(f'Enter {name}\'s longitude:')
        file.write(lat + ',' + lon + '\n')
