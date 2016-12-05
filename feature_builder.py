import os
import csv
from nltk.corpus import wordnet
import re
colHeader = ['nullValue', 'stopWord', 'fileExt', 'fileExt_jpg',
             'fileExt_gif', 'fileExt_png',
             'fileNamepattern', 'Has_image_num', 'Has_img_num',
             'numOnly', 'symbolOnly', 'symbolWord', 'words',
             'imgResolution', 'wordNumPercentageWord', 'wordUnderscoreWord',
             'wordDashWord', 'wordandWord', 'wordSymbolword', 'alttextinDictionary']
colField = {'nullValue': 'Null Value', 'stopWord': 'Stop Word',
            'fileExt': 'ALT Text has File Extension', 'fileExt_jpg': 'Has fileExt JPG', 'fileExt_gif': 'Has fileExt GIF',
            'fileExt_png': 'Has fileExt PNG', 'fileNamepattern': 'File Name Pattern',
            'Has_image_num': 'Has_image_Num', 'Has_img_num': 'Has_img_num',
            'numOnly': 'Numeric Only', 'symbolOnly': 'Special Symbol Only', 'symbolWord': 'SymbolWord',
            'words': 'Alphabetic Words', 'imgResolution': 'Image Resolution',
            'wordNumPercentageWord': 'Word Number Percent Word',
            'wordUnderscoreWord': 'Word Underscore Word', 'wordDashWord': 'Word Dash Word',
            'wordandWord': 'Word & Word', 'wordSymbolword': 'Word Symbol(.({})) Word', 'alttextinDictionary': 'Alt Text in Dictionary'}

imgExt = ['bmp', 'BMP', 'jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF', 'png',
          'PNG', 'PDF', 'pdf']
fnamePattern_list = ['dsc', 'DSC', 'img', 'IMG', 'Img', 'image', 'Image', 'IMAGE',
                     'alt', 'Alt']

# img(\s|\(|\{|\_|\-|\/)?\d+|
# image(\s)?(\s|\(|\{|\_|\-|\/)?\d+(\s|\}|\|\])?|


def main():
    fnamePattern_expression = re.compile('''
        (image|img)(\s)?(\#|\(|\{|\[|\_|\-|\/)?(\d+)?(\s)?(\}|\)|\])?|
        pic(\s|\(|\{|\_|\-|\/)?\d+|
        banner(\s)?(image)?(\#|\(|\{|\[|\_|\-|\/)?(\d+)?(\s)?(\}|\)|\])?|
        (slider|slide)(\s)?(\#|\$|\@|\%)?(\d+)?
        ''', re.X | re.I)

    has_image_num = re.compile(
        '^image(\s)?\d+|^image(\s)?(\(|\{|\_|\-)+\d+', re.I)
    # has_image_sym_num = re.compile('^image(\s)?(\(|\{|\_|\-)+\d+', re.I)
    has_img_num = re.compile('^img(\s)?\d+|^img(\s|\(|\{|\_|\-|\/)?\d+', re.I)
    # has_img_sym_num = re.compile('^img(\s|\(|\{|\_|\-|\/)?\d+', re.I)
    symbolOnlypattern = re.compile('[#$%?@]+')
    numOnlypattern = re.compile('^\d+(.)?\d+$')
    symbolWord = re.compile('(\/|\(|\{|\[|\,|\-|\:|\.|\#|\@)(\s)?[a-zA-Z]+')
    # symbolWord = re.compile('^(\[|\#|\$|\%|\?|\@|\])?(\s)?')
    wordpattern = re.compile('([a-zA-Z]+(\s)?[a-zA-Z]+)')
    wordNumPercentageWordpattern = re.compile(
        '[a-zA-Z]+(\s)?\d+\%(\s)?[a-zA-Z]+')
    # wordandWordpattern = re.compile('[a-zA-Z]+(\s)?\&(\s)?[a-zA-z]+')
    wordandWordpattern = re.compile('[a-zA-Z]+(\s)?\&(\s)?[a-zA-z]+(\s)?\w+')
    wordDashWordpattern = re.compile('[a-zA-Z]+(\s)?\-(\s)?[a-zA-z]+')
    wordUnderscoreWordpattern = re.compile('[a-zA-Z]+(\s)?\_(\s)?[a-zA-z]+')
    wordSymbolwordpattern = re.compile(
        '([a-zA-Z]+(\s)?(\/|\(|\{|\[|\,|\-|\:|\.)(\s)?([a-zA-Z]|\d+)+(\/|\)|\}|\]|\,|\-|\:|\.)?(\s)?)')
    imgResolutionpattern = re.compile('\d+')

    def imgResolutioncheck(height, width):
        if(int(height) >= 75) and (int(width) >= 75):
            return True
        else:
            return False

    def filepatternFinder(altText, imgReso_value, fileextension=None):
        if fileextension == 'JPG':
            if has_image_num.search(altText):
                return csvfileWriter(fileExt=1,
                                     fileExt_jpg=1, fileNamepattern=1, has_image_num=1, imgResolution=imgReso_value)
            elif altText.lower().startswith('dsc'):
                return csvfileWriter(fileExt=1, fileExt_jpg=1, fileNamepattern=1,
                                     imgResolution=imgReso_value)
            elif has_img_num.search(altText):
                return csvfileWriter(fileExt=1, fileExt_jpg=1, fileNamepattern=1,
                                     has_img_num=1, imgResolution=imgReso_value)
            else:
                return csvfileWriter(fileExt=1, fileExt_jpg=1, imgResolution=imgReso_value)
        elif fileextension == 'GIF':
            if has_image_num.search(altText):
                return csvfileWriter(fileExt=1,
                                     fileExt_gif=1, fileNamepattern=1, has_image_num=1, imgResolution=imgReso_value)
            elif altText.lower().startswith('dsc'):
                return csvfileWriter(fileExt=1, fileExt_gif=1, fileNamepattern=1,
                                     imgResolution=imgReso_value)
            elif has_img_num.search(altText):
                return csvfileWriter(fileExt=1, fileExt_gif=1, fileNamepattern=1,
                                     has_img_num=1, imgResolution=imgReso_value)
            else:
                return csvfileWriter(fileExt=1, fileExt_gif=1, imgResolution=imgReso_value)
        elif fileextension == 'PNG':
            if has_image_num.search(altText):
                return csvfileWriter(fileExt=1,
                                     fileExt_png=1, fileNamepattern=1, has_image_num=1, imgResolution=imgReso_value)
            elif altText.lower().startswith('dsc'):
                return csvfileWriter(fileExt=1, fileExt_png=1, fileNamepattern=1,
                                     imgResolution=imgReso_value)
            elif has_img_num.search(altText):
                return csvfileWriter(fileExt=1, fileExt_png=1, fileNamepattern=1,
                                     has_img_num=1, imgResolution=imgReso_value)
            else:
                return csvfileWriter(fileExt=1, fileExt_png=1, imgResolution=imgReso_value)
        else:
            return csvfileWriter(fileExt=1,
                                 imgResolution=imgReso_value)

    def alttextChecker(altText, imgReso_value=0):
        if (len(altText) == 0):
            csvfileWriter(nullVal=1, imgResolution=imgReso_value)
        elif len(altText) <= 3:
            csvfileWriter(stopWord=1, imgResolution=imgReso_value)
        elif (len(altText.split()) == 1 and not(altText.endswith(tuple(imgExt)))and
                not(fnamePattern_expression.search(altText)) and
                not(wordDashWordpattern.search(altText))):
            if wordnet.synsets(altText):
                csvfileWriter(textinDictionary=1, imgResolution=imgReso_value)
            else:
                csvfileWriter(altText)
        elif altText.endswith(tuple(imgExt)):
            if altText.lower().endswith('jpg') or altText.lower().endswith('jpeg'):
                filepatternFinder(altText, imgReso_value, fileextension='JPG')
            elif altText.lower().endswith('gif'):
                filepatternFinder(altText, imgReso_value, fileextension='GIF')
            elif altText.lower().endswith('png'):
                filepatternFinder(altText, imgReso_value, fileextension='PNG')

            '''
            Check for Image filename pattern image1, image2,picture1,
            picture2,pic1,pic2 etc
            '''
        elif altText.startswith(tuple(fnamePattern_list)) or fnamePattern_expression.search(altText):
            if altText.lower().startswith('dsc'):
                csvfileWriter(fileNamepattern=1,
                              imgResolution=imgReso_value)
            elif has_image_num.search(altText):
                csvfileWriter(
                    altText,
                    fileNamepattern=1,
                    has_image_num=1,
                    imgResolution=imgReso_value)
            elif has_img_num.search(altText):
                csvfileWriter(
                    altText,
                    fileNamepattern=1,
                    has_img_num=1,
                    imgResolution=imgReso_value)
            else:
                csvfileWriter(
                    altText,
                    fileNamepattern=1,
                    imgResolution=imgReso_value)

        elif symbolOnlypattern.search(altText):
            csvfileWriter(symbolOnly=1, imgResolution=imgReso_value)
        elif symbolWord.match(altText):
            csvfileWriter(symbolWord=1)
        elif numOnlypattern.search(altText):
            csvfileWriter(numOnly=1, imgResolution=imgReso_value)
        elif wordpattern.search(altText):
            if wordandWordpattern.search(altText):
                if wordNumPercentageWordpattern.search(altText):
                    if wordDashWordpattern.search(altText):
                        if wordUnderscoreWordpattern.search(altText):
                            if wordSymbolwordpattern.search(altText):
                                csvfileWriter(words=1, wordNumPercentageWord=1,
                                              wordandWord=1, wordDashWord=1, wordUnderscoreWord=1,
                                              wordSymbolword=1, imgResolution=imgReso_value)
                            else:
                                csvfileWriter(words=1, wordNumPercentageWord=1,
                                              wordandWord=1, wordDashWord=1, wordUnderscoreWord=1, imgResolution=imgReso_value)
                        elif wordSymbolwordpattern.search(altText):
                            csvfileWriter(words=1, wordNumPercentageWord=1,
                                          wordandWord=1, wordDashWord=1, wordSymbolword=1, imgResolution=imgReso_value)
                        else:
                            csvfileWriter(words=1, wordNumPercentageWord=1,
                                          wordandWord=1, wordDashWord=1, imgResolution=imgReso_value)
                    elif wordUnderscoreWordpattern.search(altText):
                        if wordSymbolwordpattern.search(altText):
                            csvfileWriter(words=1, wordNumPercentageWord=1,
                                          wordandWord=1, wordUnderscoreWord=1, wordSymbolword=1, imgResolution=imgReso_value)
                        else:
                            csvfileWriter(words=1, wordNumPercentageWord=1,
                                          wordandWord=1, wordUnderscoreWord=1, imgResolution=imgReso_value)
                    elif wordSymbolwordpattern.search(altText):
                        csvfileWriter(words=1, wordNumPercentageWord=1,
                                      wordandWord=1, wordSymbolword=1, imgResolution=imgReso_value)
                    else:
                        csvfileWriter(words=1, wordNumPercentageWord=1,
                                      wordandWord=1, imgResolution=imgReso_value)
                elif wordDashWordpattern.search(altText):
                    if wordUnderscoreWordpattern.search(altText):
                        if wordSymbolwordpattern.search(altText):
                            csvfileWriter(words=1, wordandWord=1,
                                          wordDashWord=1, wordUnderscoreWord=1,
                                          wordSymbolword=1, imgResolution=imgReso_value)
                        else:
                            csvfileWriter(words=1, wordandWord=1,
                                          wordDashWord=1, wordUnderscoreWord=1, imgResolution=imgReso_value)
                    elif wordSymbolwordpattern.search(altText):
                        csvfileWriter(words=1, wordandWord=1,
                                      wordDashWord=1, wordSymbolword=1, imgResolution=imgReso_value)
                    else:
                        csvfileWriter(words=1, wordandWord=1,
                                      wordDashWord=1, imgResolution=imgReso_value)
                elif wordUnderscoreWordpattern.search(altText):
                    if wordSymbolwordpattern.search(altText):
                        csvfileWriter(words=1, wordandWord=1,
                                      wordUnderscoreWord=1, wordSymbolword=1, imgResolution=imgReso_value)
                    else:
                        csvfileWriter(words=1, wordandWord=1,
                                      wordUnderscoreWord=1, imgResolution=imgReso_value)
                elif wordSymbolwordpattern.search(altText):
                    csvfileWriter(words=1, wordandWord=1,
                                  wordSymbolword=1, imgResolution=imgReso_value)
                else:
                    csvfileWriter(words=1, wordandWord=1, imgResolution=imgReso_value)
            elif wordNumPercentageWordpattern.search(altText):
                if wordDashWordpattern.search(altText):
                    if wordUnderscoreWordpattern.search(altText):
                        if wordSymbolwordpattern.search(altText):
                            csvfileWriter(words=1, wordNumPercentageWord=1,
                                          wordDashWord=1, wordUnderscoreWord=1, wordSymbolword=1, imgResolution=imgReso_value)
                        else:
                            csvfileWriter(words=1, wordNumPercentageWord=1,
                                          wordDashWord=1, wordUnderscoreWord=1)
                    elif wordSymbolwordpattern.search(altText):
                        csvfileWriter(words=1, wordNumPercentageWord=1,
                                      wordDashWord=1, wordSymbolword=1)
                    else:
                        csvfileWriter(words=1, wordNumPercentageWord=1,
                                      wordDashWord=1)
                elif wordUnderscoreWordpattern.search(altText):
                    if wordSymbolwordpattern.search(altText):
                        csvfileWriter(words=1, wordNumPercentageWordpattern=1,
                                      wordUnderscoreWord=1, wordSymbolword=1)
                    else:
                        csvfileWriter(words=1, wordNumPercentageWord=1,
                                      wordUnderscoreWord=1)
                elif wordSymbolwordpattern.search(altText):
                    csvfileWriter(words=1, wordNumPercentageWord=1,
                                  wordSymbolword=1)
                else:
                    csvfileWriter(words=1, wordNumPercentageWord=1)
            elif wordDashWordpattern.search(altText):
                if wordUnderscoreWordpattern.search(altText):
                    if wordSymbolwordpattern.search(altText):
                        csvfileWriter(words=1, wordDashWord=1,
                                      wordUnderscoreWord=1, wordSymbolword=1)
                    else:
                        csvfileWriter(words=1, wordDashWord=1,
                                      wordUnderscoreWord=1)
                elif wordSymbolwordpattern.search(altText):
                    csvfileWriter(words=1, wordDashWord=1,
                                  wordSymbolword=1)
                else:
                    csvfileWriter(words=1, wordDashWord=1)
            elif wordUnderscoreWordpattern.search(altText):
                if wordSymbolwordpattern.search(altText):
                    csvfileWriter(words=1, wordUnderscoreWord=1,
                                  wordSymbolword=1)
                else:
                    csvfileWriter(words=1, wordUnderscoreWord=1)
            elif wordSymbolwordpattern.search(altText):
                csvfileWriter(words=1, wordSymbolword=1)
            else:
                csvfileWriter(words=1)
        elif symbolWord.search(altText):
            csvfileWriter(symbolWord=1)
        else:
            csvfileWriter()

    def csvfileWriter(nullVal=0, stopWord=0, fileExt=0, fileExt_jpg=0,
                      fileExt_gif=0, fileExt_png=0,
                      fileNamepattern=0,
                      has_image_num=0, has_img_num=0,
                      symbolOnly=0, symbolWord=0,
                      numOnly=0, words=0, imgResolution=0,
                      wordNumPercentageWord=0, wordUnderscoreWord=0,
                      wordDashWord=0, wordandWord=0, wordSymbolword=0,
                      textinDictionary=0):
        fileName = "featurevector_demo" + ".csv"
        # check if file featurevector.csv already exist
        if os.access(fileName, os.F_OK):
            fileMode = 'a+'
        else:
            fileMode = 'w'
        with open(fileName, fileMode) as f:
            csvWriter = csv.DictWriter(f, fieldnames=colHeader)
            if fileMode == 'w':  # Writing Column Header
                csvWriter.writerow(colField)

            # writing each row with data
            csvWriter.writerow({'nullValue': nullVal,
                                'stopWord': stopWord, 'fileExt': fileExt,
                                'fileExt_jpg': fileExt_jpg, 'fileExt_gif': fileExt_gif,
                                'fileExt_png': fileExt_png,
                                'fileNamepattern': fileNamepattern,
                                'Has_image_num': has_image_num,
                                'Has_img_num': has_img_num, 'numOnly': numOnly,
                                'symbolOnly': symbolOnly, 'symbolWord': symbolWord,
                                'words': words, 'imgResolution': imgResolution,
                                'wordNumPercentageWord': wordNumPercentageWord,
                                'wordUnderscoreWord': wordUnderscoreWord,
                                'wordDashWord': wordDashWord, 'wordandWord': wordandWord,
                                'wordSymbolword': wordSymbolword, 'alttextinDictionary': textinDictionary})
        return

    fobj = open('Dataset.csv', 'r')
    reader = csv.DictReader(fobj)

    def resolutionExtractor(IMG_height, IMG_width):
        global i
        height = imgResolutionpattern.search(IMG_height)
        width = imgResolutionpattern.search(IMG_width)
        if (height is None or width is None):
            return (False, False)
        else:
            return (int(height.group()), int(width.group()))
    for row in reader:
        print(row['ALT Text'])
        x, y = resolutionExtractor(row['IMG Height'], row['IMG Width'])
        if x and y:
            if imgResolutioncheck(x, y):
                alttextChecker(row['ALT Text'], 1)
            else:
                alttextChecker(row['ALT Text'], 0)
        else:
            continue
    fobj.close()


if __name__ == '__main__':
    main()
