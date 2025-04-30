from src.news2 import ScrapeNews
from src.social_media import getSocialMedia
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')  # Only once
sia = SentimentIntensityAnalyzer()

companies = pd.read_excel('src/Céglista.xlsx', sheet_name='Cégek - angol')
key_words = pd.read_excel('src/Céglista.xlsx', sheet_name='Céghez kapcsolható kulcs (angol')
key_words = key_words['Kulcsszavak'].to_list()
companies_list = companies['Cég neve'].to_list()
print(companies_list)

list_for_df = []

def main():
    for i, company in enumerate(companies_list):
        print(f'Analyzing for: {company}')
        if i == 10:
            break
        list_item = [i, company]
        try:
            print(f'getting the news for {company}')
            news = ScrapeNews(company)
            
            news_list = [news[i]['description'] for i in range(len(news)) if news[i]['description'] != None]
            compound_scores = [sia.polarity_scores(title)['compound'] for title in news_list]
            
            average_sentiment = sum(compound_scores) / len(compound_scores)
            
            list_of_words = []
            for description in news_list:
                words = description.lower().split()  # Split into words
                list_of_words.extend(words)
            
            keywords_count = 0
            for i in list_of_words:
                if i.lower() in key_words:
                    keywords_count += 1

            print(average_sentiment)
            list_item.append(len(compound_scores))
            list_item.append(average_sentiment)
            list_item.append(keywords_count)
        except:
            print("A híreket most nem sikerült összegyűjteni egy hiba miatt")
            list_item.append(None)
            list_item.append(None)
            list_item.append(None)
        
        try:
            social_media = getSocialMedia(company)
            print(social_media)    
            list_item.append(social_media)
        except Exception as e:
            print(f"Hiba történt: {e}")
            list_item.append(None)

        list_for_df.append(list_item)
        print(i)
        
    output = pd.DataFrame(list_for_df, columns=['Id', 'Company', 'Number of news', 'Average news sentiment', 'Number of AI key words', 'Average social media sentiment'])    
    output.to_csv('output.csv')

if __name__ == '__main__':
    main()


