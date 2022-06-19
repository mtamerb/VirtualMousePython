# kütüphaneleri import edelim
import numpy as np
import el_modul as em
import autopy
import cv2

# genislik ve yuksleık degerlerını girelim
hCam = 720
wCam = 720

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = em.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    # parmakları bulalım
    fingers = [0, 0, 0, 0, 0]
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # orta parmak için
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

    cv2.rectangle(img, (100, 100), (wCam - 100, hCam - 100),
                  (255, 0, 255), 2)
    # parmak hareketleri için

    if fingers[1] == 1 and fingers[2] == 0:
        # 5. Convert Coordinates
        x3 = np.interp(x1, (100, wCam - 100), (0, wScr))
        y3 = np.interp(y1, (100, hCam - 100), (0, hScr))
        clocX = plocX + (x3 - plocX) / 10
        clocY = plocY + (y3 - plocY) / 10

        # mouse hareketi
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    if fingers[1] == 1 and fingers[2] == 1:
        # parmak mesafesi için
        length, img, lineInfo = detector.findDistance(8, 12, img)
        # mesafe kısa olunca click etsin
        if length < 40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()

    # ekrana basalım
    cv2.imshow("Image", img)
    cv2.waitKey(1)
