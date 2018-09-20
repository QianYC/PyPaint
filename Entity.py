class Picture():
	def __init__(self):
		self.__rawPicture=None
		self.__generatedPicture=None
		self.__tags=None

	def getRawPicture(self):
		return self.__rawPicture
	def getGeneratedPicture(self):
		return self.__generatedPicture
	def getTags(self):
		return self.__tags
	def setRawPicture(self,pic):
		self.__rawPicture=pic
	def setGeneratedPicture(self,pic):
		self.__generatedPicture=pic
	def setTags(self,tags):
		self.__tags=tags
