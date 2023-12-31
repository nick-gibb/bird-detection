# Bird Detection from Video Files

![Bird Detection from Video Files](data/output/num_birds_detected_vs_video_duration.png)
![Example Bird Detection](data/output/frames/frame_19_at_11887.jpg)

This repository contains a Python app for bird detection in video files using the YOLOv5s model. It processes videos to detect birds and stores the extracted data in an SQLite database (output/birds.db).

## How to Run

Install required Python packages:

```bash
pip install -r requirements.txt
```

Execute main script:

```bash
python birds/main.py <path_to_video_file>
```

### Docker

Run the app in a Docker container.

Build Docker image:

```bash
docker build -t birds .
```

Launch Docker container:

```bash
docker run birds
```

## Project analysis

### Method

Videos are processed to detect birds and data is record in a SQLite database via:

- Object Detection: Employing YOLOv5 object detection model on video frames.
- Data Storage: Storing detected object data (class, confidence score, bounding box coordinates, timestamp, frame number) in SQLite database.
- Data Visualization: Fetching bird detection data from database and plotting number of detected birds over video duration.

### Libraries

Used Python libraries include:

- cv2: For video processing and bounding box drawing.
- pandas: For data manipulation/analysis.
- sqlite3: For SQLite database interaction.
- YOLOv5: For object detection.
- matplotlib and seaborn: For data visualization.

### Design Decisions

Multiple Python modules are used for the different functionalities, including file operations, database operations, video processing, and data visualization. Constants are used for file paths and frame intervals. SQLite is used for lightweight, serverless data storage. The entire application, including data processing and visualization, is run from a single main script.

### Improvement Suggestions

- Enhance error handling.
- Implement a CI/CD pipeline for automated testing, linting, formatting, and dev/prod deployment.
- Integrate with an upstream system that provides real-time or recorded video input streams.
- Evaluate the performance of different object detection models and fine-tune them for bird detection.
- Monitoring and alerting for uptime, performance, and business-relevant metrics (e.g. number of birds detected).
- Include unit tests for code reliability and maintainability.
- Optimize performance via parallel processing of video frames.
- Preserve existing data and append new ones instead of deleting the entire database each run.
- More sophisticated visualizations like heatmaps for bird detection locations.
- Improve data insertion speed by employing bulk inserts in database operations.
- Consider a robust database system like Azure SQL for larger scale applications, offering benefits like automated backups, high availability, and greater data and user handling capabilities.
