"""
This code was written by Ian Pratt (ipratt-code, t0x1c_101, etc.)
All of this was his design (except for stackoverflow help, which is like 
40% of this). Conor wrote the code in hdwcnct.py
DO NOT USE THIS IN ANY FORM OF PRODUCTION
"""
import cv2

# from com import *
import numpy as np

regiment = False
threshold_movement = 0.075
threshold_movement_frame_count = 30
threshold_under_count = 0  # DONT TOUCH THIS
threshold_encouragement_buffer = 25
threshold_buffer_count = threshold_encouragement_buffer
base_frame_differ_threshold = 0.02
total_frames_recorded = 45
encourage_threshould = 3


def EncourageWrapper(data=1):
    for i in range(encourage_threshould):
        pass  # encourage(data)


def GetBaseVideo(indx):
    list_frames = []
    rec = cv2.VideoCapture(indx)
    i = 0
    while i < total_frames_recorded:
        r, f = rec.read()
        list_frames.append(f)
        i += 1
        cv2.imshow("window", f)
    return list_frames


def GetThreshold(g1, g2):
    deltaframe = cv2.absdiff(g1, g2)
    # cv2.imshow("delta", deltaframe)
    threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None)
    return threshold


def GetPixelDifference(thresh):
    number_of_white_pix = np.sum(threshold == 255)
    number_of_black_pix = np.sum(threshold == 0)
    return number_of_white_pix / (number_of_white_pix + number_of_black_pix)


def CompareBaseToFrame(base, frame):
    lowest = 10000000000000
    for base_frame in base:
        base_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        base_frame = cv2.GaussianBlur(gray2, (21, 21), 0)

        if GetPixelDifference(GetThreshold(base_frame, frame)) < lowest:
            lowest = GetPixelDifference(GetThreshold(base_frame, frame))
    return lowest


if regiment:
    base_list_frames = GetBaseVideo(0)

cap = cv2.VideoCapture(0)

while True:
    ret1, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    ret2, frame2 = cap.read()
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    threshold = GetThreshold(gray1, gray2)
    if regiment:
        if (
            GetPixelDifference(CompareBaseToFrame(base_list_frames, gray2))
            > base_frame_differ_threshold
            and threshold_buffer_count <= 0
        ):
            threshold_buffer_count = threshold_encouragement_buffer
            print("giving encouragement: not stick to regimen")
            EncourageWrapper(1)
        elif (
            GetPixelDifference(CompareBaseToFrame(base_list_frames, gray2))
            > base_frame_differ_threshold
        ):
            threshold_buffer_count -= 1
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
            threshold_buffer_count = threshold_encouragement_buffer
            print("giving encouragement: timeout")
            EncourageWrapper(1)
        elif threshold_under_count >= threshold_movement_frame_count:
            threshold_buffer_count -= 1
        print(threshold_under_count)
        threshold_under_count += 1
    else:
        threshold_under_count = 0
        print("giving no encouragement")

    if (
        threshold_under_count + 10 >= threshold_movement_frame_count
        and threshold_under_count < threshold_movement_frame_count
    ):
        cv2.putText(
            frame2,
            "ENCOURAGEMENT INCOMING",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_4,
        )

    # cv2.imshow("threshold", threshold)
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
