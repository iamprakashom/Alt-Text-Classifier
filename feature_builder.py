import os
import csv
from nltk.corpus import wordnet
import re
colHeader = ['altText', 'nullValue', 'stopWord', 'fileExt', 'fileExt_jpg',
             'fileExt_gif', 'fileExt_png', 'fileExt_bmp', 'fileExt_pdf',
             'fileNamepattern', 'Has_fnamepattern_by_cam', 'Has_image_num',
             'Has_image_sym_num', 'Has_img_num', 'Has_img_sym_num',
             'symbolOnly', 'symbolWord', 'dollarNumber', 'numOnly', 'alphabetic',
             'imgResolution', 'wordNumPercentageWord', 'wordUnderscoreWord',
             'wordDashWord', 'wordandWord', 'alttextinDictionary']
colField = {'altText': 'ALT Text', 'nullValue': 'Null Value', 'stopWord': 'Stop Word',
            'fileExt': 'ALT Text contain File Extension', 'fileExt_jpg': 'Has fileExt JPG', 'fileExt_gif': 'Has fileExt GIF',
            'fileExt_png': 'Has fileExt PNG', 'fileExt_bmp': 'Has fileExt BMP',
            'fileExt_pdf': 'Has fileExt PDF', 'fileNamepattern': 'File Name Pattern',
            'Has_fnamepattern_by_cam': 'F_Name pattern by Camera', 'Has_image_num': 'Has <imageNum>',
            'Has_image_sym_num': 'Has_image_sym_num', 'Has_img_num': 'Has_img_num',
            'Has_img_sym_num': 'Has_img_sym_num', 'symbolOnly': 'Special Symbol Only', 'symbolWord': 'SymbolWord', 'dollarNumber': 'Currency',
            'numOnly': 'Numeric Only', 'alphabetic': 'Alphabetic Word', 'imgResolution': 'Image Resolution',
            'wordNumPercentageWord': 'Word Number Percent Word',
            'wordUnderscoreWord': 'Word Underscore Word', 'wordDashWord': 'Word Dash Word',
            'wordandWord': 'Word & Word', 'alttextinDictionary': 'Alt Text in Dictionary'}

global imgExt
imgExt = ['bmp', 'BMP', 'jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF', 'png',
          'PNG', 'PDF', 'pdf']
fnamePattern_list = ['dsc', 'DSC', 'img', 'IMG', 'Img', 'alt', 'Alt']


def main():
    fnamePattern_expression = re.compile('''
        image(\s|\(|\{|\_|\-|\/)?\d+(\s|\}|\))?|
        img(\s|\(|\{|\_|\-|\/)?\d+|
        pic(\s|\(|\{|\_|\-|\/)?\d+|
        banner(\s|\(|\{|\_|\-|\/\d*|
        banner(-|_)\w+|
        (slide|slider)(\s|\#|\$|\@|\%)?)
        ''', re.X | re.I)

    has_image_num = re.compile('^image(\s)?\d+', re.I)
    has_image_sym_num = re.compile('^image(\s)?(\(|\{|\_|\-)+\d+', re.I)
    has_img_num = re.compile('^img(\s)?\d+', re.I)
    has_img_sym_num = re.compile('^img(\s|\(|\{|\_|\-|\/)?\d+', re.I)
    symbolonlypattern = re.compile('[#$%?@]+')
    symbolonlypattern = re.compile('[#$%?@]+')
    dollarNumpattern = re.compile(
        '(\w*(\s))*?\$(\s)?\d+|\$(\s)?\d+\s(\w*(\s))*?')
    numOnlypattern = re.compile('^\d+$')

    def filepatternFinder(altText, fileextension=None):
        if fileextension == 'JPG':
            if has_image_num.match(altText):
                return csvfileWriter(altText, fileExt=1,
                                     fileExt_jpg=1, has_image_num=1)
            elif has_image_sym_num.match(altText):
                return csvfileWriter(altText, fileExt=1, fileExt_jpg=1,
                                     has_image_sym_num=1)
            elif altText.lower().startswith('dsc'):
                return csvfileWriter(altText, fileExt=1, fileExt_jpg=1,
                                     has_fnamepattern_by_camera=1)
        elif fileextension == 'GIF':
            if has_image_num.match(altText):
                return csvfileWriter(altText, fileExt=1,
                                     fileExt_gif=1, has_image_num=1)
            elif has_image_sym_num.match(altText):
                return csvfileWriter(altText, fileExt=1, fileExt_gif=1,
                                     has_image_sym_num=1)
            elif altText.lower().startswith('dsc'):
                return csvfileWriter(altText, fileExt=1, fileExt_gif=1,
                                     has_fnamepattern_by_camera=1)
        elif fileextension == 'PNG':
            if has_image_num.match(altText):
                return csvfileWriter(altText, fileExt=1,
                                     fileExt_png=1, has_image_num=1)
            elif has_image_sym_num.match(altText):
                return csvfileWriter(altText, fileExt=1, fileExt_png=1,
                                     has_image_sym_num=1)
            elif altText.lower().startswith('dsc'):
                return csvfileWriter(altText, fileExt=1, fileExt_png=1,
                                     has_fnamepattern_by_camera=1)
        elif fileextension == 'BMP':
            if has_image_num.match(altText):
                return csvfileWriter(altText, fileExt=1,
                                     fileExt_bmp=1, has_image_num=1)
            elif has_image_sym_num.match(altText):
                return csvfileWriter(altText, fileExt=1, fileExt_bmp=1,
                                     has_image_sym_num=1)
            elif altText.lower().startswith('dsc'):
                return csvfileWriter(altText, fileExt=1, fileExt_bmp=1,
                                     has_fnamepattern_by_camera=1)
        else:
            return csvfileWriter(altText, fileExt=1)

    def alttextChecker(altText):
        if (len(altText) == 0):
            csvfileWriter(altText, nullVal=1)
        elif len(altText) <= 2:
            csvfileWriter(altText, stopWord=1)
        elif len(altText.split()) == 1 and not(altText.endswith(tuple(imgExt))):
            if wordnet.synsets(altText):
                csvfileWriter(altText, textinDictionary=1)
            else:
                csvfileWriter(altText)
        elif altText.endswith(tuple(imgExt)):
            if altText.lower().endswith('jpg') or altText.lower().endswith('jpeg'):
                filepatternFinder(altText, fileextension='JPG')
            elif altText.lower().endswith('gif'):
                filepatternFinder(altText, fileextension='GIF')
            elif altText.lower().endswith('png'):
                filepatternFinder(altText, fileextension='PNG')
            elif altText.lower().endswith('bmp'):
                filepatternFinder(altText, fileextension='BMP')
            elif altText.lower().endswith('pdf'):
                csvfileWriter(altText, fileExt=1, fileExt_pdf=1)

            '''
            Check for Image filename pattern image1, image2,picture1,
            picture2,pic1,pic2 etc
            '''
        elif altText.startswith(tuple(fnamePattern_list)) or fnamePattern_expression.match(altText):
            if altText.lower().startswith('dsc'):
                csvfileWriter(altText, fileNamepattern=1,
                              has_fnamepattern_by_camera=1)
            elif has_image_num.match(altText):
                csvfileWriter(altText, fileNamepattern=1, has_image_num=1)
            elif has_image_sym_num.match(altText):
                csvfileWriter(altText, fileNamepattern=1, has_image_sym_num=1)
            elif has_img_num.match(altText):
                csvfileWriter(altText, fileNamepattern=1, has_img_num=1)
            elif has_img_sym_num.match(altText):
                csvfileWriter(altText, fileNamePattern=1, has_img_sym_num=1)
        elif symbolonlypattern.match(altText):
            csvfileWriter(altText, symbolOnly=1)
        elif dollarNumpattern.match(altText):
            csvfileWriter(altText, dollarNum=1)
        elif numOnlypattern.match(altText):
            csvfileWriter(altText, numOnly=1)
        else:
            csvfileWriter(altText)

    def csvfileWriter(alt, nullVal=0, stopWord=0, fileExt=0, fileExt_jpg=0,
                      fileExt_gif=0, fileExt_png=0, fileExt_bmp=0, fileExt_pdf=0,
                      fileNamepattern=0, has_fnamepattern_by_camera=0,
                      has_image_num=0, has_image_sym_num=0, has_img_num=0,
                      has_img_sym_num=0, symbolOnly=0, symbolWord=0,
                      dollarNum=0, numOnly=0, alphabet=0, imgResolution=0,
                      wordNumPercentWord=0, wordUnderscoreWord=0,
                      wordDashWord=0, wordandWord=0, textinDictionary=0):
        fileName = "featurevector" + ".csv"
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
            csvWriter.writerow({'altText': alt, 'nullValue': nullVal,
                                'stopWord': stopWord, 'fileExt': fileExt,
                                'fileExt_jpg': fileExt_jpg, 'fileExt_gif': fileExt_gif,
                                'fileExt_png': fileExt_png, 'fileExt_bmp': fileExt_bmp,
                                'fileExt_pdf': fileExt_pdf, 'fileNamepattern': fileNamepattern,
                                'Has_fnamepattern_by_cam': has_fnamepattern_by_camera,
                                'Has_image_num': has_image_num, 'Has_image_sym_num': has_image_sym_num,
                                'Has_img_num': has_img_num, 'Has_img_sym_num': has_img_sym_num,
                                'symbolOnly': symbolOnly, 'symbolWord': symbolWord,
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
        alttextChecker(row['ALT Text'])
    fobj.close()


if __name__ == '__main__':
    main()
