FROM python:3.7.3-alpine

WORKDIR /app

COPY requirements.txt .
COPY docker_app.py .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "docker_app.py" ]