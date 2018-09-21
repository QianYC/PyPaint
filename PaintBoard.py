import pickle

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from Detector import gDetect
from Entity import Picture


class PaintBoard(QWidget):
	def __init__(self,parent=None):
		super().__init__(parent)

		self.__root=parent
		self.__size=QSize(500,400)
		self.__board=QPixmap(self.__size)
		self.__pixPainter=QPainter(self.__board)
		self.__board.fill(Qt.white)
		self.setFixedSize(self.__size)
		self.setMouseTracking(False)
		self.points = []
		self.__picture=Picture()

	def __changePixMap(self,pix):
		self.__board=pix
		self.__pixPainter = QPainter(self.__board)

	def clear(self):
		self.points=[]
		self.__board.fill(Qt.white)
		self.__root.updateText('')
		self.__picture=Picture()
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
		self.update()
		# 每松一次鼠标就暂存一下画板内容
		self.__picture.setRawPicture(self.__board)

	def save(self):
		path=QFileDialog.getSaveFileName(self,'保存你的画作','.\\','*.jpg;;*.pyp')
		if path[1]=="*.jpg":
			image=self.__board.save(path[0])
		elif path[1]=='*.pyp':
			with open(path[0],'wb')as f:
				pickle.dump(self.__picture,f)

	def load(self):
		path=QFileDialog.getOpenFileName(self,'选择一副画作打开','.\\','*.jpg;;*.pyp')
		self.clear()
		if path[1]=='*.jpg':
			self.__picture=Picture()
			self.__board.load(path[0])
			# self.__changePixMap(QPixmap(path[0]))
			self.__picture.setRawPicture(self.__board)
			self.repaint()
		elif path[1]=='*.pyp':
			with open(path[0],'rb')as f:
				self.__picture=pickle.load(f)
				# self.__changePixMap(self.__picture.getRawPicture())
				self.__board.copy(self.__picture.getRawPicture())
				self.__root.updateText(self.__picture.getTags())
				self.update()

	def updateTag(self,tag):
		self.__picture.setTags(tag)

	def formatPicture(self):
		pass

	def viewRaw(self):
		pix=self.__picture.getRawPicture()
		if pix==None:
			QMessageBox.warning(self,'注意','原图不存在！',QMessageBox.Yes,QMessageBox.Yes)
		else:
			# self.__changePixMap(pix)
			self.__board.fill()
			self.__board.fromImage(pix.toImage())
			self.update()
			pass

	def viewFormalized(self):
		pix=self.__picture.getGeneratedPicture()
		path='pypaint_temp.jpg'

		self.__board.save(path)
		gDetect(path)

		self.__board.fill()
		self.__board.load(path)
		self.__picture.setGeneratedPicture(self.__board)
		self.update()

