# goit-pythonweb-hw-03
Small app with Python http-server. Add Dockerfile with the purpose to run the App in the Docker container.

#### To run app in the docker container follow the next steps:

1. Run Docker Desktop

2. Build docker image running the next command from the app root folder:

```
docker build --no-cache . -t IMAGE_NAME
```

3. Run an image in the container using volumes to store data outside the container:

```
docker run -itd -p 3000:3000 -v storage:/app/storage IMAGE_NAME
```

This app will be running at http://localhost:3000.
The command above with the flag ```-v``` will create volume with the name ```storage``` outside the container and link it to the container folder ```app/storage```. In this way we will not lose our data even when we delete container or run an app in another one

#### To run the app locally:

1. Create virtual environment

```
python3 -m venv env
```

2. Activate virtual environment

```
source env/bin/activate
```

3. Install dependancies from requirements.txt

```
pip install -r requirements.txt
```

4. Run main.py:

```
python3 main.py
```