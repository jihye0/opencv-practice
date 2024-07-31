import cv2
import dlib
from deepface import DeepFace
import numpy as np


# 1. OpenCV를 사용하여 노트북 카메라에서 비디오를 캡처
cap = cv2.VideoCapture(1)

# 2. dlib의 얼굴 감지기와 랜드마크 예측기 초기화
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 얼굴 랜드마크 예측을 위한 함수
def get_face_landmarks(image, rects):
    landmarks = []
    for rect in rects:
        shape = predictor(image, rect)
        landmarks.append([(p.x, p.y) for p in shape.parts()])
    return landmarks

# 시선 방향을 추정하기 위한 함수
def estimate_gaze(landmarks):
    left_eye_indices = list(range(36, 42))
    right_eye_indices = list(range(42, 48))
    nose_tip_index = 30
    left_eye = np.mean([landmarks[i] for i in left_eye_indices], axis=0).astype(int)
    right_eye = np.mean([landmarks[i] for i in right_eye_indices], axis=0).astype(int)
    nose_tip = landmarks[nose_tip_index]
    eye_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)
    gaze_vector = (nose_tip[0] - eye_center[0], nose_tip[1] - eye_center[1])
    return eye_center, gaze_vector
# 시선 방향을 텍스트로 결정하는 함수
def get_gaze_direction(gaze_vector):
    (x, y) = gaze_vector
    angle = np.arctan2(y, x) * 180 / np.pi
    if -45 <= angle <= 45:
        return "Right"
    elif 45 < angle <= 135:
        return "Down"
    elif -135 <= angle < -45:
        return "Up"
    else:
        return "Left"
# 3. 비디오 스트림을 프레임 단위로 처리
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 2. dlib 라이브러리를 사용하여 얼굴 감지
    faces = detector(gray)
    # 4. 얼굴 랜드마크 예측
    landmarks = get_face_landmarks(gray, faces)
    # 6. 감지된 얼굴 주위에 경계 상자를 그리고 랜드마크를 그리기
    for (i, rect) in enumerate(faces):
        (x, y, w, h) = (rect.left(), rect.top(), rect.width(), rect.height())
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        for (x, y) in landmarks[i]:
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
        # 시선 방향 추정
        eye_center, gaze_vector = estimate_gaze(landmarks[i])
        gaze_endpoint = (eye_center[0] + gaze_vector[0], eye_center[1] + gaze_vector[1])
        cv2.arrowedLine(frame, eye_center, gaze_endpoint, (255, 0, 0), 2)
        # 시선 방향 결정 및 텍스트 표시
        gaze_direction = get_gaze_direction(gaze_vector)
        cv2.putText(frame, gaze_direction, (eye_center[0], eye_center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    # 7. DeepFace를 사용하여 얼굴 분석
    for (i, rect) in enumerate(faces):
        (x, y, w, h) = (rect.left(), rect.top(), rect.width(), rect.height())
        face = frame[y:y+h, x:x+w]
        try:
            # 얼굴 분석
            analysis = DeepFace.analyze(face, actions=['age', 'gender', 'emotion'], enforce_detection=False)
            print(analysis)  # 분석 결과 출력
            gender = analysis[0]['dominant_gender']
            age = analysis[0]['age']
            emotion = analysis[0]['dominant_emotion']
            text = f"Gender: {gender}, Age: {age}, Emotion: {emotion}"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        except Exception as e:
            print(f"DeepFace 분석 오류: {e}")
    # 프레임을 화면에 표시
    cv2.imshow("Video", frame)
    # 'q' 키를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 8. 비디오 캡처 및 창 닫기
cap.release()
cv2.destroyAllWindows()