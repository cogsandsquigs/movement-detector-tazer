import cv2
import numpy as np

# Load the cascade
# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

threshold_movement = 0.1
threshold_movement_frame_count = 30
threshold_under_count = 0  # DONT TOUCH THIS
threshold_zap_buffer = 25
threshold_buffer_count = threshold_zap_buffer

cap = cv2.VideoCapture(0)
while True:

    ret1, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    ret2, frame2 = cap.read()
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    deltaframe = cv2.absdiff(gray1, gray2)
    cv2.imshow("delta", deltaframe)
    threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None)

    # counting the number of pixels
    number_of_white_pix = np.sum(threshold == 255)
    number_of_black_pix = np.sum(threshold == 0)

    if (
        number_of_white_pix / (number_of_black_pix + number_of_white_pix)
        < threshold_movement
    ):
        if (
            threshold_under_count >= threshold_movement_frame_count
            and threshold_buffer_count <= 0
        ):
            threshold_buffer_count = threshold_zap_buffer
            print("zap")
        elif threshold_under_count >= threshold_movement_frame_count:
            threshold_buffer_count -= 1
        print(threshold_under_count)
        threshold_under_count += 1

    else:
        threshold_under_count = 0
        print("no zap")

    cv2.imshow("threshold", threshold)
    countour, heirarchy = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for i in countour:
        if cv2.contourArea(i) < 50:
            continue

        (x, y, w, h) = cv2.boundingRect(i)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("window", frame2)

    if cv2.waitKey(20) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
