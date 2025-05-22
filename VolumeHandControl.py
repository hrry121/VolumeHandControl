import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################################
wCam, hCam= 800, 800 #Height and width of camera (setting manually)


cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector(dectectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange= volume.GetVolumeRange()
#print(volume.GetVolumeRange())

minVol= volRange[0]
maxVol= volRange[1]
vol=0
volBar=400
volPer=0
while True:
    success, img= cap.read()
    img=detector.findHands(img)
    lmlist=detector.findpos(img, draw=False)
    if len(lmlist) !=0:
        #print(lmlist[4], lmlist[8]) #Landmark of tip of thumb and index

        x1,y1= lmlist[4][1] , lmlist[4][2]
        x2,y2= lmlist[8][1], lmlist[8][2]


        cv2.circle(img, (x1,y1),15,(0,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cx,cy= (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

        cv2.line(img, (x1,y1), (x2,y2),(255,255,0),3)
        length= math.hypot(x2-x1, y2-y1)
        #print(length)
        # Max length is around 230 and min length is around 10
        # Vol Range is -63.5 to 0


        vol= np.interp(length,[10,230],[minVol,maxVol])
        volBar = np.interp(length,[10,230],[400,150])
        volPer = np.interp(length, [10, 230], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length<20:
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

    cv2.rectangle(img,(50,150), (85,400),(0,0,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

    cTime= time.time()
    fps=1/(cTime-pTime)
    pTime=cTime


    cv2.putText(img, f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)



    cv2.imshow("Img" , img)
    cv2.waitKey(1)