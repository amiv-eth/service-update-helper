FROM python:3-alpine

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Add curl for additional requests from the CI job
RUN apk --no-cache add curl

COPY ./update.py /update.py
CMD ["/update.py"]
