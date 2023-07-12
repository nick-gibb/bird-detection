# Start with the official Python 3 base image
FROM python:3

# Set /app as the working directory in the Docker image
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements.txt first, to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Default command to run the application
CMD ["python", "-m", "birds.main", "./data/input/Pigeon - 6093.mp4"]
