import cv2
import numpy as np


def gDetect(path):
	img=cv2.imread(path)
	# 生成一个空白图像
	newImg=np.zeros(img.shape,np.uint8)
	newImg[...]=255
	try:
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		'''
		ret其实就是阈值
		thresh则是二值化的图像
		'''
		ret, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)
		'''
		image其实就是thresh
		contours是轮廓的点集
		hierarchy
		'''
		image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for cnt in contours:
			epsilon = 0.03 * cv2.arcLength(cnt, True)
			approx = cv2.approxPolyDP(cnt, epsilon, True)
			# for point in approx:
			# 	cv2.circle(img, (point[0][0], point[0][1]), 4, (255, 0, 0), 1)

			if len(approx) == 3:
				print('triangle')
				drawTriangle(approx, newImg)
			elif len(approx) == 4:
				drawRectangle(cnt, newImg)
			elif len(approx) > 4:
				print('circle')
				drawCircle(cnt, newImg)


		cv2.imwrite(path,newImg)
		# cv2.imshow('newImg',newImg)
		# cv2.waitKey(0)
	except:
		print('img does not exists!')
		return None

# 画三角形只需要两两相连即可
def drawTriangle(points,img):
	print(points)
	cv2.line(img,(points[0][0][0],points[0][0][1]),(points[1][0][0],points[1][0][1]),(0,0,255),2)
	cv2.line(img,(points[0][0][0],points[0][0][1]),(points[2][0][0],points[2][0][1]),(0,0,255),2)
	cv2.line(img,(points[2][0][0],points[2][0][1]),(points[1][0][0],points[1][0][1]),(0,0,255),2)

	pos=(int((points[0][0][0]+points[1][0][0]+points[2][0][0])/3),
	        int((points[0][0][1]+points[1][0][1]+points[2][0][1])/3))
	cv2.putText(img,'Triangle',pos,cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

# 画最小外接矩形
def drawRectangle(points,img):
	rect = cv2.minAreaRect(points)
	(x,y)=rect[0]
	pos=(int(x),int(y))
	print('pos = ',pos)
	width=rect[1][0]
	height=rect[1][1]
	res = cv2.boxPoints(rect)
	res = np.int0(res)
	cv2.drawContours(img,[res],-1,(0,0,255),2)
	text=''
	# 矩形的长宽差距小于一定范围就认定为正方形
	if np.abs(width-height)/width<=0.1 and np.abs(width-height)/height<0.1:
		text='Square'
	else:
		text='Rectangle'
	cv2.putText(img,text,pos,cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

# 画最小外接圆
def drawCircle(points,img):
	(x,y),r=cv2.minEnclosingCircle(points)
	center=(int(x),int(y))
	r=int(r)
	cv2.circle(img,center,r,(0,0,255),2)
	cv2.putText(img,'Circle',center,cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)