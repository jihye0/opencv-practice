# import cv2
# import numpy as np
# import pytesseract

# TESSERACT_PATH = "/opt/homebrew/Cellar/tesseract" #테서렉스 설치 경로
# imgpath="/Users/jihye/FLY AI/opencv/Source/chap06/proj_images/images/2-1.jpg"  #이미지 파일 경로
# win_name = "Image To Text"  #OpenCV 창 이름
# img = cv2.imread(imgpath)   #이미지 읽어오기
# point_list=[]

# #마우스 이벤트 처리 함수
# def onMouse(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         point_list.append((x, y))
#         cv2.circle(img, (x, y), 5, (0, 0, 0), -1)
#         cv2.imshow(win_name, img) 
#         print(point_list)
#     return 0

#이미치 처리 함수
def ImgProcessing():
    # gray = 
    return 0


#OCR 함수
def GetOCR():
    #이미지 불러오기
    global warped
    #OCR모델 불러오기
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    #OCR모델로 글자 추출
    text = pytesseract.image_to_string(warped, lang='kor+eng')
    return text

# cv2.setMouseCallback('img', onMouse)
# cv2.imshow(win_name, img)   #이미지 출력
# cv2.waitKey(0)              #입력 대기
# text = GetOCR()             #OCR함수로 텍스트 추출
# print(text)                 #텍스트 출력

import cv2
import numpy as np
import pytesseract
check=0
TESSERACT_PATH = "/opt/homebrew/Cellar/tesseract" #테서렉스 설치 경로
# 마우스 클릭 콜백 함수
def draw_dot(event, x, y, flags, param):
    global check
    if event == cv2.EVENT_LBUTTONDOWN:
        # 마우스 왼쪽 버튼 클릭 시 점을 찍음
        point_list.append((x, y))
        cv2.circle(image, (x, y), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.imshow('Image with Dots', image)
        print(point_list)
        check=check+1
        if check==4:
            points=np.array(point_list)
            # 다각형을 그리고 표시
            cv2.polylines(image, [points.astype(np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.imshow('Image with Dots', image)

            # 다각형의 최소 영역 회전된 사각형을 찾습니다
            rect = cv2.minAreaRect(points)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # 다각형 영역을 잘라냅니다
            width = int(rect[1][0])
            height = int(rect[1][1])

            src_pts = box.astype("float32")
            dst_pts = np.array([[0, height-1],
                                [0, 0],
                                [width-1, 0],
                                [width-1, height-1]], dtype="float32")

            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(image, M, (width, height))
            
            cv2.imshow('Cropped Image', warped)

# 이미지를 읽어옵니다.
image = cv2.imread('/Users/jihye/FLY AI/opencv/Source/chap06/proj_images/images/2-1.jpg')

# 이미지 창을 생성합니다.
cv2.namedWindow('Image with Dots')
point_list=[]

# 마우스 콜백 함수를 설정합니다.
cv2.setMouseCallback('Image with Dots', draw_dot)

# 이미지를 화면에 표시합니다.
cv2.imshow('Image with Dots', image)
cv2.waitKey(0)
text = GetOCR()             #OCR함수로 텍스트 추출
print(text)   
cv2.destroyAllWindows()