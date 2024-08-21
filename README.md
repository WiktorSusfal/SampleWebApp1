# Summary 

Sample Template Web App built using Flask. 

* Python version: 3.11
* Flask version: 3.0.3

# Components

Development is done using Docker containers. Each component of the application runs in separate container. 

* Flask web application - "python:3.11-slim" image
* nginx server - default latest nginx image
* PostgreSQL database - "postgres:13" image

# Features

Web Application supports pages for:

* registering new user 
* logging user 
* viewing user list
* viewing user log in attempts history 

Application supports:

* request over HTTPS (HTTP disabled)
* user password policies
* user account locking mechanism 
* request rate limiting for core pages 
* log in attempts logging 
* information access based on user role 