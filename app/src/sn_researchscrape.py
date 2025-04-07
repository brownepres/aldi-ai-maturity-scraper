# -*- coding: utf-8 -*-
#Chromedriver-t le kell tölteni a gépre és hozzáadni a path-hoz

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_publications():
    # WebDriver beállítása
    driver = webdriver.Chrome()

    # URL, amelyet scrapelni szeretnél
    url = "https://www.servicenow.com/research/publication.html"

    # Oldal betöltése
    driver.get(url)

    # Várakozás, hogy a JavaScript betöltse az adatokat
    time.sleep(5)

    # Cikkek keresése
    publications = driver.find_elements(By.CLASS_NAME, 'pub-list-item')

    # Változó a cikkek mentésére
    publications_data = []

    # Cikkek címének és PDF linkjének kinyerése
    for pub in publications:
        title = pub.find_element(By.CSS_SELECTOR, 'a[style="font-weight: bold;"]')
        pdf_link = pub.find_element(By.CLASS_NAME, 'btn-outline-primary').get_attribute('href')
        
        # Ha mindkét adat létezik, hozzáadjuk a listához
        if title and pdf_link:
            publications_data.append({
                'title': title.text,
                'pdf_link': pdf_link
            })

    # A kinyert adatokat egy változóban tároljuk
    # Kinyomtathatjuk a változó tartalmát, ha szükséges
    for publication in publications_data:
        print(f"Cikk cím: {publication['title']}")
        print(f"PDF link: {publication['pdf_link']}\n")
        
    # WebDriver bezárása
    driver.quit()

    return publications_data