import os
import json
from modules.boxify import boxify

def gatherfile(gathercup, extension, filepath = None):
    if filepath == None:
        filepath = '.'
    filepath = f'{filepath}\\'
    listofdir = os.listdir(filepath)

    for dir in listofdir:
        if os.path.isdir(filepath+dir):
            gatherfile(gathercup, extension, filepath=filepath+dir)
        else:
            if dir[-len(extension):] == extension:
                gathercup.append(filepath+dir)

def countlines(extension):
    gathercup = []
    gatherfile(gathercup, extension)

    record = {}
    for gathering in gathercup:
        with open(gathering, "r") as f:
            record[gathering] = len(f.readlines())

    return record

def main():
    while True:
        line = input('> ')

        if "end" in line:
            break

        elif "gather" in line:
            gathercup = []
            extension = input('Enter extension to gather : ')
            gatherfile(gathercup, extension)
            print(boxify(json.dumps(gathercup, indent=3)))

        elif "count" in line or "line" in line:
            extension = input("Enter extension : ")
            record = countlines(extension)
            string = boxify(json.dumps(record, indent=3))
            linesize = len(string.split('\n')[0])
            print(string)
            total = sum(record[num] for num in record)
            print(boxify(f"Total : {total}", width=linesize))

        else:
            pass

if __name__ == '__main__':
    main()