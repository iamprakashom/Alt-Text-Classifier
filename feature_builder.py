import os
import csv
from nltk.corpus import wordnet
# import re
colHeader = ['altText', 'nullValue', 'stopWord', 'fileExt', 'fileNamepattern',
             'symbolWord', 'dollarNumber', 'numOnly', 'alphabetic',
             'imgResolution', 'wordNumPercentageWord', 'wordUnderscoreWord',
             'wordDashWord', 'wordandWord', 'alttextinDictionary']
colField = {'altText': 'ALT Text', 'nullValue': 'Null Value', 'stopWord': 'Stop Word',
            'fileExt': 'ALT Text contain File Extension', 'fileNamepattern': 'File Name Pattern',
            'symbolWord': 'SymbolWord', 'dollarNumber': 'Currency',
            'numOnly': 'Numeric Only', 'alphabetic': 'Alphabetic Word', 'imgResolution': 'Image Resolution',
            'wordNumPercentageWord': 'Word Number Percent Word',
            'wordUnderscoreWord': 'Word Underscore Word', 'wordDashWord': 'Word Dash Word',
            'wordandWord': 'Word & Word', 'alttextinDictionary': 'Alt Text in Dictionary'}

global imgExt
imgExt = ('bmp', 'BMP', 'jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF', 'png',
          'PNG')


def checker(altText):
    if (len(altText) == 0):
        csvfileWriter(altText, nullVal=1)
    elif len(altText) <= 2:
        csvfileWriter(altText, stopWord=1)
    elif altText.endswith(tuple(imgExt)):
        csvfileWriter(altText, fileExt=1)
    elif altText.startswith('DSC_'):
        # TODO - Image filename pattern(image1, image2 etc),
        # picture filename pattern(picture1, picture2)
        csvfileWriter(altText, fileNamepattern=1)
    elif len(altText.split()) == 1:
        if wordnet.synsets(altText):
            csvfileWriter(altText, textinDictionary=1)
        else:
            csvfileWriter(altText)
    else:
        csvfileWriter(altText)


def csvfileWriter(alt, nullVal=0, stopWord=0, fileExt=0, fileNamepattern=0,
                  symbolWord=0, dollarNum=0, numOnly=0, alphabet=0,
                  imgResolution=0, wordNumPercentWord=0,
                  wordUnderscoreWord=0, wordDashWord=0, wordandWord=0,
                  textinDictionary=0):
    fileName = "featurevector" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'w'

    with open(fileName, fileMode) as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames=colHeader)
        if fileMode == 'w':  # Writing Column Header
            csvWriter.writerow(colField)

        # writing each row with data
        csvWriter.writerow({'altText': alt, 'nullValue': nullVal,
                            'stopWord': stopWord, 'fileExt': fileExt,
                            'fileNamepattern': fileNamepattern, 'symbolWord': symbolWord,
                            'dollarNumber': dollarNum, 'numOnly': numOnly,
                            'alphabetic': alphabet, 'imgResolution': imgResolution,
                            'wordNumPercentageWord': wordNumPercentWord,
                            'wordUnderscoreWord': wordUnderscoreWord,
                            'wordDashWord': wordDashWord, 'wordandWord': wordandWord,
                            'alttextinDictionary': textinDictionary})
    return

fobj = open('Dataset.csv', 'r')
reader = csv.DictReader(fobj)

for row in reader:
    print(row['ALT Text'])
    checker(row['ALT Text'])
fobj.close()
