import cv2


cap = cv2.VideoCapture(0)

while cv2.waitKey(1) != 27:
    flag, img = cap.read()
    if flag:
        cv2.imshow("test", img)