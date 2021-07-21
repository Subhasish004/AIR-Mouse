import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui as pg

#########################
wCam ,hCam =580, 420
frameR = 100
smoothening = 6
fingers = []
##########################

pTime = 0
cTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)

wScr, hScr = autopy.screen.size()
#print(wScr, hScr)

while True:
    #1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    try:
        fingers = detector.fingersUp()
    except IndexError:
        pass

    
    #2. Get the tip fo the index  and middle fingers

    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        #print(x1,y1,x2,y2)
  


    #3. check which fingers are up

    
    #print(fingers)
    cv2.rectangle(img,(frameR, frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
    #4. Only index Finger: Moving Mode
    try:
        if fingers[1]==1 and fingers[2]==0:
 
            #5. Convert Coordinates
        
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))


            #6. Smoothen Values

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #7. Move Mouse
            #autopy.mouse.move(wScr-x3 ,y3)
            #pg.moveTo(wScr-clocX,clocY)  #Not Working @coodinates
            autopy.mouse.move(wScr - clocX ,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY
    

        #8. Both index and middle finger are up : clicking mode 
        if fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
            #9. Find distance Between fingers
            length, img, lineInfo= detector.findDistance(8, 12, img)
            #print(length)
            #10. Click mouse if distance short
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()
            cv2.waitKey(40)
        
        #Right CLick
        if fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
            length, img, lineInfo= detector.findDistance(8, 16, img)
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            pg.rightClick()
            cv2.waitKey(20)

        

    
        #Drag
        if fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
                pg.mouseDown()
                #cv2.waitKey(20)
    
        #backspace
        if fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
            pg.press('backspace')
            cv2.waitKey(400)
        #Volume Control
        if fingers[0]==1 and fingers[1]==0 and fingers[3]==0 and fingers[3]==0 and fingers[4]==1:
            length, img, lineInfo= detector.findDistance(4, 20, img)
            #print(length)
            if length > 80:
                pg.press('volumeup')
        if fingers[0]==1 and fingers[1]==1 and fingers[3]==0 and fingers[3]==0 and fingers[4]==0:
            
            length, img, lineInfo= detector.findDistance(4, 8, img)
            

            #print(length)
            if length < 30:
                pg.press('volumedown')
        
        #WIN KEY
        if fingers[0]==0 and fingers[1]==0 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
            pg.press('win')
            cv2.waitKey(400)
        
        #MUTE
        if fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
            pg.press('volumemute')
            cv2.waitKey(400)
        #CTRL
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
            pg.press('ctrlleft')
            cv2.waitKey(400)
        
        
    except IndexError:
        pass
    #11. Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    #12.Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)