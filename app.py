import cv2
import datetime
import os
import time

# Create 'assets' directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Initialize the background subtractor
back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=32, detectShadows=True)

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Variables for recording
recording = False
out = None
last_motion_time = None
no_motion_threshold = 5  # Time in seconds to stop recording after no motion

# Define the width and height for resizing
resize_width = 640
resize_height = 480

# Set the frame rate
frame_rate = 20.0

# Parameters for contour filtering
min_contour_area = 1000
max_contour_area = 50000

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    frame_resized = cv2.resize(frame, (resize_width, resize_height))
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    fg_mask = back_sub.apply(gray)
    blurred = cv2.GaussianBlur(fg_mask, (5, 5), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    frame_display = frame_resized.copy()
    frame_record = frame_resized.copy()

    new_motion_detected = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if min_contour_area < area < max_contour_area:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame_display, (x, y), (x+w, y+h), (0, 255, 0), 2)
            new_motion_detected = True

    current_time = time.time()
    
    if new_motion_detected:
        last_motion_time = current_time
        if not recording:
            recording = True
            recording_start_time = current_time
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            out = cv2.VideoWriter(f'assets/motion_{timestamp}.avi', cv2.VideoWriter_fourcc(*'MJPG'), frame_rate, (resize_width, resize_height))
        
        timestamp_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame_record, timestamp_text, (10, frame_record.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        if recording:
            out.write(frame_record)
    else:
        if recording:
            if current_time - last_motion_time >= no_motion_threshold:
                recording = False
                out.release()
                out = None

    timestamp_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.putText(frame_display, timestamp_text, (10, frame_display.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow('Motion Detection', frame_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if recording:
    out.release()
cv2.destroyAllWindows()
