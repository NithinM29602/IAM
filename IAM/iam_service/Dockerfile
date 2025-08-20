FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the rest of the application
COPY . .

EXPOSE 8081

# Use absolute path and ensure Python path is set correctly
CMD ["python", "-m", "app.main"]