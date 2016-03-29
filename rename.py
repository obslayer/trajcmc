import os
for fullFilename in os.listdir('.'):
    ext = fullFilename.split('.')
    if ext[1] == 'png':
        filename = ext[0]
        while len(filename) < 3:
            filename = '0' + filename
            print filename
        os.rename(fullFilename, filename + '.png')
