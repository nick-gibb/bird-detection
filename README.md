# Bird Detection from Video Files

![Bird Detection from Video Files](data/output/num_birds_detected_vs_video_duration.png)
![Example Bird Detection](data/output/frames/frame_19_at_11887.jpg)

This repository contains a Python application that performs bird detection from video files using the YOLOv5s model.

## How to Run

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

Run the main Python script:

```bash
python birds/main.py <path_to_video_file>
```

### Docker

The application can be run in a Docker container.

To build the Docker image:

```bash
docker build -t birds .
```

To run the Docker container:

```bash
docker run birds
```

## Project analysis

### Methodology

Video files are processed to detect birds and store captured data in a SQLite database. The methodology involves the following steps:

- Data Collection: The input video file.

- Data Cleaning: The output folder is cleaned by removing any existing files.

- Object Detection: The video is processed frame-by-frame using the YOLOv5 object detection model to detect birds. The frames are extracted at a certain interval, and each frame is then processed to detect birds.

- Data Storage: The data from the detection process (including class of detected object, confidence score, bounding box coordinates, timestamp, and frame number) is stored in a SQLite database.

- Data Visualization: Bird detection data is fetched from the database and a plot is generated showing the number of birds detected over the video duration.

### Libraries

The project uses several Python libraries:

- cv2: Used for video processing and drawing bounding boxes on frames.
- pandas: Used for data manipulation and analysis.
- sqlite3: Used to interact with the SQLite database.
- YOLOv5: Model for object detection.
- matplotlib and seaborn: Used for data visualization.

### Design Decisions

Separate Python modules are used for different functionalities such as file operations, database operations, video processing, and data visualization. The use of constants for file paths and frame intervals provides flexibility. The decision to use SQLite for data storage allows for lightweight and serverless data management.

### Improvement Suggestions

- Error Handling: More comprehensive and safer error handling could be implemented.

- Testing: The project currently does not include any unit tests.

- Performance Optimization: The current implementation processes videos frame by frame, which might not be efficient for large videos. An optimization could be to process multiple frames in
parallel.

- Database Operations: Currently, the entire database is deleted and recreated every time the program runs. Instead, existing data could be preserved and new data appended to the database.

- Data Visualization: The current visualization shows the number of birds detected per second. More sophisticated visualizations could be implemented, such as heatmaps showing where in the frame birds are most commonly detected.
