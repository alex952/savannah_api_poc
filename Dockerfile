FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "/app/main.py"]
