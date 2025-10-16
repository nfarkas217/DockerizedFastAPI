FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 
EXPOSE 8080

RUN useradd app
USER app

CMD ["uvicord", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]