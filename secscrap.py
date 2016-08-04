from bs4 import BeautifulSoup
from urllib.request import urlopen
import os, requests, csv
import urllib.parse as urlparse
from PIL import Image
from io import BytesIO

urllink = "https://www.ddps.in/"

# to find the image size(height and   width)

def get_image_size(imgurl):
    data = requests.get(imgurl).content
    im = Image.open(BytesIO(data))    
    return im.size
    
def images(urlk):

    # Reading URL and storing <img> tag
    r = urlopen(urlk).read()
    bsobj = BeautifulSoup(r)
    imgtag = bsobj.find_all('img')

    # Printing all image tag
    i = 1
    for i in range(len(imgtag)):
        print(i, imgtag[i])

    # Printing only required tag and value
    print("*" * 80)

    for link in imgtag:
        m=1
        srclink = str(link.get('src'))
        image = urlparse.urljoin(urllink,srclink)
        width, height = get_image_size(image)
        print(width, height)
        
        filewriter(m, link, link.get('src'), link.get('alt'), height, width)
        m += 1

def urlParse(url):
    thepage = urlopen(url)
    soupdata = BeautifulSoup(thepage, "lxml")
    return soupdata


soup = urlParse(urllink)
print("#" * 80)
extension = ('.pdf', '.doc', '.docx', '.txt', 'xls', 'xlsx')
urldict = {}
temp = []

# Fetching all sub-url from root domain
for ur in soup.findAll('a'):
    temp = ur.get('href')
    if str(temp).startswith('http') and (str(temp).endswith(tuple(extension)) == False):
        urldict[temp] = 0

print('Printing URL List.....................................')
#for key in urldict:
#    print(key, urldict[key])

print("Total", len(urldict), "link printed")

colHeader = ['s.no', 'url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'s.no' : 'S. No.', 'url' :  'URL', 'src' : 'SRC',
            'alttext' : 'ALT Text', 'imgheight' : 'IMG Height',
            'imgwidth' : 'IMG Width'}

def filewriter(sr,ul,src,alt,ht,wd):
    fileName = "pondiuni" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'wb'

    csvWriter = csv.DictWriter(open(fileName, fileMode), fieldnames = colHeader)


    if fileMode == 'wb':
        csvWriter.writerow(colField)

    csvWriter.writerow({'s.no' : sr, 'url' : ul, 'src' : src, 'alttext' : alt, 'imgheight' : ht, 'imgwidth' : wd})

for key in (x for x in urldict):
    images(key)

