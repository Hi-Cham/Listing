import sqlite3
from sqlite3 import Error
import os
import pandas as pd
import csv, os

'''
[fun]	create_connection
[fun]	create_table
[fun]	bimg
[fun]	insert_row
[fun]	update_row
[fun]	search_for
[fun]	get_table

'''
headers =  ['Reference', 'Description', 'Quantity', 'Price', 'Category', 'Datasheet']


def create_connection(f):
    conn = None;
    try:
        conn = sqlite3.connect(f)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    finally:
        if not conn:
            conn.close()

def create_table (con, table):
	cur = con.cursor()
	try:
		cur.execute (table)
		con.commit()
	except Error as e:
		print (e)

def bimg (imgf):
	
	with open (imgf, 'rb') as mf:
		b = mf.read()
	return b

def insert_row (con, info):
	#headers =  ['Reference', 'Description', 'Quantity', 'Price', 'Category', 'Datasheet']
	infov = []
	for tite in headers:
		infov.append (info [tite])
	ins = '''
	INSERT INTO listing(Reference, Description, Quantity, Price, Category, Datasheet) VALUES(?, ?, ?, ?, ?, ?)'''
	cur = con.cursor ()
	try:
		cur.execute (ins, infov)
	except Error as e:
		print (e)
	con.commit ()
	return infov
def update_row (con, infodict):
	to_update = '\n'
	val=[]
	keys = [k for k in infodict if k != 'id']
	for k in keys:
		if 'icon' == k:
			infodict ['icon'] = bimg (infodict ['icon'])
		to_update += f'{k}=?\n'
		val.append(infodict [k])

	sql = f'''
	UPDATE listing
	set {to_update}
	WHERE id=?
	'''
	cur = con.cursor ()
	try:
		cur.execute (sql, val + [infodict ['id'], ])
		print ('line edited')
		con.commit ()
	except Error as e:
		print (e)

def search_for (con, infodict):
	cur = con.cursor ()
	sql = '''SELECT * FROM listing 
	WHERE '''
	keys = [k for k in infodict.keys ()]
	c = 1
	for k in keys:
		sql += f'{k} = "{infodict [k]}"'
		if len (keys) > c:
			sql += ', \n'
		c += 1
	try:
		cur.execute (sql)
		res = cur.fetchall ()
		print (res)
	except Error as e:
		raise Exception (e)

def get_table (con):
	cur = con.cursor ()
	sql = '''SELECT * FROM listing'''
	try:
		cur.execute (sql)
	except Error as e:
		print (e)
	return cur.fetchall ()

def import_csv_d (con, f):
	csvf = pd.read_csv (f)
	csvf.to_sql ('listing', con, if_exists='append', index=False)

def import_excel_d (con, f):
	excelf = pd.read_excel (f)
	excelf.to_csv ('listing.csv', index=None, headers=False)
	import_csv (con, os.path.join (os.getcwd (), 'listing.csv'))

def export_csv_d (con, save_to):
	cur = con.cursor ()
	tabl = cur.execute ('SELECT * FROM listing').fetchall ()
	with open (os.path.join (save_to, 'listing.csv'), 'w') as vf:
		writer = csv.writer (vf)
		writer.writerows (tabl)
	return os.path.join (save_to, 'listing.csv')


def export_excel_d (con, f):
	cur = con.cursor ()
	tabl = cur.execute ('SELECT * FROM listing').fetchall ()
	df = pd.DataFrame(tabl)
	writer = pd.ExcelWriter(os.path.join (f, 'listing.xlsx'), engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Listing', index=False)
	writer.save()
_name__ = '__main__'
if __name__ == '__main__':
	con = create_connection ("database.db")

	t = """
		CREATE TABLE IF NOT EXISTS listing (
			Reference text PRIMARY KEY,
			Description text,			
			Quantity integer,
			Price integer,
			Category text NOT NULL,
			Datasheet text
		);

		"""
	create_table (con, t)
