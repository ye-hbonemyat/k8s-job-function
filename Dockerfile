FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY api-endpoint.py .

CMD ["python", "api-endpoint.py"]
