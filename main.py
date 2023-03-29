import json
import requests
from bs4 import BeautifulSoup

# url = "http://books.toscrape.com/"

def scraper(url, type):
    result = {
        "data": [],
        "type": type
    }
    res = requests.get(url) # <Response [200]>
    res_string = res.text # string
    soup = BeautifulSoup(res_string, 'html.parser') # <class 'bs4.BeautifulSoup'>
    lst = soup.find_all("article", {"class": "product_pod"})

    # title
    def find_title(article):
        a = article.findChildren("a")[0]
        img = a.findChildren("img")[0]
        title = img.get("alt")
        return title

    # star rate
    def find_rate(article):
        p = article.findChildren("p")[0]
        rating = p.get("class")[1]
        return rating

    # price
    def find_price(article):
        p = article.findChildren("p", {"class": "price_color"})[0]
        price = p.text
        return price

    # availability
    def find_availability(article):
        p = article.findChildren("p", {"class": "instock availability"})[0]
        availability = p.text.strip()
        return availability
    

    for article in lst:
        result["data"].append(
            {
                "title": find_title(article),
                "rating": find_rate(article),
                "price":  find_price(article),
                "availability": find_availability(article)
            }
        )

    return result

def api_creator(*objs):
    return json.dumps(obj=[obj for obj in objs], indent=4, sort_keys=False)

def counting_1(data, rate):
    rating_number = {
        1: "One",
        2: "Twi",
        3: "Three",
        4: "Four",
        5: "Five"
    }
    target_rate = rating_number[rate]
    data = json.loads(data)
    counter = 0
    for obj in data:
        for book in obj.data:
            if book.rating == target_rate:
                counter += 1

    return counter

def counting_2(rate, *all):
    counter = 0
    for obj in all:
        lst = obj['data']
        for data in lst:
            if data['rating'].lower() == rate.lower():
                counter += 1
    return counter
    

        
if __name__ == "__main__":
    url_travel = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    url_mystery = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    url_historical_fiction = "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"

    scraper_travel = scraper(url_travel, "travel")
    scraper_mystery = scraper(url_mystery, "mystery")
    scraper_historical_fiction = scraper(url_historical_fiction, "historical-fiction")

    api = api_creator(scraper_travel, scraper_mystery, scraper_historical_fiction)

    num = counting_2("One", scraper_travel, scraper_mystery, scraper_historical_fiction)

