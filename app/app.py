from src.scrape_news import scrapeNews
from src.google_trends import get_trends
from src.lidl_social_media_scraping import get_social_media
from src.sn_researchscrape import get_publications
from src.penzugyiadatok import get_financial_data


def main():
    """
    ez működik
    """
    #print("calling news scraper...")
    #result = scrapeNews()
    #print(result)
    """
    pytrends nem működik
    """
    #result1, result2 = get_trends()
    """
    social media is működik
    """
    #result = get_social_media()
    #print(result)
    """
    publications működik (selenium)
    """
    #result = get_publications()
    #print(result)
    """
    financial data
    """
    result = get_financial_data()
    print(result)


    #todo: pytrends
    #shape data into csv


if __name__ == '__main__':
    main()


