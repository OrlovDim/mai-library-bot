from requests import Session
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"}
url_main = r"https://mai.ru/education/studies/schedule/groups.php?department=%D0%98%D0%BD%D1%81%D1%82%D0%B8%D1%82%D1%83%D1%82+%E2%84%963&course=all#"
url_group_base = r"https://mai.ru/education/studies/schedule/index.php?group="

table_work = Session()


def get_group():
    response = table_work.get(url_main, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find_all("a", class_="btn btn-soft-secondary btn-xs mb-1 fw-medium btn-group")
    
    for e in data:
        yield e.text


def get_table(group):

    url_group = url_group_base + group
    table_work.get(url_group, headers=headers)

    week = 0
    while True:
        week += 1
        url_group += f"&week={week}"

        response = table_work.get(url_group, headers=headers)

        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all("p", class_="mb-2 fw-semi-bold text-dark")

        if len(data) == 0:
            break

        for e in data:
            lesson = "".join(e.text.replace("\t", "").split("\n")[1:3]).replace("ЛК", "").replace("ПЗ", "").replace("ЛР", "")
            yield lesson
    yield None


# Демонстрация работы
for group in get_group():
    print("\n", group)
    for i, lesson in enumerate(get_table(group)):
        if lesson is None:
            break
        print(i, lesson)
