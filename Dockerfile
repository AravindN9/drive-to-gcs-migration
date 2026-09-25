# Start with a lightweight version of Python 3.11
FROM python:3.11-slim

# Create a folder named /app inside the container and move into it
WORKDIR /app

# Copy the requirements file into the container and install the tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your actual Python script into the container
COPY main.py .

# Tell the container what command to run when it wakes up
CMD ["python", "main.py"]