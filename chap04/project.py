import cv2

capture = cv2.VideoCapture(0)  # 0번 카메라 연결
if capture.isOpened() == False:
    raise Exception("카메라 연결 안됨")

# 카메라 속성 획득 및 출력
print("너비 %d" % capture.get(cv2.CAP_PROP_FRAME_WIDTH))
print("높이 %d" % capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("노출 %d" % capture.get(cv2.CAP_PROP_EXPOSURE))
print("밝기 %d" % capture.get(cv2.CAP_PROP_BRIGHTNESS))
pt1, pt2 = (200, 100), (300, 300) 

while True:  # 무한 반복
    ret, frame=capture.read()
    if not ret: break
    if cv2.waitKey(30) >= 0: break

    blue, green, red=cv2.split(frame)
    cv2.add(green[100:300, 200:300], 50, green[100:300, 200:300])
    frame=cv2.merge([blue, green, red])
    title = "View Frame from Camera"
    cv2.rectangle(frame, pt1, pt2, (0, 0, 255), 3, cv2.LINE_4)
    cv2.imshow(title, frame)  # 윈도우에 영상 띄우기
    
capture.release()