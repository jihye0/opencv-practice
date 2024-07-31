import numpy as np, cv2

def contain(p, shape):                              # 좌표(y,x)가 범위내 인지 검사
    return 0<=p[0]<shape[0] and 0<=p[1]<shape[1]

def translate(img, pt):
    dst=np.zeros(img.shape, img.dtype)
    for i in range(img.shape[0]):
       for j in range(img.shape[1]):
           x, y=np.subtract((j, i), pt)
           if contain((y, x), img.shape):
               dst[i, j]=img[y,x]
    return dst

image = cv2.imread('Chap08/images/translate.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일을 읽기 에러")

dst1 = translate(image, (30, 80))
dst2 = translate(image, (-70, -50))

cv2.imshow("image", image)
cv2.imshow("dst1: trans to (80, 30)", dst1);
cv2.imshow("dst2: trans to (-50, -70)", dst2);
cv2.waitKey(0)
