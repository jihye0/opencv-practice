import numpy as np
import cv2

blue, green, red = (255, 0, 0), (0, 255, 0), (0, 0, 255)
white, black = (255, 255, 255), (0, 0, 0)

image = np.full((480, 640, 3), white, np.uint8)
cv2.circle(image, (200, 400), 40, blue, -1)
cv2.circle(image, (70, 370), 30, green, -1)
cv2.circle(image, (100, 220), 70, red, -1)
cv2.circle(image, (430, 100), 60, blue, -1)
cv2.circle(image, (400, 300), 70, green, -1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 2)
#이미지에 불러 처리를 한 뒤에 원을 탐지 하는 이유는 노이즈를 줄이고 더 정확하게 원을 탐지하기 위해서
#블러 처리는 작은 세부 사항이나 노이즈를 제거하여 가장자리 검출과 같은 후속 처리 단계에서 원활한 결과를 얻을 수 있도록 함
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=50, minRadius=20, maxRadius=80)


def color_distance(c1, c2):
    return np.linalg.norm(np.array(c1) - np.array(c2))

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        radius = i[2]
        color = image[center[1], center[0]].tolist()
        color_name = "Unknown"
        
        if color_distance(color, blue) < 50:
            color_name = "Blue"
            color_to_draw = blue
        elif color_distance(color, green) < 50:
            color_name = "Green"
            color_to_draw = green
        elif color_distance(color, red) < 50:
            color_name = "Red"
            color_to_draw = red
        else:
            continue
        
        cv2.putText(image, color_name, (i[0] - radius, i[1] - radius - 10), cv2.FONT_HERSHEY_PLAIN, 2, color_to_draw, 1)
        cv2.rectangle(image, (i[0] - radius, i[1] - radius), (i[0] + radius, i[1] + radius), (0, 0, 0), 1)

cv2.imshow("Detected Circles and Colors", image)
cv2.waitKey(0)
cv2.destroyAllWindows()