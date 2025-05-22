from requests import Session
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"}
url_group_base = r"https://mai.ru/education/studies/schedule/index.php?group="

table_work = Session()

# Генератор возвращает название (номер группы) ввиде строки
# Парсит по указанному институту
def get_group(inst_num):
    url_main = f"https://mai.ru/education/studies/schedule/groups.php?department=%D0%98%D0%BD%D1%81%D1%82%D0%B8%D1%82%D1%83%D1%82+%E2%84%96{inst_num}&course=all#"
    response = table_work.get(url_main, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find_all("a", class_="btn btn-soft-secondary btn-xs mb-1 fw-medium btn-group")
    
    for e in data:
        yield e.text

# Генератор парсит расписание по неделям
# Но явно это не указывает
# Возвращает название предмета
# Может принять диапазон недель для парсинга
# end = -1 означает до последеней недели в расписании
def get_lesson(group, start = 0, end = -1):

    url_group = url_group_base + group
    table_work.get(url_group, headers=headers)

    week = start
    while True:
        week += 1
        url_group += f"&week={week}"

        response = table_work.get(url_group, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all("p", class_="mb-2 fw-semi-bold text-dark")

        if len(data) == 0 or week == end:
            break

        for e in data:
            lesson = "".join(e.text.replace("\t", "").split("\n")[1:3]).replace("ЛК", "").replace("ПЗ", "").replace("ЛР", "")
            yield lesson
    yield None
