import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QFileDialog, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from try4 import *  


class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = 'Face Recognition Base Attendence'
		self.left = 0
		self.top = 0
		self.width = 300
		self.height = 200
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		

		self.table_widget = MyTableWidget(self)
		self.setCentralWidget(self.table_widget)

		self.show()

class MyTableWidget(QWidget):

	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)
		# self.statusBar().showMessage('ghgh')
		# Initialize tab screen
		self.tabs = QTabWidget()
		self.tab1 = QWidget()
		self.tab2 = QWidget()
		self.tabs.resize(300, 200)

		# Add tabs
		self.tabs.addTab(self.tab1, "Attendence")
		self.tabs.addTab(self.tab2, "Manage")

		# Create first tab
		self.tab1.layout = QVBoxLayout(self)
		self.recordButton = QPushButton("Record")
		self.tab1.layout.addWidget(self.recordButton)
		self.recordButton.clicked.connect(self.on_recordClick)

		self.openAttendenceButton = QPushButton("Open Attendence")
		self.tab1.layout.addWidget(self.openAttendenceButton)
		self.openAttendenceButton.clicked.connect(self.on_openAttendenceClick)
		self.tab1.setLayout(self.tab1.layout)

		# Create 2nd tab
		self.tab2.layout = QVBoxLayout(self)

		
		self.nameTextbox = QLineEdit(self)
		self.nameTextbox.setPlaceholderText("Enter Student Name Here..")
		self.tab2.layout.addWidget(self.nameTextbox)
		

		self.rollNoTextbox = QLineEdit(self)
		self.rollNoTextbox.setPlaceholderText("Enter Student RollNo Here..")
		self.tab2.layout.addWidget(self.rollNoTextbox)

		self.fileTextbox = QLineEdit(self)
		self.fileTextbox.setPlaceholderText("Your image path will appear here....")
		self.tab2.layout.addWidget(self.fileTextbox)
		
		self.browseButton = QPushButton("Browse")
		self.tab2.layout.addWidget(self.browseButton)
		self.browseButton.clicked.connect(self.on_browseClick)

		label = QLabel(self)
		pixmap = QPixmap("default.jpeg")
		label.setPixmap(pixmap)
		self.resize(pixmap.width(), pixmap.height())

		self.uploadButton = QPushButton("Upload")
		self.tab2.layout.addWidget(self.uploadButton)
		self.uploadButton.clicked.connect(self.on_uploadClick)

		self.tab2.setLayout(self.tab2.layout)

		# Add tabs to widget
		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)

	@pyqtSlot()
	def on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(),
				  currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

	@pyqtSlot()
	def on_recordClick(self):
		recognize()

	@pyqtSlot()
	def on_openAttendenceClick(self):
		openAttendence()
		self.statusBar.showMessage("done")

	@pyqtSlot()
	def on_browseClick(self):
		filename = QFileDialog.getOpenFileName(
			parent=self, caption='Select Student Photo To Upload', directory=',', filter="*.jpg")
		# self.statusBar().showMessage(filename)
		self.fileTextbox.setText(filename[0])
		

	@pyqtSlot()
	def on_uploadClick(self):
		# (parent=self, caption='Select Student Photo To Upload', directory=',',filter="*.jpg")
		# filename2 = QFileDialog.getOpenFileName(parent=self, caption='Select Student Photo To Upload',
		# 										directory=',C:\\Users\\madMax\\Desktop\\DlibFaceRecognition\\Students', filter="*.jpg")
		filename=self.fileTextbox.text()
		userName=self.nameTextbox.text()
		userRollNo=self.rollNoTextbox.text()
		# test2(userName,userRollNo)
		copyImage(filename,userName,userRollNo)	
		# test2(filename2[0])


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
