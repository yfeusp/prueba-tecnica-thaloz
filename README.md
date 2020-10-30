# Thaloz - Python Code Challenge
Thaloz Python code challenge #1

# What do you need?
* Docker
* Docker-compose

# Quickstart
To run the project:
```
docker-compose pull
docker-compose up --build -d
```

# What you should do
1. Create your Django project inside `/app`
2. Edit `./app/entrypoint.sh` and fill in your project name.
3. Create a `./app/requirements.txt`
4. Pull the images `docker-compose pull`
5. Run the project with `docker-compose up --build -d`

## Notes:
* Your database data will be in `/data`, this won't be commited.
* .env will be loaded automatically in your container.
* Django has autoreload and tracks codechanges.