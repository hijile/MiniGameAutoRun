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
from screenshot import ScreenShot
from ImgUtil import ImgUtil



class AutoPlay():

    def __init__(self):
        self.m = PyMouse()
        self.shot = ScreenShot(loc)
        self.ImgUtil = ImgUtil()
        with open('lr.pickle', 'rb') as fr:
            self.lr = pickle.load(fr)

    def Play(self):
        m = self.m
        shot = self.shot
        lr = self.lr
        ImgUtil = self.ImgUtil
        
        flag = ""
        while True:
            # start = time.perf_counter()
            time.sleep(0.05)
            try:
                scr = shot.shotByWinAPI('Screenshots\screenshot.png')
                expr = ImgUtil.recognize(lr, scr)
                #expr = recognize_new(lr, scr)

                print(expr, eval(expr))
                
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
                #if 'scr' in vars():
                #    scr.save('failed.png')
                print('Error occurred: ')
                print(traceback.print_exc())
                break
            # print('One loop: ', time.perf_counter() - a)
            

    def getTrainImage(self):
        while True:
            try:
                scr = shot.shotByWinAPI('Screenshots\screenshot.png')
                saveImages(scr)
                print('finished')
                time.sleep(3)
            except Exception as e:
                break
    


if __name__ == '__main__':
    ap = AutoPlay()
    ap.Play()
    #getTrainImage()
