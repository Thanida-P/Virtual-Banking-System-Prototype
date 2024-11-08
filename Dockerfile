# Base image
FROM python:3.11.0

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the wait-for-it script is executable
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Set the environment variable for the service (can be overridden at runtime)
# ENV SERVICE authenticator  # Default service; change via docker-compose

# Expose the port
EXPOSE 8000

# Run app.py when the container launches
CMD ["wait-for-it", "db:3306", "--timeout=120", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
