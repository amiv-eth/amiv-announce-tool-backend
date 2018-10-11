# AMIV Announce-Tool Backend

## How to run this Flask app

### Development

To start the app locally for development, do the following:

1. Clone this repo
2. Create a python3 virtual environment: `virtualenv venv` (you might specify your python3 binary with `--pytho=/usr/bin/python3`)
3. Activate the virtual environment: `source venv/bin/activate`
4. Install the requirements inside the venv: `pip install -r requirements.txt`
5. Set the following environment variables: `export FLASK_APP="local.py"` and `export FLASK_DEBUG=1`
6. Create the configuration file with all the juicy secrets inside in `instance/config.py`. You might copy the file `instance/config.example.py`.
7. Run the flask app: `flask run`

### Production (w/o docker)

To start the app in a production environment, do the following:

1. clone this repo
2. Install the requirements: `pip install -r requirements.txt`
3. Set the following environment variable: `export FLASK_APP="run.py"`
4. Create the configuration file with all the juicy secrets inside in `instance/config.py`. You might copy the file `instance/config.example.py`.
5. Run the flask app: `python3 server.py`

### Production (w/ docker)

Create an Announce-Tool Backend service and give it access to the config using a docker secret:

```bash
# Create secret
docker secret create announce_config <path/to/announce_config.py>

# Create new Announce-Tool Backend service with secret
# Map port 80 (host) to 8080 (container)
docker service create \
    --name amivannounce  -p 80:8080 --network backend \
    --secret announce_config \
    amiveth/amiv-announce-tool-backend
```

If you want to use a different name for the secret (or cannot use secrets and have to mount the config manually), you can use the environment variable ANNOUNCe_CONFIG to set the config path in the Announce container.

## Which endpoints are available

### /

This returns error "400 - Wrong Ressource" to prevent uninteded calls to the app

### /mailer

This is the endpoint which is used to send mails with this backend.

It expects three variables via POST:

1. "msg" - This contains the mail itself
2. "sub" - The subject of the mail
3. "token" - The AMIV API token to be used for authentication

### /englishman

Here error 418 from RFC 2324 is implemented
