FROM python:3.6-alpine

CMD python -m flask run --host=0.0.0.0 --port=80 

# Create user with home directory and no password and change workdir
RUN adduser -Dh /announce announce
WORKDIR /announce
# API will run on port 80
EXPOSE 8080
# Environment variable for config, use path for docker secrets as default
ENV ANNOUNCE_CONFIG=/run/secrets/announce_config

# Install bjoern and dependencies for install (we need to keep libev)
RUN apk add --no-cache --virtual .deps \
        musl-dev python-dev gcc git && \
    apk add --no-cache libev-dev && \
    pip install bjoern

# Copy files to /announce directory, install requirements
COPY ./ /announce
RUN pip install -r /announce/requirements.txt

# Cleanup dependencies
RUN apk del .deps

# Switch user
USER announce

# Start bjoern
CMD ["python3", "server.py"]
