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
        if count < 800: 
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

while True:
    # Videó újraindítása ha véget ér
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    success, img = cap.read()
    if not success:
        break

    # --- Képfeldolgozási lánc ---
    
    # 1. Szürkeárnyalatos konverzió
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Elmosás (zajszűrés)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    
    # 3. Adaptív küszöbölés (Élek kiemelése, árnyékok kezelése)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    
    # 4. Median szűrő (zaj eltávolítása)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    
    # 5. Vastagítás (A vékony élek felerősítése)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Elemző függvény hívása
    checkParkingSpace(imgDilate, img)

    cv2.imshow("Parkolo Rendszer", img)
    cv2.imshow("A GEP LATASA (Fekete-Feher)", imgDilate) 
    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()