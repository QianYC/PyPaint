from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QPixmap


class Picture():
	def __init__(self):
		self.__tags=""
		self.__qpixmap={}

	def getRawPicture(self):
		return self.__qpixmap.get('raw')
	def getGeneratedPicture(self):
		return self.__qpixmap.get('generated')
	def getTags(self):
		return self.__tags

	def setRawPicture(self,pic):
		self.__qpixmap['raw']=pic
	def setGeneratedPicture(self,pic):
		self.__qpixmap['generated']=pic
	def setTags(self,tags):
		self.__tags=tags

	# 以下两个方法定义了Picture对象在序列化的行为
	# 详情见https://docs.python.org/2/library/pickle.html#what-can-be-pickled-and-unpickled
	def __getstate__(self):
		state=[]
		for key,value in self.__qpixmap.items():
			bytearray=QByteArray()
			stream=QDataStream(bytearray,QIODevice.WriteOnly)
			stream<<value
			state.append((key,bytearray))
		state.append(('tags',self.__tags))
		return state

	def __setstate__(self, state):
		self.__qpixmap={}
		for (key,buffer)in state:
			if key=='tags':
				self.__tags=buffer
			else:
				pmap=QPixmap()
				stream=QDataStream(buffer,QIODevice.ReadOnly)
				stream>>pmap
				self.__qpixmap[key]=pmap
