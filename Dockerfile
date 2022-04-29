FROM python:3.10.4

COPY ./requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /mockend

WORKDIR /mockend
RUN python3 setup.py install

CMD ["bash","-c", "mockend -c conf.json"]