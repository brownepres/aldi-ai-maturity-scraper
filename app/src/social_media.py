import requests
import time
import pandas as pd
import os
from transformers import pipeline
import sys

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

    # Eredmények mentése Excelbe
    df = pd.DataFrame(all_results)
    sentiment_pipeline = pipeline("sentiment-analysis")
    def analyze_sentiment(snippet):
        # Elemzés
        result = sentiment_pipeline(snippet)
        label = result[0]['label']  # 'POSITIVE', 'NEGATIVE', 'NEUTRAL'
        score = result[0]['score']  # Bizalom pontszám (0 és 1 között)
        
        # Kiszámoljuk a folytonos skálát (-1 és 1 között)
        if label == 'POSITIVE':
            continuous_score = 2 * (score - 0.5)  # Átalakítjuk 0.5-ből egy [-1, 1] skálára
        elif label == 'NEGATIVE':
            continuous_score = 2 * (0.5 - score)  # Negatív skála
        else:
            continuous_score = 0  # Semleges érték
        
        return label, score, continuous_score

    df[['Sentiment', 'Score', 'Continuous_Score']] = df['Snippet'].apply(lambda x: pd.Series(analyze_sentiment(x)))

    average_sentiment = df.groupby('Company')['Continuous_Score'].mean().reset_index()
    return average_sentiment['Continuous_Score'].iloc[0]
