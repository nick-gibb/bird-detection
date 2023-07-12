import sys
sys.path.append('.')
from birds import video_processing
import cv2


def test_get_frames():
    video = cv2.VideoCapture()
    frame_interval = 1
    frames = list(video_processing.get_frames(video, frame_interval))
    assert len(frames) == 0  # Expect 0 as no real video is provided
