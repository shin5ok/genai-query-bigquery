FROM python:3.8-slim

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=on


CMD ["chainlit", "run", "main.py", "--port=8080", "--host=0.0.0.0", "--headless"]
