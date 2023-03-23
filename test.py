import sqlite3
from random import shuffle
con = sqlite3.connect('questions.db')
cur = con.cursor()
answered = sqlite3.connect('users.db').cursor().execute(f"SELECT answered_questions FROM USERS WHERE tg_id={1018622609}").fetchone()[0]
answered = [int(x) for x in answered.split()]
print(answered)
questions = cur.execute(f"SELECT * FROM Questions").fetchall()
questions = [x for x in questions if x[0] not in answered]
shuffle(questions)
quest = questions[0]
print(quest)
