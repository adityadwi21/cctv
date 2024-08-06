# Motion Detection and Recording System

This repository contains a Python script for detecting motion using a webcam and recording the video when motion is detected. The recorded videos are saved in the `assets` directory with a timestamp.

## Features

- Real-time motion detection using OpenCV.
- Recording starts when motion is detected and stops after no motion is detected for a specified duration.
- Recorded videos are saved with a timestamp in the filename.
- Displays the motion detection frame with bounding boxes around detected motion.

## Requirements

- Python 3.x
- OpenCV

## Installation

1. Clone the repository:

```sh
git clone https://github.com/adityadwi21/cctv.git
cd cctv
```

2. Install the required dependencies:

```sh
pip install opencv-python
```

## Usage

Run the script:

```sh
python app.py
```

The script will start the webcam and display the video feed with motion detection. When motion is detected, a green bounding box will be drawn around the moving object. The video will be recorded and saved in the `assets` directory.

## Script Details

- The script creates an `assets` directory if it does not exist.
- Uses a background subtractor (`cv2.createBackgroundSubtractorMOG2`) for motion detection.
- Resizes the frame to 640x480 pixels.
- Sets the frame rate to 20.0 fps.
- Defines minimum and maximum contour area for filtering motion.
- Records video in `MJPG` format when motion is detected and saves it in the `assets` directory with a timestamp in the filename.
- Stops recording if no motion is detected for 5 seconds.
- Displays the current timestamp on the video frames.

## Exiting the Script

Press `q` to quit the video feed and stop the script.

## Example

```sh
python app.py
```

When the script is running, it will display the video feed with detected motion highlighted by a green bounding box. The recorded videos will be saved in the `assets` directory with filenames like `motion_YYYYMMDD_HHMMSS.avi`.
