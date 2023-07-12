import sqlite3

from .constants import DB_PATH


def initialize_db():
    """
    Creates tables in the SQLite database.

    Deletes and creates 'Classes', 'Frames' and 'Objects' tables.
    """
    # If the database already exists, delete it
    if DB_PATH.exists():
        DB_PATH.unlink()

    # Establish a connection to the SQLite database
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()

        # SQL command to create the Classes table
        create_classes_table_command = """
            CREATE TABLE Classes (
                class_id INTEGER PRIMARY KEY,
                class_name TEXT
            )
        """
        cursor.execute(create_classes_table_command)

        # SQL command to create the Frames table
        create_frames_table_command = """
            CREATE TABLE Frames (
                frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                frame_number INTEGER
            )
        """
        cursor.execute(create_frames_table_command)

        # SQL command to create the Objects table
        create_objects_table_command = """
            CREATE TABLE Objects (
                object_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER,
                frame_id INTEGER,
                bounding_box_coordinate_0 REAL,
                bounding_box_coordinate_1 REAL,
                bounding_box_coordinate_2 REAL,
                bounding_box_coordinate_3 REAL,
                confidence REAL,
                FOREIGN KEY (class_id) REFERENCES Classes (class_id),
                FOREIGN KEY (frame_id) REFERENCES Frames (frame_id)
            )
        """
        cursor.execute(create_objects_table_command)

        # Commit changes
        conn.commit()


def populate_database_tables(detections_df, classes_df):
    """
    Inserts detection and class data into the SQLite database.

    Args:
    detections_df (DataFrame): DataFrame containing detection data.
    classes_df (DataFrame): DataFrame containing class data.

    Inserts class data into 'Classes' table and detection data into 'Objects' table,
    linked to frame and class.
    """
    class_to_id_dict = classes_df.set_index("class_name")["class_id"].to_dict()
    grouped_detections = detections_df.groupby(["timestamp", "frame_number"])

    # Establish a connection to the SQLite database
    with sqlite3.connect(str(DB_PATH)) as conn:
        # Insert the classes into the Classes table
        classes_df.to_sql("Classes", conn, if_exists="append", index=False)

        cursor = conn.cursor()
        total_inserted_rows = 0
        for (timestamp, frame_number), group in grouped_detections:
            frame_number = int(frame_number)

            # Check if the frame already exists in the Frames table
            check_frame_exists_command = (
                "SELECT frame_id FROM Frames WHERE timestamp = ? AND frame_number = ?"
            )
            cursor.execute(check_frame_exists_command, (timestamp, frame_number))

            frame_result = cursor.fetchone()

            if frame_result is None:
                # If the frame does not exist, insert it into the Frames table
                insert_frame_command = (
                    "INSERT INTO Frames (timestamp, frame_number) VALUES (?, ?)"
                )
                cursor.execute(insert_frame_command, (timestamp, frame_number))
                frame_id = cursor.lastrowid  # Get the id of the newly inserted frame
            else:
                frame_id = frame_result[0]  # If the frame exists, get its id

            # For each object in this frame, insert the object into the Objects table
            for _, row in group.iterrows():
                class_id = class_to_id_dict[
                    row["class"]
                ]  # Get the class_id for this object
                bounding_box_coordinates = row[
                    [
                        "frame_bounding_box_coordinate_0",
                        "frame_bounding_box_coordinate_1",
                        "frame_bounding_box_coordinate_2",
                        "frame_bounding_box_coordinate_3",
                    ]
                ]
                confidence = row["confidence"]

                insert_object_command = """
                    INSERT INTO Objects (class_id, frame_id, bounding_box_coordinate_0, bounding_box_coordinate_1, bounding_box_coordinate_2, bounding_box_coordinate_3, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(
                    insert_object_command,
                    (class_id, frame_id, *bounding_box_coordinates, confidence),
                )

                total_inserted_rows += 1
                if total_inserted_rows % 50 == 0:
                    print(f"Inserted {total_inserted_rows} rows so far")

        # Commit changes
        conn.commit()
