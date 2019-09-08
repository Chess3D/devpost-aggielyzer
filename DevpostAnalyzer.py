import urllib, re
from bs4 import BeautifulSoup

# Base website
website = 'https://devpost.com/software/search?page='

# Keyphrase looking to be found
boundsKeyphrase = "Oh no! Looks like there's no software matching your query."

# Keyword being search for
keyword = input('Enter Search Term:\n')

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


# Gets all the relevant links from each page
def extract_link(page):
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


# Writes the data to a text file to be analyzed
def data_to_text():
    writeFile = open('ProjectText.txt', 'w')

    for i in range(40):
        for url in extract_link(i + 1):
            try:
                writeFile.write(format_page_text(url))
            except:
                print('Exception: Failed to write a project description to text file')
    
    writeFile.close()


# Gets the number of times the keyword appears
def keyword_count(text):
    if text.strip():
        text = re.sub('[^A-Za-z0-9]+', ' ', text)
        return text.lower().count(' ' + keyword.lower() + ' ')
    else:
        return -1


# Add keywords to a text file
def keywords_to_text():
    readFile = open('ProjectText.txt', 'r')
    writeFile = open('KeywordFrequency.txt', 'w')

    url = ''

    for line in readFile:
        if line.find('https://devpost.com/software/') != -1:
            url = line
        else:
            keywordCount = keyword_count(line)

            if keywordCount > 0:
                writeFile.write('Keyword Count: ' + str(keywordCount) + '\t' + url)

    readFile.close()
    writeFile.close()


# Sorts the projects by the frequency the keyword shows up
def sort_by_frequency():
    readFile = open('KeywordFrequency.txt', 'r')
    frequencyList = []

    for line in readFile:
        frequencyList.append(line)
    
    readFile.close
    frequencyList = sorted(frequencyList, reverse = True)
    writeFile = open('KeywordFrequency.txt', 'w')

    for line in frequencyList:
        writeFile.write(line)


keywords_to_text()
sort_by_frequency()