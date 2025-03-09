# FastAPI Blog Application

This is a simple FastAPI application for managing blog posts. It supports operations like creating, reading, updating, and deleting blog posts.

## Table of Contents
- [Clone the Repository](#clone-the-repository)
- [Install Dependencies](#install-dependencies)
- [Run the Application Locally](#run-the-application-locally)
- [Run the Application in Docker](#run-the-application-in-docker)
- [Swagger](#swagger)

## Clone the Repository

Clone this repository to your local machine using the following command:
```bash
git clone git@github.com:NitheshHS/fast_api_app.git
```

## Install Dependencies
Install the required dependencies using the following command:
```bash
pip3 install -r requirements.txt
```

## Run the Application Locally
To run the application locally, open your terminal and use the following command. By default, the app will run on port 8000:
```bash
uvicorn blogs.main:app
```

## Run the Application in Docker
To run the application in Docker, follow these steps:
1. Build the Docker image:
```bash
docker build -t my-blog-app .
```
2. Run the app on a specified host and port:
```bash
docker run -d -p 8000:8000 .
```

## Swagger
Once the application is running, you can view the Swagger documentation at the following URL:
```angular2html
http://0.0.0.0:8000/docs
```




