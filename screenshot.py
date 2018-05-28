
from PIL import Image
import cv2
import win32gui, win32ui, win32con


class ScreenShot():

	def __init__(self, loc):
		self.left_top_x = loc['left_top_x']
		self.left_top_y = loc['left_top_y']
		self.right_buttom_x = loc['right_buttom_x']
		self.right_buttom_y = loc['right_buttom_y']

		self.w = self.right_buttom_x - self.left_top_x
		self.h = self.right_buttom_y - self.left_top_y

		self.hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
		self.hwndDC = win32gui.GetWindowDC(self.hwnd)
		# 根据窗口的DC获取mfcDC
		self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
		# mfcDC创建可兼容的DC
		self.saveDC = self.mfcDC.CreateCompatibleDC()
		# 创建bigmap准备保存图片
		self.saveBitMap = win32ui.CreateBitmap()
		# 为bitmap开辟空间
		self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)

	def shotByWinAPI(self, filename):
		"""使用windows原生API截屏，快的一匹"""
		w = self.w
		h = self.h

		mfcDC = self.mfcDC 
		saveDC = self.saveDC
		saveBitMap = self.saveBitMap


		# 高度saveDC，将截图保存到saveBitmap中
		oldbmp = saveDC.SelectObject(saveBitMap)
		# 截取从左上角（0，0）长宽为（w，h）的图片
		saveDC.BitBlt((0, 0), (w, h), mfcDC, (self.left_top_x, self.left_top_y), win32con.SRCCOPY)
		saveBitMap.SaveBitmapFile(saveDC, filename)
		img = cv2.imread(filename, 0)
		#img = Image.open(filename)

		#saveDC.SelectObject(oldbmp)
		#win32gui.DeleteObject(saveBitMap.GetHandle())
		#saveDC.DeleteDC()
		#win32gui.ReleaseDC(hwnd, hwndDC)
		return img