import argparse
import ssl
from pathlib import Path

import pandas as pd

from .constants import DF_CLASSES_PATH, FRAME_INTERVAL, OUTPUT_FOLDER
from .data_visualization import visualize_bird_detections
from .database_operations import initialize_db, populate_database_tables
from .file_operations import clean_output_folder
from .video_processing import extract_and_detect_frames

# Disabling SSL verification
ssl._create_default_https_context = ssl._create_unverified_context


def execute_program(video_file_path):
    """
    Main function to execute all steps of the program.
    """
    clean_output_folder(video_file_path)
    detected_objects_df = extract_and_detect_frames(
        video_file_path, OUTPUT_FOLDER, FRAME_INTERVAL
    )

    initialize_db()
    class_data_df = pd.read_csv(DF_CLASSES_PATH)
    populate_database_tables(detected_objects_df, class_data_df)
    visualize_bird_detections()

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Process a video file for bird detection."
    )
    arg_parser.add_argument("video_file", type=str, help="Path to the video file.")
    parsed_args = arg_parser.parse_args()

    execute_program(Path(parsed_args.video_file))
