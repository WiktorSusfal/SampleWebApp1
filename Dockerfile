FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 5000

ENV NAME World

CMD ["python", "main.py"]