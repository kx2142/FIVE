import os
import datetime
import win32api
import win32clipboard
import win32gui
import win32con
import time
import ctypes
from PIL import ImageGrab
import aircv as ac
import win32clipboard as wincld
import webbrowser
import subprocess
import sys,os,subprocess
from subprocess import Popen,PIPE


#对比两张图，找到坐标。
def matchImg(imgsrc, imgobj):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
    match_result = ac.find_template(imsrc, imobj, 0.9)  #0.9、confidence是精度，越小对比的精度就越低 {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    # print(match_result)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
    return match_result

def manyclick(SN='ab0729cf', Re=True):
    # 这里是在点击屏幕固定区域采集能量
    for myx in range(200, 900, 50):
        for myy in range(500, 900, 50):
            myxstr = str(myx)
            myystr = str(myy)
            os.popen('adb -s {} shell input tap {} {}'.format(SN, myxstr, myystr), 'r', 1)
            # print(myxstr +' , '+myystr)
            time.sleep(0.1)
    # 返回
    if Re == True:
        os.popen('adb -s ab0729cf shell input keyevent 4', 'r', 1)
        time.sleep(1)

#打开支付宝蚂蚁森林操作
def openalipay(SN='ab0729cf'):
    # 返回
    os.popen('adb -s {} shell input keyevent 4'.format(SN), 'r', 1)
    time.sleep(0.3)
    # 返回
    os.popen('adb -s {} shell input keyevent 4'.format(SN), 'r', 1)
    time.sleep(0.3)
    # 返回
    os.popen('adb -s {} shell input keyevent 4'.format(SN), 'r', 1)
    time.sleep(0.3)
    # 去点击
    os.popen('adb -s {} shell input keyevent 3'.format(SN), 'r', 1)
    time.sleep(1)
    os.popen('adb -s {} shell input swipe 500 1000 250 1000'.format(SN), 'r', 1)
    time.sleep(1)
    # 打开alipay文件夹
    os.popen('adb -s {} shell input tap 900 1150'.format(SN), 'r', 1)
    time.sleep(1)
    # 打开alipay
    os.popen('adb -s {} shell input tap 250 850'.format(SN), 'r', 1)
    time.sleep(2)
    # 打开蚂蚁森林
    os.popen('adb -s {} shell input tap 400 1350'.format(SN), 'r', 1)
    time.sleep(1)

# 截图
def screencap(SN='ab0729cf'):
    # 截图
    os.popen('adb -s {} shell screencap -p /sdcard/phoneScreencap.png'.format(SN))
    time.sleep(1.5)
    #发送到电脑
    os.popen('adb -s {} pull /sdcard/phoneScreencap.png'.format(SN))
    time.sleep(1.5)

def forest_to_list(SN='ab0729cf'):
    for i in range(4):
        os.popen('adb -s {} shell input swipe 500 1000 500 500'.format(SN), 'r', 1)
        time.sleep(1)
    os.popen('adb -s {} shell input tap 500 1980'.format(SN), 'r', 1)
    time.sleep(1)

def collect(SN='ab0729cf'):
    # 截图
    screencap()
    # alipay_hand
    i = 0
    while True:
        if matchImg('phoneScreencap.png', 'alipay_hand.png') != None:
            print("alipay_hand！" + str(
                matchImg('phoneScreencap.png', 'alipay_hand.png')['result'][0]) + ',' + str(
                matchImg('phoneScreencap.png', 'alipay_hand.png')['result'][1]))
            myx = str(matchImg('phoneScreencap.png', 'alipay_hand.png')['result'][0])
            myy = str(matchImg('phoneScreencap.png', 'alipay_hand.png')['result'][1])
            os.popen('adb -s {} shell input tap {} {}'.format(SN, myxstr, myystr), 'r', 1)
            time.sleep(3)
            print("manyclick")
            manyclick()
            # 截图
            screencap()
        else:
            # 向下滚动排行榜
            for j in range(2):
                os.popen('adb -s {} shell input swipe 500 1000 500 400'.format(SN), 'r', 1)
                time.sleep(1)
            screencap()
        # 判断是否到底
        # print(matchImg('phoneScreencap.png', 'alipay_hand.png')==None, matchImg('phoneScreencap.png', 'alipay_nomore.png') != None)
        if matchImg('phoneScreencap.png', 'alipay_hand.png') == None and matchImg('phoneScreencap.png', 'alipay_nomore.png') != None:
            i += 1
            print('已循换{}次'.format(i))
            restart()
            screencap()
            
def present(SN='ab0729cf'):    
    # alipay_hui给特定的好友浇水，根据头像判断
    if matchImg('phoneScreencap.png', 'alipay_hui.png') != None:
        print("alipay_hui！" + str(
            matchImg('phoneScreencap.png', 'alipay_hui.png')['result'][0]) + ',' + str(
            matchImg('phoneScreencap.png', 'alipay_hui.png')['result'][1]))
        myx = str(matchImg('phoneScreencap.png', 'alipay_hui.png')['result'][0])
        myy = str(matchImg('phoneScreencap.png', 'alipay_hui.png')['result'][1])
        os.popen('adb -s {} shell input tap {} {}'.format(SN, myxstr, myystr), 'r', 1)
        time.sleep(4)
        print("water")
        os.popen('adb -s {} shell input tap 1000 1500'.format(SN), 'r', 1)
        time.sleep(3)
        # 返回
        os.popen('adb -s .format(SN) shell input keyevent 4'.format(SN), 'r', 1)
        time.sleep(2)

def restart(SN='ab0729cf'):
    # alipay_nomore到底部了，得从头开始
    print("alipay_nomore！" + str(
        matchImg('phoneScreencap.png', 'alipay_nomore.png')['result'][0]) + ',' + str(
        matchImg('phoneScreencap.png', 'alipay_nomore.png')['result'][1]))
    # 返回
    os.popen('adb -s {} shell input keyevent 4'.format(SN), 'r', 1)
    time.sleep(1)
    # 重新进入排行榜
    screencap( )
    if matchImg('phoneScreencap.png', 'alipay_lookForMoreFriends.png') != None:
        print("alipay_lookForMoreFriends！" + str(matchImg('phoneScreencap.png', 'alipay_lookForMoreFriends.png')['result'][0]) +','+ str(
            matchImg('phoneScreencap.png', 'alipay_lookForMoreFriends.png')['result'][1]))
        myx = str(matchImg('phoneScreencap.png', 'alipay_lookForMoreFriends.png')['result'][0])
        myy = str(matchImg('phoneScreencap.png', 'alipay_lookForMoreFriends.png')['result'][1])
        os.popen('adb -s 66819679 shell input tap '+myx+' '+myy, 'r', 1)
        time.sleep(1)

    
def morefriend(SN='ab0729cf'):


def accident_solve(SN='ab0729cf'):       
    # alipay_love因为网络等问题，如果出现这alipay_love图标就得从头再来。
    if matchImg('phoneScreencap.png', 'alipay_love.png') != None:
        print("alipay_love！" + str(
            matchImg('phoneScreencap.png', 'alipay_love.png')['result'][0]) + ',' + str(
            matchImg('phoneScreencap.png', 'alipay_love.png')['result'][1]))
        # 返回
        os.popen('adb -s {} shell input keyevent 4'.format(SN), 'r', 1)
        time.sleep(0.3)
        # 返回
        os.popen('adb -s {} shell input keyevent 4'.format(SN), 'r', 1)
        time.sleep(0.3)
        # 返回
        os.popen('adb -s a{} shell input keyevent 4'.format(SN), 'r', 1)
        time.sleep(0.3)
        # 返回
        os.popen('adb -s {} shell input keyevent 4'.format(SN), 'r', 1)
        time.sleep(0.3)
        openalipay()
        
#主函数
def main(SN='ab0729cf'):
    # 打开蚂蚁森林
    openalipay(SN)
    # 收取能量
    manyclick(SN, Re=False)
    # 打开好友排行榜
    forest_to_list(SN)
    # 滚动偷取能量
    collect(SN)

