import urllib
from bs4 import BeautifulSoup

# Base website
website = 'https://devpost.com/software/search?page='

# Keyphrase looking to be found
boundsKeyphrase = "Oh no! Looks like there's no software matching your query."


# Checks if the keyword is on the desired page
def content_check(page):
    html = urllib.request.urlopen(website + str(page)).read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    return text.find(boundsKeyphrase) != -1


# Preforms a binary search to find the last page
def binary_search():    
    i = 10000
    currentPage = 0
    pastPage = i
    state = False

    while True:
        state = bool((int(state) + 1) % 2)
        i = i // 2

        while content_check(currentPage) == state:        
            if currentPage == pastPage:
                return currentPage
            else:
                pastPage = currentPage

            if state == True:
                currentPage -= i
            else:
                currentPage += i


# Pulls text and converts into txt file
def pull_text(page):
    html = urllib.request.urlopen(website + str(page)).read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    pageText = open('PageText.txt','w')
    pageText.write(text)
    pageText.write('\n')


for page in range(2):
    pull_text(page + 1)


# Gets all the relevant links from each page
def extract_links(page):
    html = urllib.request.urlopen(website + str(page)).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.findAll('a')
    keyphrase = "https://devpost.com/software/"
    linkList = []

    for t in tags:
        text = t.attrs['href']

        if text.find(keyphrase) != -1 and text.find('https://devpost.com/software/search?page=') == -1:
            linkList.append(t.attrs['href'])
    
    return linkList


# Formats a URL into the final usable data
def format_page_text(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.findAll('p')
    formatedText = ''
    
    for t in tags:
        formatedText += t.text
    
    while formatedText.find('  ') != -1:
        formatedText = formatedText.replace('  ', ' ')

    formatedText = formatedText.replace('\n', '')
    formatedText = formatedText.replace('\t', '')

    return '' + url + '\n' + formatedText + '\n'


# Given a word and source file a count of the # of occurrences in stored in an array
def get_keyword_count(keyword, srcFile):
    file = open(srcFile, "r")
    lines = file.readlines()

    # Takes the input file and puts every word in its own index
    for i in lines:
        words = lines.split(" ")

    # Array format: [ page_description_0, count0, page_description_1, count1, ... ]
    pageCount = []
    count = 0

    # If currentWord equals keyWord count is incremented
    # Else if 'page_description_text' is found in currentWord then it and count are appended to array
    for currentWord in words:
        if currentWord.lower() == keyword.lower():
            count += 1
        elif 'page_description_text_' in currentWord.lower():
            pageCount.append(currentWord)
            pageCount.append(count)
            count = 0


# Writes text file with the # of occurrences of keyWord in each different project
def write_keyword_count(keyWord, list):
    tempDescrip = ''
    tempCount = 0
    file = open('KeywordCount.txt', 'w')

    # If j is an even number then it indicates a new Project
    # Else i is count and the info is written to file
    for i in pageCount and j in range(0, len(list)):
        if j % 2 == 0 :
            tempDescrip = i
        else:
            tempCount = i
            file.write(tempDescrip, ': ', tempCount, '\n')

    file.close()