FROM python:3.9-slim

RUN apt update && apt install gcc -y

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./bot.py" ]
