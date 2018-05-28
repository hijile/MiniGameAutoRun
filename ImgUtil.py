
import cv2
import numpy as np
import os
import pickle
from TimeIt import time_it

class ImgUtil():
	def __init__(self):
		pass

	def binaryImg(self, img):
		"""二值化图片"""
		ret, thresh1 = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
		# ret, thresh1 = cv2.threshold(img, config.config['binary_threshold'], 255, cv2.THRESH_BINARY_INV)
		#print('二值化完毕')
		thresh1[thresh1 == 0] = 1
		thresh1[thresh1 == 255] = 0
		return thresh1

	def vertical_cut(self, img):
		"""纵向切割"""
		_, height = img.shape
		px = list(np.sum(np.array(img) == 0, axis=0))
		# 列表保存像素累加值大于0的列
		x0 = []
		for x in range(len(px)):
			if px[x] > 1:
				x0.append(x)

		# 找出边界
		cut_list = [x0[0]]
		for i in range(1, len(x0)):
			if abs(x0[i] - x0[i - 1]) > 1:
				cut_list.extend([x0[i - 1], x0[i]])
		cut_list.append(x0[-1])

		cut_imgs = []
		# 切割顺利的话应该是整对
		if len(cut_list) % 2 == 0:
			for i in range(len(cut_list) // 2):
				cut_img = img[:, cut_list[i * 2]:cut_list[i * 2 + 1]]
				h, w = cut_img.shape
				#print(w, h)
				if w > 60:
					cut_img1 = cut_img[:, 0:w //2]
					cut_img2 = cut_img[:, w //2:]
					cut_imgs.append(cut_img1)
					cut_imgs.append(cut_img2)
				else:
					cut_imgs.append(cut_img)
			return cut_imgs
		else:
			print('Vertical cut failed.')
			return

	def horizontal_cut(self, img):
		"""横向切割"""
		#width, _ = img.shape
		#print(img.shape)
		px = list(np.sum(np.array(img) == 0, axis=1))
		#print(px)
		# 列表保存像素累加值大于0的行
		y0 = []
		for y in range(len(px)):
			if px[y] > 1:
				y0.append(y)

		# 找出边界
		cut_list = [y0[0]]
		for i in range(1, len(y0)):
			if abs(y0[i] - y0[i - 1]) > 1:
				cut_list.extend([y0[i - 1], y0[i]])
		cut_list.append(y0[-1])

		# 切割顺利的话应该是长度为4的list
		if len(cut_list) == 4:
			#cut_img1 = img.crop([0, cut_list[0], width, cut_list[1]])
			#cut_img2 = img.crop([0, cut_list[2], width, cut_list[3]])
			cut_img1 = img[cut_list[0]:cut_list[1], 0:]
			cut_img2 = img[cut_list[2]:cut_list[3], 0:]
			return [cut_img1, cut_img2]
		else:
			print('Horizontal cut failed.')
			return

	def getOneChar(self, lr, img):
		img = cv2.resize(img, (20, 30), interpolation=cv2.INTER_CUBIC)
		#img = img.resize((20, 30), Image.LANCZOS).convert("L")
		img = np.array(img).reshape(1, -1)
		#img[img == 255] = 1
		y_hat = lr.predict(img)[0]
		if y_hat == 10:
			y_hat = '+'
		elif y_hat == 11:
			y_hat = '-'
		elif y_hat == 12:
			y_hat = '=='
		else:
			y_hat = str(y_hat)
		return y_hat

	@time_it
	def recognize(self, lr, img):
		"""输入：经过裁剪的含有等式的区域图像"""
		#img = img.convert('L')
		img = self.binaryImg(img)
		#print(type(img))
		#print(img)

		h_cut_imgs = self.horizontal_cut(img)

		chars1 = self.vertical_cut(h_cut_imgs[0])
		chars2 = self.vertical_cut(h_cut_imgs[1])

		expr = ''
		for char in chars1:
			expr += self.getOneChar(lr, char)
			#print(y_hat)

		for char in chars2:
			expr += self.getOneChar(lr, char)

		return expr

if __name__ == '__main__':
    """
    以下代码只用于debug
    """
    with open('lr.pickle', 'rb') as fr:
        lr = pickle.load(fr)

    ImgUtil = ImgUtil()
    scr = cv2.imread('Screenshots\screenshot.png', 0)
    expr = ImgUtil.recognize(lr, scr)
    print(expr)