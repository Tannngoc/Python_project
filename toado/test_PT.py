import cv2
import dlib
import time

net = cv2.dnn.readNetFromCaffe(
    './models/deploy.prototxt.txt',
    './models/res10_300x300_ssd_iter_140000_fp16.caffemodel'
)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')

cap = cv2.VideoCapture(0)

start_time = time.time()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Cannot read frame from webcam.")
        break

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177, 123), swapRB=False)
    net.setInput(blob)
    faces = net.forward()

    h, w = frame.shape[:2]
    all_face_landmarks = []

    for i in range(0, faces.shape[2]):
        confidence = faces[0, 0, i, 2]
        if confidence > 0.5:
            startx = max(0, int(faces[0, 0, i, 3] * w))
            starty = max(0, int(faces[0, 0, i, 4] * h))
            endx = min(w, int(faces[0, 0, i, 5] * w))
            endy = min(h, int(faces[0, 0, i, 6] * h))

            cv2.rectangle(frame, (startx, starty), (endx, endy), (0, 255, 0))
            text = 'Face: {:.2f}%'.format(confidence * 100)
            cv2.putText(frame, text, (startx, starty - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

            rect = dlib.rectangle(startx, starty, endx, endy)
            shape = predictor(frame, rect)
            face_landmarks = []

            for j in range(68):
                x = shape.part(j).x
                y = shape.part(j).y
                if startx <= x <= endx and starty <= y <= endy:
                    face_landmarks.append((x - startx, y - starty))
                    cv2.circle(frame, (x, y), 1, (255, 200, 0), -1)
                    if j < 67:
                        mid_x = int((x + shape.part(j + 1).x) / 2)
                        mid_y = int((y + shape.part(j + 1).y) / 2)
                        if startx <= mid_x <= endx and starty <= mid_y <= endy:
                            cv2.circle(frame, (mid_x, mid_y), 2, (255, 200, 0), -1)

            all_face_landmarks.append(face_landmarks)

    cv2.imshow('Result', frame)

    #Cam sẽ tự động tắt sau 10s, có thể chỉnh lại theo ý muốn của thầy
    if time.time() - start_time > 10:
        print("Finished after 10 seconds.")

        #Đổi tên file thành anh2.txt để xác thực với file anh1.txt khi chạy lần 2
        with open("./Team_Project/toado/anh1.txt", "w") as file:
            for landmarks in all_face_landmarks:
                for x, y in landmarks:
                    file.write(f"{x},{y}\n")
        print("Saved coordinates to toado folder")
        cv2.imshow('Result', frame)
        cv2.waitKey(3000)
        break

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
