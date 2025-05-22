import schedule_parsing as sp
import book_parsing as bp
import db_filling
import os

"""
При запуске парсер будет ждать ответ от сервера 10 - 15 секунд
прежде, чем начать заполнять БД
"""

inst_num = 3 # Парсим только 3 институт

db = db_filling.DB(os.path.abspath("chat_bot.db"))

for group in sp.get_group(inst_num):
    group_id = db.insert_group(group)
    print("\n\n", group)
    for lesson in sp.get_lesson(group): # Можно парсить не все недели (см. schedule_parsing.py)
        # Храним ключевые слова в верхнем регистре, и оперируем с ними так же
        lesson = lesson.upper()
        print(lesson)
        book_ids = db.find_book_with_keyword(lesson)

        if len(book_ids) != 0:
            for book_id in book_ids:
                db.insert_recomendation(group_id, book_id[0])
                db.commit()

        else:
            book_lst = bp.get_book(lesson, quantity=4) # Разумно парсить первые 4 книги
            for book in book_lst:
                if book is not None:
                    print("\n", book.title)
                    book_id = db.insert_book(book)
                    db.insert_recomendation(group_id, book_id)
                    db.commit()
