import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture('AngleDetectAirfoil_1920x1080.mp4')

# Get the width and height of the video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set the new width and height
new_width = 1366
new_height = 768

if cap.isOpened() == False:
    print('Unable to read camera feed')

while cap.isOpened():
    # Read the next frame from the video
    ret, frame = cap.read()

    if ret == True:

        # Resize the frame
        new_frame = cv2.resize(frame, (new_width, new_height))

        # Convert the frame to grayscale
        gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

        # Blur the frame to reduce high frequency noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # Use Canny edge detection to detect edges in the frame
        edges = cv2.Canny(blurred, 50, 150)

        # Use Hough line detection to detect lines in the frame
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

        # Calculate the angle of each line
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            angles.append(angle)

        # Calculate the average angle
        angle = sum(angles) / len(angles)

        # Convert the angle to a string and draw it on the frame
        angle_str = f"Angle: {angle:.2f}"
        cv2.putText(new_frame, angle_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

        # Display the resulting frame
        cv2.imshow('Frame', new_frame)
        cv2.imshow('Edges', edges)

        # Press Q on keyboard to  exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()
# Closes all the frames
cv2.destroyAllWindows()

