import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, \
	QLabel, QMessageBox
from PaintBoard import PaintBoard

class MainUI(QWidget):
	def __init__(self):
		super().__init__()
		self.__initUI()


	def __initUI(self):
		self.resize(600,450)
		self.setWindowTitle('PyPaint')
		self.moveToCenter()
		self.__paintBoard=PaintBoard(self)

		mainLayer=QHBoxLayout()
		mainLayer.setSpacing(10)
		mainLayer.addWidget(self.__paintBoard)

		subLayer=QVBoxLayout()
		subLayer.setContentsMargins(10,10,10,10)

		self.__label=QLabel()
		self.__label.setText('标记输入框')
		self.__input=QLineEdit()
		self.__viewRaw=False

		formatBtn = QPushButton('查看规范图像', self)
		formatBtn.clicked.connect(self.viewPicture)
		saveBtn = QPushButton('保存', self)
		saveBtn.clicked.connect(self.__paintBoard.save)
		loadBtn = QPushButton('载入', self)
		loadBtn.clicked.connect(self.__paintBoard.load)
		clearBtn = QPushButton('清空', self)
		clearBtn.clicked.connect(self.clear)
		subLayer.addWidget(self.__label)
		subLayer.addWidget(self.__input)
		subLayer.addWidget(formatBtn)
		subLayer.addWidget(saveBtn)
		subLayer.addWidget(loadBtn)
		subLayer.addWidget(clearBtn)
		mainLayer.addLayout(subLayer)
		self.setLayout(mainLayer)
		self.show()

	# 使界面居中
	def moveToCenter(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def updateText(self,text):
		self.__label.setText(text)

	def keyPressEvent(self, QKeyEvent):
		if QKeyEvent.key()==Qt.Key_Return and self.__input.hasFocus():
			text=self.__input.text()
			self.__paintBoard.updateTag(text)
			self.__label.setText(text)

	def clear(self):
		self.__paintBoard.clear()
		self.__input.setText('')

	def viewPicture(self):
		sender=self.sender()
		if self.__viewRaw:
			self.__viewRaw=False
			sender.setText('查看规范图像')
			self.__paintBoard.viewRaw()
		else:
			self.__viewRaw=True
			sender.setText('查看原图')
			self.__paintBoard.viewFormalized()
		pass


if __name__ == "__main__":
	app = QApplication(sys.argv)
	paintBoard = MainUI()
	sys.exit(app.exec_())
