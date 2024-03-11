FROM python:3.10-slim

RUN apt-get -y update
RUN apt-get install -y ffmpeg

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD ["asr_api.py" ]