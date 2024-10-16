# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app


# Install tzdata
RUN apt-get update && apt-get install -y tzdata

# Set the timezone to preferred region
ENV TZ=Europe/Stockholm
RUN ls -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo > /etc/timezone

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask app
CMD ["python3", "class_timer_flask.py"]
