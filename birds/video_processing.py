from pathlib import Path

import cv2
import pandas as pd
import torch


def load_model():
    """Load the YOLOv5s model"""
    return torch.hub.load("ultralytics/yolov5", "yolov5s")


def detect_birds(model, frame, bird_class_index):
    """Perform object detection on a given frame using YOLOv5."""
    results = model(frame)

    detections = [
        {
            "class": results.names[int(class_idx)],
            "confidence": conf.item(),
            "frame_bounding_box_coordinate_0": x1.item(),
            "frame_bounding_box_coordinate_1": y1.item(),
            "frame_bounding_box_coordinate_2": x2.item(),
            "frame_bounding_box_coordinate_3": y2.item(),
        }
        for x1, y1, x2, y2, conf, class_idx in results.xyxy[0]
        if int(class_idx) == bird_class_index
    ]
    return detections


def draw_bounding_boxes(frame, detections):
    """Draw bounding boxes on the frame for each detection."""
    for detection in detections:
        x1 = int(detection["frame_bounding_box_coordinate_0"])
        y1 = int(detection["frame_bounding_box_coordinate_1"])
        x2 = int(detection["frame_bounding_box_coordinate_2"])
        y2 = int(detection["frame_bounding_box_coordinate_3"])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame



def annotate_and_save_frame(frame, output_file_path, bird_count):
    """Save the frame as a JPEG file with bounding box annotations and bird count."""
    cv2.putText(
        frame,
        f"Birds: {bird_count}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    cv2.imwrite(str(output_file_path), frame)


def extract_and_detect_frames(video_path, output_folder, frame_interval):
    """Extract frames from a video file, perform object detection using YOLOv5, and save the annotated frames."""
    video = cv2.VideoCapture(str(video_path))

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {total_frames}")

    model = load_model()
    bird_class_index = next(i for i, v in model.names.items() if v == "bird")

    detections = []  # Initialize list to hold all detections
    for frame_index, frame in enumerate(get_frames(video, frame_interval)):
        # Get the current position in the video file in milliseconds
        timestamp_msec = str(round(video.get(cv2.CAP_PROP_POS_MSEC)))
        output_path = (
            Path(output_folder) / f"frame_{frame_index}_at_{timestamp_msec}.jpg"
        )

        object_detections = detect_birds(model, frame, bird_class_index)
        bird_count = len(object_detections)

        frame = draw_bounding_boxes(frame, object_detections)
        annotate_and_save_frame(frame, output_path, bird_count)
        for detection in object_detections:
            detection["timestamp"] = timestamp_msec
            detection["frame_number"] = frame_index
            detections.append(detection)

    # Release the video file
    video.release()
    df = pd.DataFrame(detections)
    return df


def get_frames(video, frame_interval):
    count = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        if count % frame_interval == 0:
            yield frame
        count += 1
