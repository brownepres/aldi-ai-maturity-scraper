import requests
import time
import pandas as pd
import os
import sys
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')  # Only once
sia = SentimentIntensityAnalyzer()

# API kulcs és CSE ID
api_key = "AIzaSyDMgAtDM9eDQHH5YMiQ45RJY5xta1fVOrI"
cx = "5785af9aa16b4437b"

# Kulcsszavak beolvasása
def get_resource_path(filename):
    if getattr(sys, 'frozen', False):  # running as a bundle
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'src', filename)
    else:
        path = f"src/{filename}"
        return path

file_path = get_resource_path('companies.xlsx')
kulcsszavak_df = pd.read_excel(file_path, sheet_name='keywords-english')
kulcsszavak = kulcsszavak_df.iloc[:, 0].dropna().unique()  # Feltételezve, hogy az első oszlopban vannak a kulcsszavak

# Kulcsszavak összeállítása "OR" kapcsolóval
kulcsszo_kifejezes = " OR ".join([f'"{kulcsszo}"' for kulcsszo in kulcsszavak])

url = "https://www.googleapis.com/customsearch/v1"
max_results = 10

def getSocialMedia(company):

    # Összes eredmény
    all_results = []
    query = f'{company} ({kulcsszo_kifejezes}) site:instagram.com OR site:twitter.com OR site:facebook.com'

    for start_index in range(1, max_results + 1, 10):
        params = {
            'key': api_key,
            'cx': cx,
            'q': query,
            'start': start_index
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            search_results = response.json()
            items = search_results.get('items', [])
            if not items:
                print(f"Nincs több találat: {company}")
                break

            for item in items:
                all_results.append({
                    'Company': company,
                    'Title': item.get('title'),
                    'Link': item.get('link'),
                    'Snippet': item.get('snippet')
                })

                time.sleep(5)
        else:
            print(f"Hiba {company} cégnél, {start_index}. találatnál: {response.status_code}")
            break

        compound_scores = [sia.polarity_scores(i['Snippet'])['compound'] for i in all_results]
            
        average_sentiment = sum(compound_scores) / len(compound_scores)
    return average_sentiment
