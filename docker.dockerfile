# Gunakan base image Python
FROM python:3.10-slim

# Set working directory di dalam container
WORKDIR /app

# Copy file dependency terlebih dahulu
COPY requirements.txt .

# Install dependency
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh project
COPY . .

# Expose port FastAPI
EXPOSE 8000

# Jalankan FastAPI menggunakan Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]