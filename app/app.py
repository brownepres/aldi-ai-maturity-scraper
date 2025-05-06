from src.news2 import ScrapeNews
from src.social_media import getSocialMedia
from src.oldalak_diagram import pages
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os
import sys

nltk.download('vader_lexicon')  # Only once
sia = SentimentIntensityAnalyzer()

def get_resource_path(filename):
    if getattr(sys, 'frozen', False):  # running as a bundle
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'src', filename)
    else:
        path = f"src/{filename}"
        return path
    

file_path = get_resource_path('companies.xlsx')

companies = pd.read_excel(file_path, sheet_name='companies-english')
key_words = pd.read_excel(file_path, sheet_name='keywords-english')
key_words = key_words['keywords'].to_list()
companies_list = companies['company_name'].to_list()
print(companies_list)

list_for_df = []

def main():
    for i, company in enumerate(companies_list):
        print(f'Analyzing for: {company}')
        if i == 1:
            break
        list_item = [i, company]
        try:
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

            list_item.append(len(compound_scores))
            list_item.append(average_sentiment)
            list_item.append(keywords_count)
        except:
            print("The news could not be collected due to an error")
            list_item.append(None)
            list_item.append(None)
            list_item.append(None)
        
        try:
            social_media = getSocialMedia(company)
            print(social_media)    
            list_item.append(social_media)
        except Exception as e:
            print(f"Social media data could not be collected due to an error. {e}")
            list_item.append(None)

        list_for_df.append(list_item)
        print(i)
        
    output = pd.DataFrame(list_for_df, columns=['Id', 'Company', 'Number of news', 'Average news sentiment', 'Number of AI key words', 'Average social media sentiment'])    
    output.to_csv('output.csv')

    #scrape the desired pages
    print("Analyzing the desired AI trend pages")
    result = pages()


if __name__ == '__main__':
    main()


