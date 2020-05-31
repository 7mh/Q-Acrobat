#! /usr/bin/env python3
import re

db = {}

def filldb(fileName, db):
    l = []
    count  =0
    t = []

    with open(fileName, 'r') as fd:
        l = map(str, fd.readlines())
    for i in l:
        count  += 1
        #t.append(i.rstrip())
        a = re.match(r'\(\((\d),(\d),(\d),(\d)\),(-?\d)\)=(.*)',i.rstrip())
        if a:
#            print(a.group(1), a.group(2),a.group(3),a.group(4),a.group(5),a.group(6), )
            db[((int(a.group(1)),int(a.group(2)),int(a.group(3)),int(a.group(4))), int(a.group(5)))] = float(a.group(6))
        else:
            print("No match at regexp")
#        if count == 100:
#            break


if __name__ == '__main__':
    filldb('acrobot.txt',db)


