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

class Book:
    authors = None
    keywords = None
    title = None
    annotation = None

# Функция возвращает список из объектов класса Book длинной quantity
# Если книга не соответствует теребованиям (не имеет имени, автора, ключевых слов), то на ее место ставится None
# Если при запросе ни одной книги не найдено, то вернется пустой список
def get_book(keyword, quantity):
    book_work.get(url_main, headers=headers)
    send_data["simpleCond"] = keyword
    response = book_work.post(url_search, headers=headers, data=send_data, allow_redirects=True)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find_all("div", class_="rs-data")
    book_lst = []
    if len(data) != 0:
        book_lst = [Book() for _ in range(quantity)]
        for i in range(quantity):

            authors = data[i].find("div", class_="rs-item findByDict IDX100a")
            keywords = data[i].find("div", class_="rs-item findByDict IDX653a")
            items = data[i].find_all("div", class_="rs-item")
            title = items[0]
            if authors is not None and keywords is not None and items is not None: 
                book_lst[i].authors = authors.text.replace("Авторы: ", "").split(", ")
                book_lst[i].keywords = keywords.text.replace("Ключевые слова: ", "").split(", ")
                book_lst[i].keywords.append(keyword)
                book_lst[i].title = title.text.split("   ")[-1]
                if items[4].text[:10] == "Аннотация:": #4й rs-item на сайте
                    book_lst[i].annotation = items[4].text[10:]
            else:
                book_lst[i] = None
    return book_lst
