import psycopg2
import datetime
from stopwatch import timeit

USER = 'ach'
PASSWORD = 'ach'
DATABASE = 'ach'


class DbManager():

    def __init__(self, user, password, database):
        self.conn = psycopg2.connect(
            user=user,
            password=password,
            database=database,
            host="localhost",
        )
        self.cur = self.conn.cursor()
        self.initial_creation()

    def initial_creation(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS posts (
                            number INT PRIMARY KEY,
                            content TEXT,
                            date TIMESTAMP,
                            notions SMALLINT,
                            is_op BOOLEAN,
                            link TEXT,
                            files TEXT [],
                            thumbs TEXT []);
                            """)
        self.conn.commit()
        print("Initianl creation completed")

    def erase_all(self):
        self.cur.execute("DELETE FROM posts")
        self.conn.commit()

    def insert_post(self, post):
        self.cur.execute(f"""
                         INSERT INTO posts VALUES (%(number)s, %(content)s, %(date)s, %(notions)s, %(is_op)s, %(link)s, %(files)s, %(thumbs)s)
                         ON CONFLICT (number) DO UPDATE
                         SET notions = %(notions)s""",
                         post)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


@timeit
def update_database(top_posts):
    db = DbManager(USER, PASSWORD, DATABASE)
    db.erase_all()
    for post in top_posts:
        db.insert_post(post)
