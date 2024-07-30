import numpy as np, cv2

image = cv2.imread("chap07/images/filter_avg.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

blur_img=cv2.blur(image, (5,5), borderType=cv2.BORDER_CONSTANT)
box_img=cv2.boxFilter(image, ddepth=-1, ksize=(5,5))

cv2.imshow("image", image),
cv2.imshow("blur_img", blur_img)
cv2.imshow("box_img", box_img)
cv2.waitKey(0)