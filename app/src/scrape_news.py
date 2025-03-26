import requests
def scrapeNews():
    url = ('https://newsapi.org/v2/everything?'
       'q=Apple&AI'
       'from=2025-03-10&'
       'sortBy=popularity&'
       'apiKey=237d140128514a4bb46272ece0d0bbff')

    response = requests.get(url).json()
    return response