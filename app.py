#!/usr/bin/python3

import random, string, csv, os
from datetime import datetime, time
import pandas as pd

inFileName = 'generated'
outFileName = 'output'

def dataFrame(final):

    dataFrame = pd.DataFrame(final)

    pd.set_option('display.max_rows', dataFrame.shape[0] + 1)

    print(dataFrame)

def secondFileWrite(final):

    with open('%s.csv' % outFileName, 'w', encoding= "latin-1", newline = '\n') as file:

        fieldnames = [  
        'input', 
        'output',
        ]

        my_File = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',', dialect='excel')

        my_File.writeheader()
        my_File.writerows(final)

    dataFrame(final)

def find_all(a_str, sub):

    start = 0

    while True:

        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def readFile():

    final = []

    if os.path.exists('./%s.csv' % inFileName):

        with open('%s.csv' % inFileName, 'r', encoding= "latin-1", newline = '\n') as file:

            fieldnames = [  
            'input', 
            'output',
            ]

            my_File = csv.DictReader(file, fieldnames=fieldnames, delimiter=',', dialect='excel')

            [final.append(x) for x in my_File]

    del final[0]

    for row in final:

        status = False

        opening = list(find_all(row['input'], '('))
        closer = list(find_all(row['input'], ')'))

        if len(opening) == len(closer):

            if len(opening) == 0 and len(closer) == 0:

                status = True

            else:

                if closer[0] < opening[0] or closer[-1] < opening[-1]:

                    status = False

                else:

                    for _ in range(len(closer)):

                        if opening[_] < closer[_]:

                            status = True

                        else:

                            status = False
                            break

        else:

            status = False

        row['output'] = 'correct' if status == True else 'incorrect'

    secondFileWrite(final)

def firstWriteFile(finalList):

    with open('%s.csv' % inFileName, 'w', encoding= "latin-1", newline = '\n') as file:

        fieldnames = [  
        'input', 
        'output',
        ]

        my_File = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',', dialect='excel')
        my_File.writeheader()
        my_File.writerows(finalList)

    readFile()

def main():

    finalList = []

    rangeLetters = list(string.ascii_letters[0:3])
    rangeNums = list(string.digits[0:3])

    operators = [
    '+',
    '-',
    '/',
    '*',
    ]

    parentheses = [
    "(",
    ")",
    ]

    for _ in range(random.randint(1,1000)):

        expression = ''

        expression = ''.join(random.choice([
        random.choice(operators),
        random.choice(rangeNums),
        random.choice(rangeLetters),
        random.choice(parentheses)]
        ) for i in range(random.randint(1, 1000)))

        finalList.append({"input": expression, "output": ''})

    if finalList != None:

        firstWriteFile(finalList)

if __name__ == '__main__':

    startedScipt = datetime.now()

    main()

    endScript = datetime.now()

    print("\nInício: %s Fim: %s Duração: %s" % (
    startedScipt.strftime('%H:%M:%S'), 
    endScript.strftime('%H:%M:%S'),
    endScript - startedScipt
    )
    )
