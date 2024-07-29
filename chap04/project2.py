import numpy as np
import cv2

# 마우스 콜백 함수 정의
def onMouse(event, x, y, flags, param):
    global image
    thickness = cv2.getTrackbarPos('Thickness', 'Image')  # 선의 굵기 트랙바 위치 가져오기
    radius = cv2.getTrackbarPos('Radius', 'Image')  # 원의 반지름 트랙바 위치 가져오기
    
    if event == cv2.EVENT_RBUTTONDOWN:  # 마우스 오른쪽 버튼 클릭 시 원 그리기
        cv2.circle(image, (x, y), radius, thickness)
    elif event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭 시 사각형 그리기
        cv2.rectangle(image, (x - 15, y - 15), (x + 15, y + 15), thickness)
    cv2.imshow('Image', image)

# 트랙바 콜백 함수 (트랙바 이동 시 특별한 동작이 필요하지 않으므로 빈 함수로 둠)
def nothing(x):
    pass

# 이미지와 윈도우 생성
image = np.full((400, 400, 3), 255, np.uint8)
cv2.namedWindow('Image')

# 트랙바 생성
cv2.createTrackbar('Thickness', 'Image', 1, 10, nothing)  # 선의 굵기 조절 트랙바
cv2.createTrackbar('Radius', 'Image', 20, 50, nothing)  # 원의 반지름 조절 트랙바

# 마우스 콜백 함수 설정
cv2.setMouseCallback('Image', onMouse)

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()