#pip install google
#pip install beautifulsoup4
#pip install requests

# Please make sure that the library insalled is google and not googlesearch-python
# And if you have any other variations installed make sure to create a virtual environment
# And have only google libarary installed in it and no other variations
# DOCS : https://python-googlesearch.readthedocs.io/en/latest/

import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import os

def google_search(query, num_results, sleep_interval):
    results = []
    try:
        # This will search for articles that are 1 week old
        # To look for older articles edit the tbs argument
        for url in search(query, tbs="qdr:w", num=num_results, pause=sleep_interval):
            results.append(url)
        return results
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print(f"Rate limit exceeded, retrying in {sleep_interval} seconds...")
            time.sleep(sleep_interval)
            return google_search(query, num_results, sleep_interval * 2) 
        else:
            raise
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else 'No Title'
        paragraphs = soup.find_all('p')
        content = '\n'.join([para.get_text() for para in paragraphs])

        filename = os.path.join("ensimag_news", f"{title[:50].replace(' ', '_')}.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(content)
        print(f"Saved article: {title[:50]}")

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

def main():
    
    # Save the text files with the resulting articles in this folder
    os.makedirs("ensimag_news", exist_ok=True)

    queries = [
        "actualités positives ENSIMAG Grenoble",
        "réussites des étudiants ENSIMAG Grenoble",
        "projets innovants ENSIMAG Grenoble",
        "succès des alumni ENSIMAG Grenoble",
        "distinctions reçues ENSIMAG Grenoble",
        "initiatives ENSIMAG Grenoble",
        "événements positifs ENSIMAG Grenoble",
        "collaborations ENSIMAG Grenoble",
        "recherches ENSIMAG Grenoble",
        "partenariats ENSIMAG Grenoble",
        "prix remportés ENSIMAG Grenoble",
        "témoignages positifs ENSIMAG Grenoble",
        "projets étudiants ENSIMAG Grenoble",
        "réalisations ENSIMAG Grenoble",
        "succès académiques ENSIMAG Grenoble"
    ]

    for query in queries:
        print(f"Searching for: {query}")
        # Please don't change the sleep interval to lower than 35 seconds
        # This will end up by getting your IP banned
        search_results = google_search(query, 10, 40.0) 

        for result in search_results:
            print(f"Scraping: {result}")
            get_article(result)

if __name__ == "__main__":
    main()

# Developed by Mohamed Mahdi
