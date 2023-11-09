FROM python:latest

WORKDIR /app

COPY . .

CMD ["echo", "OK"]