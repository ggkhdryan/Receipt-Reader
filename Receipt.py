import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'


def mapp(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew



img = cv2.imread('files/2.jpg')
img = cv2.resize(img,(500,800)) #make image smaller


gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #make image grayscale
orig = gray.copy()
blurred = cv2.GaussianBlur(gray,(5,5),0) #apply gaussian blur to image
edged = cv2.Canny(blurred,30,50) #find image edges

contours,hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours,key=cv2.contourArea,reverse=True)

max_area = 0
for c in contours:
    area = cv2.contourArea(c)
    p = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.02*p,True)
    if area>max_area and len(approx)==4:
        target = approx
        max_area = area

approx = mapp(target)

pts = np.float32(([0,0],[500,0],[500,800],[0,800]))
op = cv2.getPerspectiveTransform(approx,pts)
dst = cv2.warpPerspective(orig,op,(500,800))

cv2.imshow("Title",dst)
cv2.waitKey(0)

text = pytesseract.image_to_string(dst)
print(text)