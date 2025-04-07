# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 13:46:10 2025

@author: Asus
"""

import requests

# API kulcs és CSE ID
api_key = "AIzaSyD9ABV8pR98oXic3el2Qufms9OxtFts0nk"
cx = "764ee30944e1747ef"

def get_social_media():
    # Keresési kulcsszavak
    query = 'LIDL ("AI" OR "Machine Learning" OR "Data Science") site:instagram.com OR site:twitter.com OR site:facebook.com'  # LIDL szó és az egyik kívánt kifejezés

    # URL és kérés paraméterek
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        'key': api_key,  # API kulcs
        'cx': cx,        # CSE ID
        'q': query,      # Keresési lekérdezés
    }

    # HTTP GET kérés
    response = requests.get(url, params=params)

    lista = []

    # Ellenőrizzük, hogy sikeres volt-e a kérés
    if response.status_code == 200:
        # JSON válasz feldolgozása
        search_results = response.json()
        items = search_results.get('items', [])
        if items:
            for item in items:
                title = item['title']
                link = item['link']
                snippet = item['snippet']
                lista.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
                print(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
        else:
            print("Nem találtunk találatokat.")
    else:
        print("Hiba történt a kérés során.")

    return lista
