# Use Python 3.9 base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ /app/

# Expose port (if needed)
EXPOSE 443

# Command to run the application
CMD ["python", "main.py"]
