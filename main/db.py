import sqlite3


class DbCreator:
    def __init__(self, table_name):
        self.db = sqlite3.connect('vacancies.db')
        self.sql = self.db.cursor()
        self.table_name = table_name
        self.sql.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (Url TEXT, City TEXT ,Company TEXT ,Position TEXT)")
        self.db.commit()
        self.sql.execute(f'DELETE FROM {self.table_name}')

    def set_table(self, card_url_list):
        for line in card_url_list:
            self.sql.execute(f'INSERT INTO {self.table_name} VALUES (?, ?, ?, ?)', (line[0], line[1], line[2], line[3]))
            self.db.commit()


