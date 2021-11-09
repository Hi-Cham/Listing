from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

#headers =  ['Reference', 'Description', 'Quantity', 'Price', 'Category', 'Datasheet']
categories = ['Analog IC', 'Arduino', 'Bluetooth', 'Capacitors', 'Diodes', 'Inductor', 'IC', 'Mechanical', 'Microprocessor',
 'Operational Amplifiers', 'Optoelectronics', 'PIC', 'Resistors', 'Sound', 'Transducers', 'Transistors']

class new_item(QDialog):
	"""a dialog that does not speak, a window that shows inside, what am i?"""
	def __init__(self, *args, **kwargs):
		super(new_item, self).__init__()
		self.lines = {}
		self.setModal(True)
		vlay = QVBoxLayout ()

		iw = self.get_insertion_widget_or_values ()
		bhw = self.get_ok_cancel_butts ()

		vlay.addWidget (iw)
		vlay.addWidget (bhw)

		self.setLayout (vlay)

	def get_ok_cancel_butts (self):
		bhlay, bhw = QHBoxLayout (), QWidget ()


		ok_butt = QPushButton ("Ok")
		ok_butt.clicked.connect (lambda: self.get_insertion_widget_or_values (insertion=False))

		cancel_butt = QPushButton ("Cancel")
		cancel_butt.clicked.connect (self.reject)


		bhlay.addWidget(ok_butt)
		bhlay.addWidget(cancel_butt)
		bhw.setLayout (bhlay)
		return bhw


	def get_price_w (self):
		
		w = QWidget ()
		w.setLayout (hlay)
		return w

	def cat_to_top (self, combo, line):
		text = line.text ()
		combo.insertItem (0, text)


	def get_insertion_widget_or_values (self, insertion=True):
		if insertion:
			iw = QWidget ()
			ihlay = QHBoxLayout ()
			ivlay = QVBoxLayout ()

			self.ref, self.dat = [QLineEdit (), QLineEdit ()]
			self.ref.setPlaceholderText ("Reference")
			self.dat.setPlaceholderText ("Datasheet link")

			self.des = QTextEdit ()
			self.des.setPlaceholderText ("Description")
			
			self.cat = QComboBox ()
			self.new_cat = QLineEdit ()
			self.new_cat.setPlaceholderText("...add category")
			self.new_cat.returnPressed.connect (lambda:self.cat_to_top (combo = cat, line = new_cat))
			#cat.setLineEdit(new_cat) TODO: make it so that only one line can be edited. This method makes all editable at once
			self.cat.addItems(categories)

			self.quan = QSpinBox ()

			self.pri = QSpinBox ()
			self.pri.setSuffix (" DZD")
			tw, ttw = [QWidget (), QWidget ()]
			ihlay.addWidget (self.ref)
			ihlay.addWidget (self.dat)
			ihlay.addWidget (self.quan)
			ihlay.addWidget (self.pri)
			ihlay.addWidget (self.cat)
			tw.setLayout (ihlay)
			ivlay.addWidget (tw)
			ivlay.addWidget (self.des)

			iw.setLayout (ivlay)
			return iw
		else:
			#headers =  ['Reference', 'Description', 'Quantity', 'Price', 'Category', 'Datasheet']
			self.lines ['Reference'] = self.ref.text ()
			self.lines ['Description'] = self.des.toPlainText ()
			self.lines ['Quantity'] = self.quan.value ()
			self.lines ['Price'] = self.pri.value ()
			self.lines ['Category'] = self.cat.currentText ()
			self.lines ['Datasheet'] = self.dat.text ()
			self.accept ()
			return self.lines 
	def result (self):
		return self.lines

#dialog.result () has the result