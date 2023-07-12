from .constants import OUTPUT_FOLDER
from pathlib import Path

def clean_output_folder(video_path: Path) -> None:
    """
    Validates the video file and prepares the output directory.

    Args:
    video_path (Path): Path of the input video file.

    Checks the existence of the input video file. If the output directory doesn't exist, creates it.
    Also, deletes any existing files in the output directory.
    """
    # Check if the input video file exists
    assert video_path.exists(), f"Video file {video_path} not found"

    # Create the output directory if it doesn't exist
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Delete existing files in the output directory
    for file in OUTPUT_FOLDER.iterdir():
        file.unlink()  # Remove the file
