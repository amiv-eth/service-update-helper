FROM python:3-alpine

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./update.py /update.py
CMD ["/update.py"]
