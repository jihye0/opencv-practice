import numpy as np, cv2

image = cv2.imread("chap07/images/edge.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")
    
dst1=cv2.Sobel(np.float32(image), cv2.CV_32F, 1, 0, ksize=3)
dst2=cv2.Sobel(np.float32(image), cv2.CV_32F, 0, 1, 3)

dst1=cv2.convertScaleAbs(dst1)
dst2=cv2.convertScaleAbs(dst2)

cv2.imshow("edge- sobel edge", image)
cv2.imshow("dst1- vertical_OpenCV", dst1)
cv2.imshow("dst2- horizontal_OpenCV", dst2)
cv2.waitKey(0)