import urllib
from bs4 import BeautifulSoup

# Base website
website = 'https://devpost.com/software/search?page='

# Keyword looking to be found
keyword = "Oh no! Looks like there's no software matching your query."


# Checks if the keyword is on the desired page
def content_check(page):
    html = urllib.request.urlopen(website + str(page)).read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    return text.find(keyword) != -1


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

print(format_page_text('https://devpost.com/software/takeme2'))
print(format_page_text('https://devpost.com/software/cryptotoken-access-your-credentials-marketplace'))