
FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg aria2

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "run.sh"]
