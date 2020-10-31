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
* Django has autoreload and tracks codechanges, so if you edit your code with the containers up it will update 
without building.

## Code Assigment 

We want to implement a user microservice which must have the following routes

* POST /user crates a user in the DB.

* PUT /user updates user data in the DB.

* GET /user/:id returns the user by Id.

* DELETE /user/:id deletes the user from DB.

* POST /login for user login. Every time the user logs into the system we store the login event in the DB. 

* GET /activityReport/day This route will return the total logging events by user by day.

```
Jhon, 24/03/2020, 3
Jhon, 25/03/2020, 5
Jhon, 10/04/2020, 1
```
    
* GET /activityReport/month This route will return the total logging events by user by month.

```
Jhon, 03/2020, 8
Jhon, 04/2020, 1
```

Database schema definition is totally up to you, the only requirement is to use Postgres. 
Please add a DDL script to recreate the schema.
