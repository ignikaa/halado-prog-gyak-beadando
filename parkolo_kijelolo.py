import cv2
import pickle

# --- Konfiguráció ---
start_width, start_height = 107, 48 # Kezdő méret

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f) # Korábbi adatok betöltése
except:
    posList = [] # Üres lista, ha nincs fájl

def empty(a):
    pass

# Beállító ablak és csúszkák létrehozása
cv2.namedWindow("Beallitasok")
cv2.resizeWindow("Beallitasok", 300, 150)
cv2.createTrackbar("Szelesseg", "Beallitasok", start_width, 200, empty)
cv2.createTrackbar("Magassag", "Beallitasok", start_height, 150, empty)

def mouseClick(events, x, y, flags, params):
    # Méretek lekérése a csúszkákról
    w = cv2.getTrackbarPos("Szelesseg", "Beallitasok")
    h = cv2.getTrackbarPos("Magassag", "Beallitasok")

    # Bal klikk: Új hely hozzáadása (pozíció + méret)
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y, w, h))
    
    # Jobb klikk: Hely törlése
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            px, py, pw, ph = pos
            if px < x < px + pw and py < y < py + ph:
                posList.pop(i)
                break 

    # Adatok mentése fájlba
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    cap = cv2.VideoCapture('carPark.mp4')
    success, img = cap.read()
    if not success:
        break
    
    curr_w = cv2.getTrackbarPos("Szelesseg", "Beallitasok")
    curr_h = cv2.getTrackbarPos("Magassag", "Beallitasok")

    # Mentett helyek kirajzolása
    for pos in posList:
        x, y, w, h = pos
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

    # Aktuális kurzor méret mutatása
    cv2.rectangle(img, (10, 10), (10 + curr_w, 10 + curr_h), (0, 255, 255), 2)
    cv2.putText(img, "Aktualis meret", (15, 30 + curr_h), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Parkolo Kijelolo", img)
    #cv2.setMouseCallback("Parkolo Kijelolo", mouseClick)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()