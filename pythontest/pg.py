import pygame

import time

import ctypes
from ctypes import wintypes
import pyautogui
from pygame.constants import K_w
import unicode 
import socket #소켓 
import threading #멀티쓰레딩
from PIL import Image
import os
import sys
import random
#-*- coding: utf-8 -*-


# if getattr(sys, 'frozen', False):
#     CurrentPath = os.environ.get("_MEIPASS2")
    
# else:
#     #CurrentPath = os.path.dirname(__file__)
#     CurrentPath = ''


# 자음-초성/종성
cons = {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ'}
# 모음-중성
vowels = {'k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'nj':'ㅝ', 'np':'ㅞ', 'nl':'ㅟ', 'b':'ㅠ',  'm':'ㅡ', 'ml':'ㅢ', 'l':'ㅣ'}

# 자음-종성
cons_double = {'rt':'ㄳ', 'sw':'ㄵ', 'sg':'ㄶ', 'fr':'ㄺ', 'fa':'ㄻ', 'fq':'ㄼ', 'ft':'ㄽ', 'fx':'ㄾ', 'fv':'ㄿ', 'fg':'ㅀ', 'qt':'ㅄ'}

def engkor(text):
    result = ''   # 영 > 한 변환 결과
    
    # 1. 해당 글자가 자음인지 모음인지 확인
    vc = '' 
    for t in text:
        if t in cons :
            vc+='c'
        elif t in vowels:
            vc+='v'
        else:
            vc+='!'
	
    # cvv → fVV / cv → fv / cc → dd 
    vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')
	
    
    # 2. 자음 / 모음 / 두글자 자음 에서 검색
    i = 0
    while i < len(text):
        v = vc[i]
        t = text[i]

        j = 1
        # 한글일 경우
        try:
            if v == 'f' or v == 'c':   # 초성(f) & 자음(c) = 자음
                result+=cons[t]

            elif v == 'V':   # 더블 모음
                result+=vowels[text[i:i+2]]
                j+=1

            elif v == 'v':   # 모음
                result+=vowels[t]

            elif v == 'd':   # 더블 자음
                result+=cons_double[text[i:i+2]]
                j+=1
            else:
                result+=t
                
        # 한글이 아닐 경우
        except:
            if v in cons:
                result+=cons[t]
            elif v in vowels:
                result+=vowels[t]
            else:
                result+=t
        
        i += j


    return unicode.join_jamos(result)     
 
VK_HANGUEL = 0x15

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


SIZE = width,height = 1280,720

CameraPos = [0, 0]
ScreenCameraRatio = 36

def worldToCamera(tempPos):
    pos = tempPos.copy()
    pos[0] -= CameraPos[0]
    pos[1] -= CameraPos[1]

    pos[0] *= ScreenCameraRatio
    pos[1] *= ScreenCameraRatio

    pos[0] += width/2
    pos[1] += height/2
    return pos

def cameraToWorld(tempPos):
    pos = tempPos.copy()
    pos[0] -= width/2
    pos[1] -= height/2

    pos[0] /= ScreenCameraRatio
    pos[1] /= ScreenCameraRatio
    
    pos[0] += CameraPos[0]
    pos[1] += CameraPos[1]
    return pos


print('접속할 서버의 ip 주소를 입력해 주세요')
ip = input()
print('닉네임을 입력해 주세요')
name = input()
print('사용할 캐릭터 이미지의 링크를 붙여넣어 주세요 (미입력시 기본 주소 사용) : ')
image_url = input()
if len(image_url) < 5 :
    image_url = 'https://i.imgur.com/y29Ztbj.png'


screen = pygame.display.set_mode(SIZE)

screen.fill("WHITE")

pygame.init()


hllDll = ctypes.WinDLL ("User32.dll", use_last_error=True)
 
# Text Editing
def get_hanguel_state():
    return (hllDll.GetKeyState(VK_HANGUEL) & 0x15)
 

os.chdir((sys.path[0]))

text1 = '텍스트를 입력하려면 엔터키를 누르세요'
font1 = pygame.font.Font('gothic.ttf',15)
img1 = font1.render(text1,True,pygame.Color(100, 100, 100, 255))
 
rect1 = img1.get_rect()
rect1.topleft = (30,30)
cursor1 = pygame.Rect(rect1.topright,(3,rect1.height))
colorRect = pygame.Rect((1200,620), (40,40))

texts = ['공백', '공백', '공백', '공백', '공백', '공백', '공백', '공백']

running = True

if os.path.exists( name + ".png"):
    os.remove( name + ".png")

#tempPlayerImage = pygame.image.load('tempPlayer.png')
os.system("curl " + image_url + " > " + name + ".png")
tempPlayerImage = pygame.image.load(name + ".png")
tempPlayerImage = pygame.transform.scale(tempPlayerImage, (100,100))
playerPos = [0,0]
playerSpeed = 7
playerVelocity = [0,0]

isSpace = 0
skip = False
isKorean = False
tempKor = ''
isChatting = False
textResult = ''
getTicksLastFrame = 0
clock = pygame.time.Clock()

clientsImage = {}
clientsPos = {}

def addText(tmpText):
    global texts
    if len(texts) > 7:
        texts = texts[1:] + [tmpText]
    else:
        texts = texts + [tempText]
        
    print(texts)

def consoles(): 
    while True: 
        msgs=client.recv(1024)
        msgs = msgs.decode()
        for msg in msgs.split('&&'):
            if msg:
                if msg[0] == '`':
                    addText(msg)
                if msg[0] == '>':
                    tmpinfos = msg[1:].split("|")
                    os.system("curl " + tmpinfos[1] + " > " + tmpinfos[0] + ".png")
                    clientsImage[tmpinfos[0]] = pygame.image.load(tmpinfos[0]+ ".png")
                    clientsImage[tmpinfos[0]] = pygame.transform.scale(clientsImage[tmpinfos[0]], (100,100))
                    clientsPos[tmpinfos[0]] = [0,0]
                if msg[0] == '<':
                    tmpinfos = msg[1:].split("|")        
                    print('remove!')  
                    if(tmpinfos[0] in clientsPos.keys()):
                        del clientsImage[tmpinfos[0]]
                        del clientsPos[tmpinfos[0]]
                if msg[0] == '~':
                    tmpinfos = msg[1:].split("|")
                    if(tmpinfos[0] in clientsPos.keys() and isNumber(tmpinfos[1]) and isNumber(tmpinfos[2])):
                        clientsPos[tmpinfos[0]] = [float(tmpinfos[1]), float(tmpinfos[2])]
                if msg[0] == '+':
                    tmpinfos = msg[1:].split("|")
                    ttmp = tmpinfos[0].split(',')
                    tmpColor = [float(ttmp[0]), float(ttmp[1]), float(ttmp[2])]
                    spots.append([tmpColor, float(tmpinfos[1]), float(tmpinfos[2])])
                


def acceptC():
    global client 
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    print(ip)
    client.connect((ip,25565)) 
    thr=threading.Thread(target=consoles,args=()) 
    thr.Daemon=True 
    textResult = '>' + name + '|' + image_url + '&&'
    client.sendall(textResult.encode())
    thr.start()


acceptC()

spots = []

color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
while running:
    dt = clock.tick(60)
    tempText = ''
    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    for event in pygame.event.get():
        tmpt = "~"
        tmpt += name + '|' + str(playerPos[0]) + '|' + str(playerPos[1]) + '&&'
        if event.type == pygame.QUIT:
            textResult = '<' + name + '&&'
            client.sendall(textResult.encode())
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            [mx, my] = pygame.mouse.get_pos()
            mx = cameraToWorld([mx, my])[0]
            my = cameraToWorld([mx, my])[1]
            spots.append((color, mx, my))
            textResult = '+' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ',' + '|' + str(mx) + '|' + str(my) + '&'
            client.sendall(textResult.encode())


        if event.type == pygame.KEYDOWN and isChatting:
            if event.key == pygame.K_RETURN: 
                isChatting = False
                textResult = '`' + name + " : " + text1 + engkor(tempKor) + '&&'
                text1 = ''
                tempKor = '' 
                client.sendall(textResult.encode())

            if get_hanguel_state() == 1:
                isKorean = not isKorean
                pyautogui.press('hangul')
            if event.key == pygame.K_BACKSPACE:
                if len(tempKor) > 0:
                    tempKor = tempKor[:-1]
                elif len(text1)> 0:
                    text1 = text1[:-1]

            elif isKorean:
                tempKor += event.unicode
            else:
                if len(tempKor) > 0:
                    text1 += engkor(tempKor) + event.unicode
                    tempKor = ''
                else:
                    text1 += event.unicode


            img1 = font1.render(text1 + engkor(tempKor),True,pygame.Color(100, 100, 100, 255))
            rect1.size = img1.get_size()
            cursor1.topleft = rect1.topright

        elif event.type == pygame.KEYDOWN and not isChatting:
            if event.key == pygame.K_RETURN: 
                isChatting = True
                playerVelocity[0] = 0
                playerVelocity[1] = 0
            

            if event.key == pygame.K_w:
                playerVelocity[1] -= playerSpeed
            if event.key == pygame.K_a:
                playerVelocity[0] -= playerSpeed
            if event.key == pygame.K_s:
                playerVelocity[1] += playerSpeed
            if event.key == pygame.K_d:
                playerVelocity[0] += playerSpeed

            if event.key == pygame.K_r:
                color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                playerVelocity[1] =0
            if event.key == pygame.K_a:
                playerVelocity[0] =0
            if event.key == pygame.K_s:
                playerVelocity[1] =0
            if event.key == pygame.K_d:
                playerVelocity[0] =0

    if not isChatting:
        playerPos[0] += playerVelocity[0] * deltaTime
        playerPos[1] += playerVelocity[1] * deltaTime
        client.sendall(tmpt.encode())

    
    CameraPos[0] = (playerPos[0] + CameraPos[0] * 5) / 6
    CameraPos[1] = (playerPos[1] + CameraPos[1] * 5) / 6

    screen.fill("WHITE")

    tempBack = pygame.image.load("resources/tempBack2.png")
    tempBack = pygame.transform.scale(tempBack, (1200, 1200))
    screen.blit(tempBack, worldToCamera([-16.67, -16.67]))


    for i in clientsImage.keys():
        screen.blit(clientsImage[i], [worldToCamera(clientsPos[i])[0] - 50, worldToCamera(clientsPos[i])[1] - 50])
        iImg = font1.render(i,True,(90,150,120))
        r = iImg.get_rect()
        r.center = (worldToCamera(clientsPos[i])[0], worldToCamera(clientsPos[i])[1] - 70)
        screen.blit(iImg, r)

    screen.blit(tempPlayerImage, [worldToCamera(playerPos)[0] - 50, worldToCamera(playerPos)[1] - 50])

    for c in spots:
        pygame.draw.circle(screen, c[0], worldToCamera([c[1], c[2]]), 10)
        print(c)




    screen.blit(img1,rect1)
    
    timg = font1.render("R키를 눌러 색상을 새로 배정",True,"BLACK")

    r = timg.get_rect()
    r.bottomright = (1240, 690)
    screen.blit(timg, r)

    i = 0
    for t in texts.__reversed__():
        iImg = font1.render(t,True,"BLACK")
        r = iImg.get_rect()
        r.topleft = (40,60 + i*25)
        i+=1
        screen.blit(iImg, r)
    i = 0

    if time.time() % 1 > 0.5 and isChatting:
        pygame.draw.rect(screen, "RED", cursor1)

    colorRect.center = (1220, 650)
    colorRect.width = 40
    colorRect.height = 40
    pygame.draw.rect(screen, color, colorRect)
    pygame.display.update()

 

pygame.quit()
