from src.scrape_news import scrapeNews


def main():
    print("calling news scraper...")
    result = scrapeNews()
    print(result)


if __name__ == '__main__':
    main()


