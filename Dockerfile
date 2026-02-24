# Dockerfile for Streamlit Career Assistant Platform
# Python base image
FROM python:3.14

# Set working directory
WORKDIR /app

# Copy requirements and app files
COPY requirements.txt ./
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py"]
