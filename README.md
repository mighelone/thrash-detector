# Thrash detector app

The **thrash detector** app is composed by two components, each of them running on a seperate docker container.

## Run components

The backend/frontend can be run using containers with `docker` and `docker-compose`.

First build the docker image:

```console
$ docker-compose build
```

and then, launch the services with:

```console
$ docker-compose up -d
```

check if the services are running:

```console
$ docker-compose ps

        Name                      Command               State           Ports         
--------------------------------------------------------------------------------------
recycleye_backend_1    gunicorn --workers=2 backe ...   Up      0.0.0.0:28000->8000/tcp
recycleye_frontend_1   gunicorn --workers=2 front ...   Up      0.0.0.0:28100->8100/tcp
```

The frontend is accessible from the browser pointing to `http://127.0.0.1:28100`, while the backend using `http://127.0.0.1:28000`.

If the ports 28000 and 28100 are already used change them in the `docker-compose.yml` file, under the `ports` field.

The logs of the containers can be checked by (calling the desired service):

```console
$ docker-compose log -f frontend
```
## Components

### Backend

The backend component serves a REST-API, returning the results of the `detect_thrash` function.

The API is exposing a POST method, accepting two files under the values `image1` and `image2`

```console
$ curl -X POST http://localhost:28000/api   \
    -F 'image1=@./images/2020-05-08-221615.jpg' \
    -F 'image2=@./images/2020-05-08-221627.jpg' \
    --output res.jpg
```

Otherwise the API can be access using the python script `scripts/request_api.py`. 
Install first all the required packages with

```console
$ pip install -r requirements.txt
```
And then call the script

```console
$ python scripts/request_api.py \
    ./images/2020-05-08-221615.jpg \
    ./images/2020-05-08-221627.jpg \
    --url http://localhost:28000 \
    --output res.jpg
```

### Frontend

The frontend component is an web-based interface for accessing the `detect_thrash` backend API.
Point your browser to http://localhost:28100