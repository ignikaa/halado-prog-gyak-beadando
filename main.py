import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')

# Pozíciók betöltése a fájlból
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro, imgOriginal):
    spaceCounter = 0

    for pos in posList:
        x, y, w, h = pos 
        
        # Parkolóhely kivágása a feldolgozott képből
        imgCrop = imgPro[y:y+h, x:x+w]
        
        # Fehér pixelek számlálása
        count = cv2.countNonZero(imgCrop)
        
        # Ha a pixelszám alacsony (<900), akkor üres a hely
        if count < 900: 
            color = (0, 255, 0) # Zöld
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255) # Piros
            thickness = 2

        # Keret kirajzolása az eredeti képre
        cv2.rectangle(imgOriginal, (x, y), (x + w, y + h), color, thickness)

    # Információs sáv és szöveg
    cvzone.putTextRect(imgOriginal, f'Szabad: {spaceCounter}/{len(posList)}', (50, 60), scale=2, thickness=3, offset=10, colorR=(0,200,0))
    
    if spaceCounter > 0:
        cvzone.putTextRect(imgOriginal, "BEHAJTHAT", (50, 150), scale=3, thickness=3, offset=10, colorR=(0, 255, 0))
    else:
        cvzone.putTextRect(imgOriginal, "TELE VAN", (50, 150), scale=3, thickness=3, offset=10, colorR=(0, 0, 255))