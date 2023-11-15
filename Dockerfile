FROM python:3.10

WORKDIR /

RUN mkdir -p ./logs

COPY ./config ./config
COPY ./utils ./utils
COPY ./requirements.txt ./requirements.txt
COPY ./main.py ./main.py
COPY ./platforms ./platforms

RUN apt-get update && apt-get install libgl1 -y

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["python", "./main.py"]