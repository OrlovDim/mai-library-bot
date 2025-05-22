import sqlite3


class DB:

    cursor = None
    new_group_id = 1
    new_book_id = 1
    new_author_id = 1
    new_keyword_id = 1
    new_recomendation_id = 1
    new_authorship_id = 1

    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)
        self.cursor = self.con.cursor()

        # Узнаем последнии значения id в БД
        self.cursor.execute("SELECT MAX(group_id) FROM Group_")
        last_group_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT MAX(book_id) FROM Book")
        last_book_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT MAX(author_id) FROM Author")
        last_author_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT MAX(keyword_id) FROM Keyword")
        last_keyword_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT MAX(authorship_id) FROM Authorship")
        last_authorship_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT MAX(rec_id) FROM Recomendation")
        last_recomendation_id = self.cursor.fetchone()[0]
        
        # Проверяем наличие уже существующих id в БД
        # Определяем новые (не занятые) id
        if last_group_id != None:
            self.new_group_id = last_group_id + 1
        if last_book_id != None:
            self.new_book_id = last_book_id + 1
        if last_author_id != None:
            self.new_author_id = last_author_id + 1
        if last_keyword_id != None:
            self.new_keyword_id = last_keyword_id + 1
        if last_authorship_id != None:
            self.new_authorship_id = last_authorship_id + 1
        if last_recomendation_id != None:
            self.new_recomendation_id = last_recomendation_id + 1


    def insert_group(self, group):
        self.cursor.execute("INSERT INTO Group_ VALUES (?, ?, ?)", (self.new_group_id, group, int(group[1])))
        self.new_group_id += 1
        return self.new_group_id - 1


    def find_book_with_keyword(self, keyword):
        self.cursor.execute("SELECT book_id FROM Keyword WHERE word = ?", (keyword,))
        return self.cursor.fetchall()
    

    def insert_book(self, book):
        self.cursor.execute("INSERT INTO Book VALUES (?, ?)", (self.new_book_id, book.title))

        for keyword in book.keywords:
            self.cursor.execute("INSERT INTO Keyword VALUES (?, ?, ?)", (self.new_keyword_id, self.new_book_id, keyword))
            self.new_keyword_id += 1

        if book.annotation is not None:
            self.cursor.execute("INSERT INTO Annotation VALUES (?, ?)", (self.new_book_id, book.annotation))

        for author in book.authors:
            self.cursor.execute("SELECT author_id FROM Author WHERE name = ?", (author,))
            author_id = self.cursor.fetchone()
            if author_id == None:
                self.cursor.execute("INSERT INTO Author VALUES (?, ?)", (self.new_author_id, author))
                self.cursor.execute("INSERT INTO Authorship VALUES (?, ?, ?)", (self.new_authorship_id, self.new_book_id, self.new_author_id))
                self.new_author_id += 1
            else:
                self.cursor.execute("INSERT INTO Authorship VALUES (?, ?, ?)", (self.new_authorship_id, self.new_book_id, author_id[0]))
            self.new_authorship_id += 1

        self.new_book_id += 1
        return self.new_book_id - 1

    
    def insert_recomendation(self, group_id, book_id):
        self.cursor.execute("INSERT INTO Recomendation VALUES (?, ?, ?)", (self.new_recomendation_id, book_id, group_id))
        self.new_recomendation_id += 1
        return self.new_recomendation_id - 1


    def commit(self):
        self.con.commit()


    def __del__(self):
        self.con.close()