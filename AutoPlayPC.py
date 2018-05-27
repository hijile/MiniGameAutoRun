from PIL import Image
from pymouse import PyMouse
from ImgTools import recognize,saveImages,recognize_new
from TimeIt import time_it
from Config import location_on_pc as loc
import os
import time
import sys
import traceback
import pickle
import win32gui, win32ui, win32con
from PIL import ImageGrab


hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
# 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
hwndDC = None
# 根据窗口的DC获取mfcDC
mfcDC = None
# mfcDC创建可兼容的DC
saveDC = None
# 创建bigmap准备保存图片
saveBitMap = None


def shotByWinAPI(filename):
    """使用windows原生API截屏，快的一匹"""
    w = loc['right_buttom_x'] - loc['left_top_x']
    h = loc['right_buttom_y'] - loc['left_top_y']

    global hwnd, hwndDC, mfcDC, saveDC, saveBitMap
    if not hwndDC :
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, loc['right_buttom_x'] - loc['left_top_x'], loc['right_buttom_y'] - loc['left_top_y'])
    
    # 高度saveDC，将截图保存到saveBitmap中
    oldbmp = saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (loc['left_top_x'], loc['left_top_y']), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    img = Image.open(filename)

    #saveDC.SelectObject(oldbmp)
    #win32gui.DeleteObject(saveBitMap.GetHandle())
    #saveDC.DeleteDC()
    #win32gui.ReleaseDC(hwnd, hwndDC)
    return img


@time_it
def get_screenshot(index):
    if sys.platform == 'win32':
        #print(loc['left_top_x'], loc['left_top_y'], loc['right_buttom_x'], loc['right_buttom_y'])
        #scr = ImageGrab.grab(
        #    [loc['left_top_x'], loc['left_top_y'], loc['right_buttom_x'], loc['right_buttom_y']])
        #scr.save('screenshot.png')
        scr = shotByWinAPI('Screenshots\screenshot%d.png' % index)
        return scr
    elif sys.platform == 'linux':
        command = 'import -window root -crop {0}x{1}+{2}+{3} screenshot.png'
        command = command.format(loc['right_buttom_x'] - loc['left_top_x'],
                                 loc['right_buttom_y'] - loc['left_top_y'],
                                 loc['left_top_x'],
                                 loc['left_top_y'])
        os.system(command)
        scr = Image.open('screenshot.png')
        return scr
    else:
        print('Unsupported platform: ', sys.platform)
        os._exit(0)


def Play():
    m = PyMouse()
    with open('lr.pickle', 'rb') as fr:
        lr = pickle.load(fr)
    flag = ""
    time.sleep(1)
    index = 0
    while True:
        # start = time.perf_counter()
        #time.sleep(0.05)
        try:
            scr = get_screenshot(index % 2 + 1)
            index += 1
            expr = recognize_new(lr, scr)
            #print(expr, eval(expr))
            
            if flag == expr:
                continue
            else:
                flag = expr
                if eval(expr):
                    m.click(loc['click_true_x'], loc['click_true_y'], 1)
                    #os.system("adb shell input tap 300 1500")
                else:
                    m.click(loc['click_false_x'], loc['click_false_y'], 1)
                    #os.system("adb shell input tap 800 1500")
        except:
            if 'scr' in vars():
                scr.save('failed.png')
            print('Error occurred: ')
            print(traceback.print_exc())
            break
        # print('One loop: ', time.perf_counter() - a)
        

def getTrainImage():
    while True:
        try:
            scr = get_screenshot()
            saveImages(scr)
            print('finished')
            time.sleep(3)
        except Exception as e:
            break
    


if __name__ == '__main__':
    Play()
    #getTrainImage()
