import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .constants import DB_PATH, OUTPUT_DIRECTORY


def fetch_bird_data() -> pd.DataFrame:
    """
    Fetch bird detection data and their timestamps from an SQLite database.

    Returns:
        A DataFrame containing bird detection data with timestamps.
    """
    with sqlite3.connect(str(DB_PATH)) as conn:
        bird_data_df = pd.read_sql_query(
            """
            SELECT Objects.*, Frames.timestamp
            FROM Objects
            JOIN Frames ON Objects.frame_id = Frames.frame_id
            WHERE Objects.class_id = (SELECT class_id FROM Classes WHERE class_name = 'bird')
            """,
            conn,
        )

    bird_data_df["timestamp"] = bird_data_df["timestamp"].astype(int)
    bird_data_df["timestamp_seconds"] = bird_data_df["timestamp"] / 1000

    return bird_data_df


def visualize_bird_detections() -> None:
    """
    Fetch bird detections data, compute the bird counts per second and generate a plot.
    """
    bird_data_df = fetch_bird_data()

    bird_counts_per_second = (
        bird_data_df["timestamp_seconds"].value_counts().sort_index()
    )

    create_and_save_plot(bird_counts_per_second)


def create_and_save_plot(bird_counts: pd.Series) -> None:
    """
    Generate and save a line plot for the given bird counts data.

    Args:
        bird_counts (Series): Bird counts per second.
    """
    plt.figure(figsize=(12, 8))
    sns.lineplot(x=bird_counts.index, y=bird_counts.values, color="blue", linewidth=2.5)

    for x, y in bird_counts.items():
        plt.text(x, y, str(y), color="black", fontsize=12, ha="center", va="bottom")

    plt.title("Number of Birds Detected Over Video Duration", fontsize=20)
    plt.xlabel("Video Duration (seconds)", fontsize=16)
    plt.ylabel("Number of Birds Detected", fontsize=16)
    plt.grid(True)

    output_path = Path(OUTPUT_DIRECTORY) / "num_birds_detected_vs_video_duration.png"
    plt.savefig(output_path)
