FROM python:3.9

WORKDIR /code

COPY ./dockerrequirements.txt /code/dockerrequirements.txt

RUN pip install --no-cache-dir --upgrade /code/dockerrequirements.txt 

COPY ./TrainYourOwnYOLO /code/TrainYourOwnYOLO