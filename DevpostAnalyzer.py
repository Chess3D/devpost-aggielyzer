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
    i = 5000
    currentPage = 1
    pastPage = currentPage + 1
    state = False

    while True:

        while content_check(currentPage) == state:
            print('Current Page:',currentPage, '\tPast Page:', pastPage, '\tState:', state)
            
            if currentPage == pastPage:
                return currentPage
            elif state == True:
                pastPage = currentPage
                currentPage -= i
            else:
                pastPage = currentPage
                currentPage += i

        state = bool((int(state) + 1) % 2)
        i = i // 2

    return currentPage


print(binary_search())

# Get the max page count
# def get_page_count()
#     for 

# lastPage = 

# for link in devpost.find_all('page='):
#     print(link)

# print(devpost)