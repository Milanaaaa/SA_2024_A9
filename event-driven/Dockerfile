FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/ ./services/
COPY build.sh .

RUN chmod +x build.sh

EXPOSE 5000

CMD ["./build.sh"]
