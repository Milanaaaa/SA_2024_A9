FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/ ./services/

EXPOSE 5000

CMD ["python", "services/filter_service.py"]
