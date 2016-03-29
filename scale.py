import os, sys

inputPath = "/home/wang/workplace/zyed/data/"

files = os.listdir(inputPath)

xMin = sys.maxint
yMin = sys.maxint
xMax = 1
yMax = 1
for filename in files:
    with open(inputPath + filename) as f:
        for lines in f:
            terms = lines.split(',')
            x = float(terms[0])
            y = float(terms[1])
            if x > xMax:
                xMax = x
            if y > yMax:
                yMax = y
            if x != 0.0 and x < xMin:
                xMin = x
            if x != 0.0 and y < yMin:
                yMin = y

print "xMin:", xMin, "yMin:", yMin, "xMax:", xMax, "yMax:", yMax
