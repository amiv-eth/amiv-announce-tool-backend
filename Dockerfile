from python:3.6-alpine

ENV FLASK_APP app.py
ENV FLASK_DEBUG true
EXPOSE 80

RUN pip install Flask

COPY ./app.py /app.py
COPY ./InvalidUsage.py /InvalidUsage.py

WORKDIR /

CMD python -m flask run --host=0.0.0.0 --port=80 

