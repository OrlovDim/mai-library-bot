import sqlite3


class DB:

    cursor = None
    new_group_id = 0
    new_book_id = 0
    new_author_id = 0
    new_keyword_id = 0
    new_recomendation_id = 0

    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT MAX(group_id) FROM Group_")
        last_group_id = self.cursor.fetchall()
        self.cursor.execute("SELECT MAX(book_id) FROM Book")
        last_book_id = self.cursor.fetchall()
        self.cursor.execute("SELECT MAX(author_id) FROM Author")
        last_author_id = self.cursor.fetchall()
        self.cursor.execute("SELECT MAX(keyword_id) FROM Keyword")
        last_keyword_id = self.cursor.fetchall()
        if len(last_group_id) != 0:
            self.new_group_id = last_group_id[0]
        if len(last_book_id) != 0:
            self.new_book_id = last_book_id[0]
        if len(last_author_id) != 0:
            self.new_author_id = last_author_id[0]
        if len(last_keyword_id) != 0:
            self.new_keyword_id = last_keyword_id[0]


    def insert_group(self, group):
        self.cursor.execute("INSERT INTO Group_ VALUES (?, ?, ?)", (self.new_group_idw, group, int(group[1])))
        self.new_group_id += 1
        return self.new_group_id - 1


    def find_book_with_keyword(self, keyword):
        self.cursor.execute("SELECT book_id FROM Keyword WHERE word = ?", (keyword))
        return self.cursor.fetchall()
    

    def insert_book(self, book):
        self.cursor.execute("INSERT INTO Book VALUES (?, ?)", (self.new_book_id, book.title))

        for keyword in book.keywords:
            self.cursor.execute("INSERT INTO Keyword VALUES (?, ?)", (self.new_keyword_id, self.new_book_id, keyword))
            self.new_keyword_id += 1

        if book.annotation is not None:
            self.cursor.execute("INSERT INTO Annotation VALUES (?, ?)", (self.new_book_id, book.annotation))

        for author in book.authors:
            self.cursor.execute("SELECT author_id FROM Author name = ?", (author))
            author_id = self.cursor.fetchall()
            if len(author_id) == 0:
                self.cursor.execute("INSERT INTO Author VALUES (?, ?)", (self.new_author_id, author))
                self.cursor.execute("NSERT INTO Authorship VALUES (?, ?)", (self.new_author_id, self.new_book_id))
            else:
                self.cursor.execute("NSERT INTO Authorship VALUES (?, ?)", (author_id[0], self.new_book_id))
            self.new_author_id += 1
        self.new_book_id += 1
        return self.new_book_id - 1

    
    def insert_recomendation(self, group_id, book_id):
        self.cursor.execute("INSERT INTO Recomendation VALUES (?, ?)", (self.new_recomendation_id, book_id, group_id))
        self.new_recomendation_id += 1
        return self.new_recomendation_id - 1


    def commit(self):
        self.con.commit()

    def __del__(self):
        self.con.close()