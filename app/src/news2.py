from newsdataapi import NewsDataApiClient

api = NewsDataApiClient(apikey='pub_835978595a1839887a70da7d5737b45ade500')

def ScrapeNews(company):
    response = api.news_api(q=company, language='en')
    
    return response['results']