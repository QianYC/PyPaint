import sys
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

		label=QLabel()
		label.setText('标记输入框')
		input=QLineEdit()
		# drawBtn=QPushButton('画图',self)

		formatBtn = QPushButton('识别并格式化', self)
		saveBtn = QPushButton('保存', self)
		saveBtn.clicked.connect(self.save)
		loadBtn = QPushButton('载入', self)
		loadBtn.clicked.connect(self.__paintBoard.load)
		clearBtn = QPushButton('清空', self)
		clearBtn.clicked.connect(self.__paintBoard.clear)
		subLayer.addWidget(label)
		subLayer.addWidget(input)
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

	def save(self):
		self.__paintBoard.save()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	paintBoard = MainUI()
	sys.exit(app.exec_())
