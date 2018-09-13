import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QHBoxLayout, QVBoxLayout,QLineEdit
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPainter, QPen


class PaintBoard(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		self.setMouseTracking(False)
		# 点集
		self.points = []

	def initUI(self):

		quickBtn = QPushButton('退出画板', self)
		quickBtn.clicked.connect(QCoreApplication.instance().quit)
		formatBtn = QPushButton('识别并格式化', self)
		formatBtn.clicked.connect(self.buttonClicked)
		saveBtn = QPushButton('保存', self)
		loadBtn = QPushButton('载入', self)
		clearBtn = QPushButton('清空', self)
		clearBtn.clicked.connect(self.clear)


		input=QLineEdit()

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(input)
		hbox.addWidget(formatBtn)
		hbox.addWidget(saveBtn)
		hbox.addWidget(loadBtn)
		hbox.addWidget(clearBtn)
		hbox.addWidget(quickBtn)

		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

		self.setGeometry(100, 100, 400, 300)
		self.moveToCenter()

		self.setWindowTitle('PyPaint')
		self.show()

	def buttonClicked(self):
		sender=self.sender()
		print(sender.text())

	def clear(self):
		self.points=[]
		self.repaint()

	# 使界面居中
	def moveToCenter(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def closeEvent(self, QCloseEvent):
		reply = QMessageBox.question(self, 'Message', 'want to quit?',
		                             QMessageBox.Yes | QMessageBox.No,
		                             QMessageBox.No)
		if reply == QMessageBox.Yes:
			QCloseEvent.accept()
		else:
			QCloseEvent.ignore()

	def paintEvent(self, QPaintEvent):
		painter = QPainter()
		painter.begin(self)
		pen = QPen(Qt.black, 1, Qt.SolidLine)
		painter.setPen(pen)

		self.draw(painter)

		painter.end()

	def draw(self,painter):
		points2draw=[]
		for point in self.points:
			if point!=[-1,-1]:
				points2draw.append(point)
				if len(points2draw)>1:
					for i in range(len(points2draw)-1):
						p1=points2draw[i]
						p2=points2draw[i+1]
						painter.drawLine(p1[0],p1[1],p2[0],p2[1])
			else:
				points2draw=[]




	def mousePressEvent(self, QMouseEvent):
		print('mouse clicked')
		x=QMouseEvent.pos().x()
		y=QMouseEvent.pos().y()
		self.points.append([x,y])

		self.repaint()


	def mouseMoveEvent(self, QMouseEvent):
		x = QMouseEvent.pos().x()
		y = QMouseEvent.pos().y()
		self.points.append([x, y])
		self.repaint()

	def mouseReleaseEvent(self, QMouseEvent):
		self.points.append([-1,-1])
		print(self.points)
		self.repaint()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	paintBoard = PaintBoard()
	sys.exit(app.exec_())
