from src.scrape_news import scrapeNews


def main():
    print("calling news scraper...")
    result = scrapeNews()
    print(result)
    #todo: call all other functions
    #shape data into csv


if __name__ == '__main__':
    main()


