from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def celonis():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    urls = [
        "https://www.celonis.com/press/in-the-news/",
        "https://www.celonis.com/press/partner-press-releases/"
    ]

    all_articles = []

    for url in urls:
        driver.get(url)

        # Cookie elfogadása, ha van
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
        except:
            pass

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ems-press-item"))
            )

            articles = driver.find_elements(By.CLASS_NAME, "ems-press-item")

            for article in articles:
                try:
                    title_elem = article.find_element(By.CLASS_NAME, "ems-press-item__title")
                    title = title_elem.text.strip()
                    relative_link = article.get_attribute("href")
                    full_link = f"https://www.celonis.com{relative_link}" if relative_link.startswith("/") else relative_link

                    all_articles.append({
                        "title": title,
                        "link": full_link
                    })

                except Exception as e:
                    print(f"Elem feldolgozási hiba: {e}")
                    continue

        except Exception as e:
            print(f"Cikkek betöltési hiba az oldalon: {url} -> {e}")

    for article in all_articles:
        print(f"Cím: {article['title']}")
        print(f"Link: {article['link']}\n")

    driver.quit()
    return all_articles


def news(pages=20):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    base_url = "https://www.marketresearchfuture.com/news"
    all_news = []

    for page_num in range(1, pages + 1):
        url = f"{base_url}?page={page_num}"
        print(f"Oldal betöltése: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "layout"))
            )

            articles = driver.find_elements(By.CLASS_NAME, "layout")

            for article in articles:
                try:
                    title_elem = article.find_element(By.TAG_NAME, "h6").find_element(By.TAG_NAME, "a")
                    title = title_elem.text.strip()
                    relative_link = title_elem.get_attribute("href")

                    # Teljes link
                    full_link = relative_link if relative_link.startswith("http") else base_url + relative_link

                    if title and full_link:
                        all_news.append({
                            "title": title,
                            "link": full_link
                        })

                except Exception as e:
                    print(f"Hiba a cikk feldolgozásakor: {e}")
                    continue

        except Exception as e:
            print(f"Hiba az oldal betöltésekor ({url}): {e}")

    driver.quit()

    # Kiíratás
    for news in all_news:
        print(f"Cím: {news['title']}")
        print(f"Link: {news['link']}\n")

    return all_news


def marketresearchfuture(base_url, pages=20):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    root_url = "https://www.marketresearchfuture.com"
    all_reports = []

    for page_num in range(1, pages + 1):
        url = f"{base_url}?page={page_num}"
        print(f"Oldal betöltése: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "iiborder"))
            )

            report_blocks = driver.find_elements(By.CLASS_NAME, "iiborder")

            for block in report_blocks:
                try:
                    # Első link és href (ez az oldal linkje)
                    report_link_tag = block.find_element(By.TAG_NAME, "a")
                    relative_link = report_link_tag.get_attribute("href")
                    full_link = (
                        root_url + relative_link
                        if relative_link.startswith("/")
                        else relative_link
                    )

                    # Cím kinyerése a span vagy strong-ból
                    try:
                        title = block.find_element(By.CLASS_NAME, "report-icon").text.strip()
                    except:
                        title = block.find_element(By.TAG_NAME, "strong").text.strip()

                    # Dátum
                    try:
                        date = block.find_element(By.CLASS_NAME, "date").text.strip()
                    except:
                        date = ""

                    all_reports.append({
                        "title": title,
                        "link": full_link,
                        "date": date
                    })

                except Exception as e:
                    print(f"Hiba egy elem feldolgozásakor: {e}")
                    continue

        except Exception as e:
            print(f"Hiba az oldal betöltésekor ({url}): {e}")

    driver.quit()

    for report in all_reports:
        print(f"Cím: {report['title']}")
        print(f"Dátum: {report['date']}")
        print(f"Link: {report['link']}\n")

    return all_reports

def sstonework():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    urls = [
        "https://www.ssonetwork.com/reports",
        "https://www.ssonetwork.com/articles"
    ]

    all_articles = []
    base_url = "https://www.ssonetwork.com"

    for url in urls:
        driver.get(url)

        # Töltsük be az oldalon a további elemeket
        for i in range(5):
            try:
                load_more_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn-load-more"))
                )
                driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(2)  # Várjunk, míg betöltődnek az új elemek
            except Exception as e:
                print(f"Nem sikerült a {i+1}. Load more kattintás: {e}")
                break

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "post-item"))
            )

            article_divs = driver.find_elements(By.CLASS_NAME, "post-item")

            for div in article_divs:
                try:
                    title_elem = div.find_element(By.CLASS_NAME, "article-title").find_element(By.TAG_NAME, "a")
                    title = title_elem.text.strip()
                    relative_link = title_elem.get_attribute("href")
                    full_link = relative_link if relative_link.startswith("http") else base_url + relative_link

                    date_span = div.find_element(By.CLASS_NAME, "text-date").find_element(By.TAG_NAME, "span")
                    date = date_span.text.strip()

                    all_articles.append({
                        "title": title,
                        "date": date,
                        "link": full_link
                    })

                except Exception as e:
                    print(f"Hiba egy elem feldolgozásakor: {e}")
                    continue

        except Exception as e:
            print(f"Hiba a cikkek betöltésekor ezen az oldalon: {url} -> {e}")

    for article in all_articles:
        print(f"Cím: {article['title']}")
        print(f"Dátum: {article['date']}")
        print(f"Link: {article['link']}\n")

    driver.quit()
    return all_articles

def thinkhdi():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # opcionális: ne nyissa meg a böngészőablakot
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    base_url = "https://www.thinkhdi.com/library/supportworld/metrics?pg="
    all_articles = []

    try:
        for page in range(1, 21):
            url = base_url + str(page)
            driver.get(url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "TaggedContent-Item"))
                )
            except Exception as e:
                print(f"Nem található tartalom az oldalon ({url}): {e}")
                continue

            articles = driver.find_elements(By.CLASS_NAME, "TaggedContent-Item")

            for article in articles:
                try:
                    title_elem = article.find_element(By.CLASS_NAME, "TaggedContent-Title").find_element(By.TAG_NAME, "a")
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute("href")

                    all_articles.append({
                        "title": title,
                        "link": link
                    })

                except Exception as e:
                    print(f"Hiba egy elem feldolgozásakor: {e}")
                    continue

    finally:
        driver.quit()

    for art in all_articles:
        print(f"Cím: {art['title']}")
        print(f"Link: {art['link']}\n")

    return all_articles

def servicenow_blog():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    urls = [
        "https://www.servicenow.com/blogs/2025",
        "https://www.servicenow.com/blogs/2024"
    ]

    all_articles = []

    # Két oldal kezelése
    for url in urls:
        driver.get(url)

        # Cookie elfogadása, ha szükséges
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
        except:
            pass

        # Cikkek betöltése
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
            )
            
            # Cikkek begyűjtése
            articles = driver.find_elements(By.CLASS_NAME, "card")
            
            # Cikkek feldolgozása
            for article in articles:
                try:
                    title_elem = article.find_element(By.TAG_NAME, "a")
                    title = title_elem.text.strip()
                    
                    # Link beszerzése
                    relative_link = title_elem.get_attribute("href")
                    full_link = f"https://www.servicenow.com{relative_link}" if relative_link.startswith("/") else relative_link
                    
                    # Dátum
                    date_elem = article.find_element(By.CLASS_NAME, "card-date")
                    date = date_elem.text.strip() if date_elem else "Nincs dátum"
                    
                    all_articles.append({
                        "title": title,
                        "link": full_link,
                        "date": date
                    })
                except Exception as e:
                    print(f"Elem feldolgozási hiba: {e}")
                    continue

            # "Load More" gomb megnyomása, ha létezik
            while True:
                try:
                    load_more_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "cta-loadmore"))
                    )
                    load_more_button.click()  # Rákattintunk a "Load More" gombra
                    time.sleep(3)  # Várakozunk egy kicsit, hogy a cikkek betöltődjenek

                    # Cikkek újra betöltése
                    articles = driver.find_elements(By.CLASS_NAME, "card")

                    for article in articles:
                        try:
                            title_elem = article.find_element(By.TAG_NAME, "a")
                            title = title_elem.text.strip()
                            
                            relative_link = title_elem.get_attribute("href")
                            full_link = f"https://www.servicenow.com{relative_link}" if relative_link.startswith("/") else relative_link
                            
                            date_elem = article.find_element(By.CLASS_NAME, "card-date")
                            date = date_elem.text.strip() if date_elem else "Nincs dátum"
                            
                            all_articles.append({
                                "title": title,
                                "link": full_link,
                                "date": date
                            })
                        except Exception as e:
                            print(f"Elem feldolgozási hiba: {e}")
                            continue

                except:
                    # Ha nincs több "Load More" gomb
                    print("Nincs több cikk betölthető.")
                    break

        except Exception as e:
            print(f"Cikkek betöltési hiba: {e}")

    driver.quit()

    # Cikkek kiírása
    for article in all_articles:
        print(f"Cím: {article['title']}")
        print(f"Link: {article['link']}")
        print(f"Dátum: {article['date']}\n")

    return all_articles


# celonis.com
celonis()

# marketresearchfuture.com
marketresearchfuture("https://www.marketresearchfuture.com/report-types/cooked-research-reports", pages=20)
marketresearchfuture("https://www.marketresearchfuture.com/report-types/half-cooked-research-reports", pages=20)

# ssonetwork.com
sstonework()

# thinkhdi.com
thinkhdi()

#servicenow.com/blog
servicenow_blog()