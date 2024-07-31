import numpy as np, cv2

image = cv2.imread('chap08/images/affine.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일을 읽기 에러")

center=(200, 200)
angle, scale=30, 1
size=image.shape[::-1]

pt1=np.array([(30, 70), (20, 240), (300, 110)], np.float32)
pt2=np.array([(120, 20), (10, 180), (180, 260)], np.float32)

aff_mat=cv2.getAffineTransform(pt1, pt2)
rot_mat=cv2.getRotationMatrix2D(center, angle, scale)

dst3=cv2.warpAffine(image, aff_mat, size, cv2.INTER_LINEAR)
dst4=cv2.warpAffine(image, rot_mat, size, cv2.INTER_LINEAR)

image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
dst3 = cv2.cvtColor(dst3, cv2.COLOR_GRAY2BGR )

for i in range(len(pt1)):
    cv2.circle(image, tuple(pt1[i].astype(int)), 3, (0, 0, 255), 2)
    cv2.circle(dst3 , tuple(pt2[i].astype(int)), 3, (0, 0, 255), 2)

cv2.imshow("image", image)
cv2.imshow("dst3_OpenCV_affine", dst3); cv2.imshow("dst4_OpenCV_affine_rotate", dst4)
cv2.waitKey(0)