import requests
def scrapeNews():
    url = ('https://newsapi.org/v2/everything?'
       'q=Apple&AI'
       'from=2025-03-10&'
       'sortBy=popularity&'
       'apiKey=xx')

    response = requests.get(url).json()
    return response