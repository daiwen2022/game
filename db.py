import sqlite3 as s
from bot import bot

def main(msg):
	with s.connect('db.db') as db:
		c = db.cursor()

		if msg.chat.title is None:
			c.execute('INSERT INTO ID(ID, user, persd) VALUES(?, ?, ?) ', (msg.chat.id, msg.chat.username, 'user'))

		else:
			c.execute('INSERT INTO ID(ID, user, persd) VALUES(?, ?, ?) ', (msg.chat.id, msg.chat.title, 'besed'))


def check(msg):
	with s.connect('db.db') as db:
		c= db.cursor()

		info = c.execute("SELECT * FROM ID WHERE ID = ?", (msg.chat.id, )).fetchone()
		return info

def addrep(msg, rep):
	with s.connect('db.db') as db:
		c = db.cursor()

		c.execute('UPDATE ID SET rep = rep + ? WHERE ID = ?', (rep, msg.chat.id, ))

def minusrep(msg, rep):
	with s.connect('db.db') as db:
		c = db.cursor()

		c.execute('UPDATE ID SET rep = rep - ? WHERE ID = ?', (rep, msg.chat.id, ))

def addgame(msg):
	with s.connect('db.db')  as db:
		c = db.cursor()

		c.execute('UPDATE ID SET games = games + 1 WHERE ID = ?', (msg.chat.id, ))

def all():
	with s.connect('db.db') as db:
		c = db.cursor()

		al = c.execute('SELECT * FROM ID WHERE persd = ? ORDER BY rep DESC', ('user', )).fetchall()

		return al

def allbesed():
	with s.connect('db.db') as db:
		c = db.cursor()

		al = c.execute('SELECT * FROM ID WHERE persd = ? ORDER BY rep DESC', ('besed', )).fetchall()

		return al
