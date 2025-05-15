import schedule_parsing as sp
import book_parsing as bp
import db_filling
import os

inst_num = 3 # Парсим только 3 институт

db = db_filling.DB(os.path.abspath("chat_bot.db"))

for group in sp.get_group(inst_num):
    group_id = db.insert_group(group)
    for lesson in sp.get_table(group):
        book_ids = db.find_book_with_keyword(lesson)

        if len(book_ids) != 0:
            for book_id in book_ids:
                db.insert_recomendation(group_id, book_id)

        else:
            book_lst = bp.find_book(lesson, quantity=4) # Разумно парсить первые 4 книги
            for book in book_lst:
                book_id = db.insert_book(book)
                db.insert_recomendation(group_id, book_id)
