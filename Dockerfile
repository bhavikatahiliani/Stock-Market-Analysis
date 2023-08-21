
# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables for Flask
ENV FLASK_APP=stock_market
ENV FLASK_ENV=production

# Set environment variable for database URL
ENV DATABASE_URL=postgresql://postgres:root@localhost/Stocks

# Set the working directory in the container
WORKDIR /stock_market

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# install psycopg2 binary package
RUN apt-get install -y libpq-dev
RUN pip install --no-cache-dir psycopg2==2.9.1

# Copy your application code into the container
COPY . /stock_market

# Expose the port your Flask app will run on
EXPOSE 5000

# Start the Flask application
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
