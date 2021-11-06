from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import *
import sys

database_link = 'database.db' #must be same working directory

class Table(QTableWidget):
	"""a table"""
	def __init__(self, *args, con, **kwargs):
		super(Table, self).__init__(*args, **kwargs)
		self.con = con
		self.create_table ()


	def create_table(self):
		self.headers = ['icon', 'serial', 'quantity', 'price', 'category']
		self.setColumnCount (len (self.headers))
		self.setHorizontalHeaderLabels (self.headers)
		#TODO: import data from database
		tcontent = self.get_table_from_database ()
		self.fill_table (tcontent)		
		print (self.rowCount())

		self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.resizeRowsToContents()


	def fill_table (self, listdata):
		columns = len (self.headers)
		rows = len (listdata)
		self.setRowCount(rows)
		r = 0
		for row in listdata:
			print (row)
			img = QPixmap ("00775576.jpg")
			l = QLabel ()
			l.setPixmap(img)
			self.setCellWidget (r, 0,l)
			self.setItem (r, 1, QTableWidgetItem (row [0]))
			self.setItem (r, 2, QTableWidgetItem (str (row [2])))
			self.setItem (r, 3, QTableWidgetItem (str (row [3])))
			self.setItem (r, 4, QTableWidgetItem (row [4]))

			r += 1


	def get_table_from_database (self):
		t = get_table (self.con)
		return t

class List (QWidget):
	def __init__(self, *args,con,  **kwargs):
		super (List, self).__init__(*args, **kwargs)
		self.con = con
		vlay = QVBoxLayout ()

		sw = self.get_search_w ()

		self.t = Table (con=self.con)	#create self.t in place
		vlay.addWidget (sw)
		vlay.addWidget (self.t)

		self.setLayout(vlay)


	def get_search_w (self):
		l = QLabel ("Search: ")
		lb = QLineEdit ()
		criteria = QComboBox ()
		criteria.insertItems (0, ['name', 'serial'])

		butt = QPushButton ("search")

		hlay = QHBoxLayout ()
		hlay.addWidget (l)
		hlay.addWidget (lb)
		hlay.addWidget (criteria)
		hlay.addWidget (butt)#connect it to something that look for stuff, problem for a future me lol
		ww = QWidget ()
		ww.setLayout (hlay)
		return ww

class MainWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.connect_to_database ()
		self.set_dimension ()
		self._createMenuBar ()
		self.set_central_widget ()


	def set_dimension (self):
		self.setWindowTitle("Listing")
		self.setGeometry(100, 100, 700, 600)

	def set_central_widget (self):
		self.setCentralWidget(self.switcheroo ())

	def main_search (self):
		w = QWidget ()
		vlay = QVBoxLayout ()
		hlay = QHBoxLayout ()

		butt = QPushButton ("Search")
		butt.clicked.connect (lambda : self.stack.setCurrentIndex(1))

		line = QLineEdit ("Search")

		hlay.addWidget (line)
		hlay.addWidget (butt)

		ww = QWidget ()
		ww.setLayout (hlay)

		vlay.addWidget (ww)
		w.setLayout(vlay)
		return w
		
	def switcheroo(self):
		#is in charge of chaging between widgets. One is the main searchy one and the other is the list
		self.stack = QStackedWidget ()

		ms = self.main_search ()
		ms.resize(40, 200)
		self.stack.addWidget (ms)


		st = List (con=self.con)
		self.stack.addWidget (st)

		return self.stack

	def _createMenuBar (self):
		menu = self.menuBar ()
		file = menu.addMenu("&File")
		_import = file.addMenu ('&Import')
		_import.addAction ("Excel")
		_import.addAction ("Csv")
		
		_export = file.addMenu ('&Export')
		_export.addAction ("Excel")
		_export.addAction ("Csv")


		database_sittings = menu.addMenu("&Database")



	def connect_to_database (self):
		self.con = create_connection (database_link)


if __name__ =='__main__':

	app = QApplication ([])
	window = MainWindow()
	window.show()

	sys.exit (app.exec ())