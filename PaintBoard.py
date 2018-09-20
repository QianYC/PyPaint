from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog
from Entity import Picture
import pickle

class PaintBoard(QWidget):
	def __init__(self,parent=None):
		super().__init__(parent)

		self.__size=QSize(500,400)
		self.__board=QPixmap(self.__size)
		self.__pixPainter=QPainter(self.__board)
		self.__board.fill(Qt.white)
		self.setFixedSize(self.__size)
		self.setMouseTracking(False)
		self.points = []
		self.__picture=Picture()


	def buttonClicked(self):
		sender=self.sender()
		print(sender.text())

	def clear(self):
		self.points=[]
		self.__board.fill(Qt.white)
		self.repaint()

	def paintEvent(self, QPaintEvent):
		painter = QPainter(self.__board)
		painter.begin(self)
		pen = QPen(Qt.black, 2, Qt.SolidLine)
		painter.setPen(pen)
		self.draw(painter)
		painter.end()

	def draw(self,painter):
		self.__pixPainter.begin(self)
		self.__pixPainter.drawPixmap(0,0,self.__board)
		self.__pixPainter.end()

		p1=[-1,-1]
		for point in self.points:
			if point==[-1,-1]:
				p1=[-1,-1]
				continue
			else:
				if p1==[-1,-1]:
					p1=point
					continue
				else:
					p2=point
					painter.drawLine(p1[0],p1[1],p2[0],p2[1])
					p1=p2

	def mousePressEvent(self, QMouseEvent):
		self.__painting=True
		self.update()

	def mouseMoveEvent(self, QMouseEvent):
		if self.__painting:
			x = QMouseEvent.pos().x()
			y = QMouseEvent.pos().y()
			self.points.append([x, y])
			self.update()

	def mouseReleaseEvent(self, QMouseEvent):
		self.points.append([-1,-1])
		print(self.points)
		self.update()
		# 每松一次鼠标就暂存一下画板内容
		raw = self.__board.toImage()
		self.__picture.setRawPicture(raw)

	def save(self):
		path=QFileDialog.getSaveFileName(self,'保存你的画作','.\\','*.jpg;;*.pic')
		if path[1]=="*.jpg":
			image=self.__board.toImage()
			image.save(path[0])
		elif path[1]=='*.pic':
			with open(path[0],'wb')as f:
				pickle.dump(self.__picture,f)

	def load(self):
		path=QFileDialog.getOpenFileName(self,'选择一副画作打开','.\\','*.jpg;;*.pic')
		if path[1]=='*.jpg':
			pass
		elif path[1]=='*.pic':
			with open(path[0],'rb')as f:
				self.__picture=pickle.load(f)
				print(self.__picture)

