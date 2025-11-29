# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .
RUN apt-get update
RUN apt-get install libmagic1 -y

# Expose the port Flask will run on
EXPOSE 5000

# Remember to Run the app with Gunicorn for production
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "api.v1.app:app"]
