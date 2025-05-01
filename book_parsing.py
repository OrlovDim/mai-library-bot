from requests import Session
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"}
url_main = r"https://elibrary.mai.ru/MegaPro/Web/Search/Simple"
url_search = "https://elibrary.mai.ru/MegaPro/Web/SearchResult/Simple"

book_work = Session()
send_data = {
    "simpleCond": "keyword",
    "cond_words": "all",
    "cond_match": "exect_match",
    "filter_dateFrom": "",
    "filter_dateTo": ""
}


def find_book(keyword):
    book_work.get(url_main, headers=headers)
    send_data["simpleCond"] = keyword
    response = book_work.post(url_search, headers=headers, data=send_data, allow_redirects=True)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find_all("div", class_="rs-data")
    for i in range(4): # разумно парсить первые четыре книги
        authors = data.find("div", class_="rs-item findByDict IDX100a")
        keywords = data.find("div", class_="rs-item findByDict IDX653a")
        title = data.find("div", class_="rs-item")
        authors = authors.text.replace("Авторы: ", "")
        keyword = keywords.text.replace("Ключевые слова: ", "")
        title = title.text.split("   ")[-1]
    return 


find_book("Общая физика") # демонстрация работы
