import sqlite3

class Course:
	def get_all():
		con = sqlite3.connect("webcms4.sqlite")

		cur = con.cursor()
		cur.execute("SELECT ID, CODE, SEMESTER, NAME FROM COURSES")
		rows = cur.fetchall()

		con.close()
		return rows

	def get_query(term):
		con = sqlite3.connect("webcms4.sqlite")

		cur = con.cursor()
		cur.execute(f"SELECT ID, CODE, SEMESTER, NAME FROM COURSES WHERE NAME LIKE '%{term}%'")
		rows = cur.fetchall()

		con.close()
		return rows

class User:
	def get_user(sid):
		con = sqlite3.connect("webcms4.sqlite")

		cur = con.cursor()
		cur.execute(f"SELECT SID, NAME, IMAGE, BIO FROM USERS WHERE SID = '{sid}'")
		row = cur.fetchone()

		con.close()
		return row

	def check_creds(sid, password):
		con = sqlite3.connect("webcms4.sqlite")

		cur = con.cursor()
		cur.execute(f"SELECT * FROM USERS WHERE SID = '{sid}' AND PASSWORD = '{password}'")
		valid = cur.fetchone() is not None

		con.close()

		return valid

	def update_image(sid, image):
		con = sqlite3.connect("webcms4.sqlite")

		cur = con.cursor()
		cur.execute(f"UPDATE USERS SET IMAGE = '{image}' WHERE SID = '{sid}'")

		con.commit()
		con.close()

		return True

	def update_bio(sid, bio):
		con = sqlite3.connect("webcms4.sqlite")

		cur = con.cursor()
		cur.execute(f"UPDATE USERS SET BIO = ? WHERE SID = ?", (bio, sid))

		con.commit()
		con.close()

		return True

