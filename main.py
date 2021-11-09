from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import *
from add_item_dialog import *
import sys

database_link = 'database.db' #must be same working directory
headers =  ['Reference', 'Description', 'Quantity', 'Price', 'Category', 'Datasheet']
categories = ['Analog IC', 'Arduino', 'Bluetooth', 'Capacitors', 'Diodes', 'Inductor', 'IC', 'Mechanical', 'Microprocessor',
 'Operational Amplifiers', 'Optoelectronics', 'PIC', 'Resistors', 'Sound', 'Transducers', 'Transistors']


class Table(QTableWidget):
	"""a table"""
	def __init__(self, *args, con, headers, categories=categories, **kwargs):
		super(Table, self).__init__(*args, **kwargs)
		self.con = con
		self.headers = headers
		self.categories = categories
		self.create_table ()


	def create_table(self):
		#['icon', 'serial', 'quantity', 'price', 'category']
		#['Reference', 'Description', 'Quantity', 'Price', 'Category', 'Datasheet']
		self.setColumnCount (len (self.headers))
		self.setHorizontalHeaderLabels (self.headers)
		#TODO: import data from database
		tcontent = self.get_table_from_database ()
		self.fill_table (tcontent)		

		self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.resizeRowsToContents()


	def add_row_to_end_table (self, row):
		r = self.rowCount() + 1
		self.setItem (r, 0, QTableWidgetItem (str (row [0])))	#ref
		self.setItem (r, 1, QTableWidgetItem (str (row [1])))	#des
		self.setItem (r, 2, QTableWidgetItem (str (row [2])))	#quan
		self.setItem (r, 3, QTableWidgetItem (str (row [3])))	#pri
		cat = QComboBox ()
		cat.addItems (self.categories)
		i = cat.findText(row [4])
		cat.setCurrentIndex(i)
		self.setCellWidget (r, 4, cat)	#cat
		self.setItem (r, 5, QTableWidgetItem (str (row [5])))	#dat


	def fill_table (self, listdata):
		columns = len (self.headers)
		rows = len (listdata)
		self.setRowCount(rows)
		r = 0
		for row in listdata:
			self.setItem (r, 0, QTableWidgetItem (str (row [0])))	#ref
			self.setItem (r, 1, QTableWidgetItem (str (row [1])))	#des
			self.setItem (r, 2, QTableWidgetItem (str (row [2])))	#quan
			self.setItem (r, 3, QTableWidgetItem (str (row [3])))	#pri
			cat = QComboBox ()
			cat.addItems (self.categories)
			i = cat.findText(row [4])
			cat.setCurrentIndex(i)
			self.setCellWidget (r, 4, cat)	#cat
			self.setItem (r, 5, QTableWidgetItem (str (row [5])))	#dat


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

		self.t = Table (con=self.con, headers=headers)	#create self.t in place
		vlay.addWidget (sw)
		vlay.addWidget (self.t)

		self.setLayout(vlay)

	def add_new_item (self):
		d = new_item ()
		d.exec ()
		info = insert_row (self.con, d.result())
		self.t.fill_table (get_table (self.con))

	def get_search_w (self):
		l = QLabel ("Search: ")
		lb = QLineEdit ()
		new_item = QPushButton ("Add row")
		new_item.clicked.connect (self.add_new_item)
		criteria = QComboBox ()
		criteria.insertItems (0, ['name', 'serial'])

		butt = QPushButton ("search")

		hlay = QHBoxLayout ()
		hlay.addWidget (l)
		hlay.addWidget (lb)
		hlay.addWidget (criteria)
		hlay.addWidget (butt)#connect it to something that look for stuff, problem for a future me lol
		hlay.addWidget (new_item)
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

		line = QLineEdit ()
		line.setPlaceholderText("Search")

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
		
		imp_excel = _import.addAction ("Excel")
		imp_excel.triggered.connect (self.import_excel)

		imp_csv = _import.addAction ("Csv")
		imp_csv.triggered.connect (self.import_csv)

		
		_export = file.addMenu ('&Export')
		exp_excel = _export.addAction ("Excel")
		exp_excel.triggered.connect (self.export_excel)

		exp_csv = _export.addAction ("Csv")
		exp_csv.triggered.connect (self.export_csv)


		database_settings = menu.addMenu("&Database")
		del_db = database_settings.addAction ("Delete ")


		themes = menu.addMenu ("&Themes")
		language = menu.addMenu ("&Language")

	def import_excel (self):
		d = QFileDialog.getOpenFileName(self,  "Open excel", "C:", "Excel Files (*.xlsx)")
		import_excel_d (self.con, d)

	def import_csv (self):
		d = QFileDialog.getOpenFileName(self,  "Open excel", "C:", "Csv files (*.csv)")
		import_csv_d (self.con, d)
		
	def export_excel (self):
		d = QFileDialog.getExistingDirectory(self,  "Save excel", "C:")
		export_excel_d (self.con, d)

	def export_csv (self):
		d = QFileDialog.getExistingDirectory(self,  "Save excel", "C:")
		export_csv_d (self.con, d)



	def connect_to_database (self):
		self.con = create_connection (database_link)


if __name__ =='__main__':

	app = QApplication ([])
	window = MainWindow()
	window.show()

	sys.exit (app.exec ())