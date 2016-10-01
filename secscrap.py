import csv
import os
import time
import socket
import urllib.parse as urlparse
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup


global imgext
imgext = ('jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF', 'tiff', 'png', 'PNG')

global hdrs
hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (\
        KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}

global certpath
certpath = 'gd_bundle-g2-g1.crt'

global extension
extension = ('.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.css', '.zip','.PDF')

colHeader = ['imageurl', 'url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'imageurl': 'IMAGE URL', 'url': '<img> TAG', 'src': 'SRC',
            'alttext': 'ALT Text', 'imgheight': 'IMG Height',
            'imgwidth': 'IMG Width'}

global errorcode
errorcode = (404, 500, 502, 503)

global urlList
urlList = []

global imgLinkList
imgLinkList = []


def getimgSize(imgurl, responseObj, nextUrl):
    '''
    Find the image size(height and width)
    '''
    urlbytedata = None

    if imgurl == nextUrl:
        urlbytedata = BytesIO(responseObj.content)
        try:
            im = Image.open(urlbytedata)
            return im.size
        except IOError as err:
            print("IOError :", str(err))
            return (None, None)
    else:
        print("URL %s gets redirected...." % imgurl)
        return(None, None)


def images(urlk,):
    print(urlk)
    # Reading URL and storing <img> tag
    try:
        responseObj = requests.get(urlk, verify=certpath, headers=hdrs, timeout=30)
        statusCode = responseObj.status_code
    except requests.exceptions.SSLError as e:
        responseObj = requests.get(urlk, verify=True, headers=hdrs, timeout=30)
        statusCode = responseObj.status_code
    except socket.timeout as e:
        print("Socket Time out Error!", str(e))
        print("Skipping to next url")
        return
    except requests.exceptions.Timeout as e:
        print("Timeout Error :", str(e))
        print("Skipping to next url")
        return

    if statusCode == 503:
        print("Internal Server Error..! Error Code: %d!" % statusCode)
        return

    # soupdata = souping(r)
    soupdata = BeautifulSoup(responseObj.content)
    imgtag = soupdata.find_all('img') # Finding all <img> tag

    print("****** ", len(imgtag), "<img> tags found *******")
    for link in imgtag:
        #print(urlk + "/" + link.get('src'))
        if (link.get('src')) == None:
            continue
        else:
            pass

        # Getting <src> attribute from <img> tag and storing it
        if (link.get('src')).startswith('.'):
            print("Invalid <src> path: starts with .(dot)", link.get('src'))
            srclink = link.get('src')[1:]
            continue
        else:
            srclink = link.get('src')

        if not(srclink.endswith(tuple(imgext))):
            print("<src> attribute ends with an invalid image extention", srclink)
            continue

        print("\n<src> attribute :", srclink)
        imgurl = urlparse.urljoin(urlk, srclink)
        if imgurl in imgLinkList:
            print("DUPLICATE IMAGE FOUND")
            continue
        else:
            imgLinkList.append(imgurl)

        imgurl = imgurl.replace(' ', '%20')
        time.sleep(5)
        try:
            responseObject = requests.get(
                imgurl, verify=certpath, headers=hdrs, timeout=30, allow_redirects=True)
            statusCode = responseObject.status_code
            nextUrl = responseObject.url
        except requests.exceptions.SSLError as e:
            responseObject = requests.get(
                imgurl, verify=True, headers=hdrs, timeout=30, allow_redirects=True)
            statusCode = responseObject.status_code
            nextUrl = responseObject.url
        except socket.timeout as e:
            print("Socket Time out Error!", str(e))
            continue
        except requests.exceptions.Timeout as e:
            print("Timeout Error!", str(e))
            continue

        # print(statusCode)
        if statusCode in errorcode:
            if statusCode == 404:
                print("URL [ %s ] is an INVALID URL(not found on the server)" % imgurl)
            elif statusCode == 500:
                print("Internal Server Error with URL %s" % imgurl)
            elif statusCode == 502:
                print("Bad Gateway......Error with URL %s" % imgurl)
            elif statusCode == 503:
                print("Service Unavailable....Error with URL %s" % imgurl)

            print("Skiping to next link in <imgtag>")
            continue
        else:
            print("No Error Code for image url.. Proceeding to fetch image-size")

        print("Image URL is : ", imgurl)
        imgheight = link.get('height')
        imgwidth = link.get('width')

        if not(imgheight and imgwidth):
            width, height = getimgSize(imgurl, responseObject, nextUrl)
        else:
            width, height = imgwidth, imgheight
        print("image Height : ", height)
        print("image Width : ", width)

        if (height == None or width == None):
            # height and width not found
            continue

        # Writes when height and Width found.
        fileWriter(imgurl, link, link.get('src'),
                   link.get('alt'), height, width)
    return

'''
def souping(url):
    # This function is for future use and it is incomplete as of now.
    result = list()
    urlResponse = requests.get(url, verify=certpath, headers=hdrs)
    result.append(urlResponse.statusCode)
    result.append(BeautifulSoup(urlResponse.content))
    return result
'''

def urlCrawler(url):
    '''
    Crawling website to find all Sub Links
    '''
    print("-------------------------Searching For Images-------------------------")
    images(url)
    print("-------------------------END Searching images-------------------------")

    try:
        responseObject = requests.get(url, verify=certpath, headers=hdrs, timeout=30)
        statusCode = responseObject.status_code
    except requests.exceptions.SSLError as e:
        responseObject = requests.get(url, verify=True, headers=hdrs, timeout=30)
        statusCode = responseObject.status_code
    except socket.timeout as e:
        print("Socket Time out Error!", str(e))
        return
    except requests.exceptions.Timeout as e:
        print("Timeout error!", str(e))
        return
    if statusCode in errorcode:
            return
    # Fetching all sub-url from root domain
  

    # soupdata = souping(url)
    soupdata = BeautifulSoup(responseObject.content)

    for tags in soupdata.findAll('a'): # Souping all <a href> tag
        linktag = str(tags.get('href'))
        # print("<a href> tag> ", linktag)
        '''
        if (linktag.startswith('/') and (not(linktag.endswith(tuple(extension))))):
            if ('=' not in linktag):
                abslink=urlparse.urljoin(url, linktag)
                if (abslink not in urlList):
                    urlList.append(abslink)
                    print(abslink)
        else: 
            continue
        '''
        abslink = urlparse.urljoin(url, linktag)
        #print("Absolute Link after join with seed link: ", abslink)
        if ((str(url) in abslink) and (not(abslink.endswith(tuple(extension))))):
            if (abslink not in urlList):
                urlList.append(abslink)
                print("New SUB-URL added to urlList", abslink)
            else:
                print("DUPLICATE SUB-URL FOUND", abslink)
        '''

        if (not(temp.endswith(tuple(extension)))):
            if (temp.startswith('http')):
                tmp.append(temp)
            else:
                temp = urlparse.urljoin(url, temp)
                tmp.append(temp)
        '''
    return


def urlFetch(mainUrl):
    urlList.append(urlparse.urljoin(mainUrl,"/"))
    for url in urlList:
        print("========================New Sub Url========================")
        print(url)
        urlCrawler(url)
    print("Total", len(urlList), "SUB-URL printed")


def fileWriter(imgurl, ul, src, alt, ht, wd):
    fileName = "dataset" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'w'

    csvWriter = csv.DictWriter(open(fileName, fileMode), fieldnames=colHeader)

    if fileMode == 'w':
        csvWriter.writerow(colField) # Writing Column Header

    if alt == " ":
        alt = "Alt text not defined"

    # writing each row with data
    csvWriter.writerow({'imageurl': imgurl, 'url': ul, 'src': src, 'alttext': alt, 'imgheight': ht,
                        'imgwidth': wd})
    return