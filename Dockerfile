# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy your code into the container
COPY calculator.py .
COPY test_calculator.py .

# Install dependencies (if you have any)
# RUN pip install flask pytest

# Command to run when container starts
CMD ["python", "-c", "print('Calculator app is ready!')"]
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
