# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables for Flask
ENV FLASK_APP=stock_market
ENV FLASK_ENV=production


# Set environment variable for database URL
ENV DATABASE_URL=postgresql://postgres:root@localhost/Stocks

# Set the working directory in the container
WORKDIR /stock_market

# Copy your application code into the container
COPY . /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app will run on
EXPOSE 5000

# Start the Flask application
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
