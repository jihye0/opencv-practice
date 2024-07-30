import numpy as np, cv2

def onThreshold(value):
    result=cv2.threshold(BGR_img, value, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("result", result)

BGR_img = cv2.imread("chap06/images/color_space.jpg", cv2.IMREAD_COLOR) # 컬러 영상 읽기
if BGR_img is None: raise Exception("영상 파일 읽기 오류")

cv2.namedWindow('result')
cv2.createTrackbar("threshold", "result", 128, 255, onThreshold)
onThreshold(128)

cv2.imshow("BGR_img", BGR_img)
cv2.waitKey(0)