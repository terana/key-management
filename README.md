# Key Managements Service
A simple key managements service.

### Running
This service is based on Docker containers orchestrated by Docker Compose. To start the server, try
```
docker-compose up --build 
```
To execute a django command inside the gunicorn container, try
```
docker exec -it kms_gunicorn_1 python manage.py <your command here>
```
To access the server, try sending `GET` request to `http://127.0.0.1:8080/api`

### Repository
The project layout is as follows:
```
key-management/
    nginx/ # nginx container contents, forget about it.
    gunicorn/
        manage.py
        kms/  # some djando app settings, you won't need them too frequently.
        api/ # this is something interesting, your logical modules are here!
            <your module>/ # your logical module
                __init__.py
                tests.py
                urls.py
                views.py
                <some other file with logic>
                <some other module with logic>/
                    __init__.py   
```
