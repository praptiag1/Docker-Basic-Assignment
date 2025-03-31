# Docker-Basic-Assignment
This is a multiservice docker assignment that includes three services: web, db and cache. Build customer Dockerfiles for each service, push it on docker hub and using it in docker compose to run the application in local system.

# Multi-Service User Wishlist App

## Overview

This project is a multi-service User's Wishlist Application built using **Flask**, **Redis**, and **PostgreSQL**. The application allows users to:
 * Add items to their wishlist
 * Delete items from their wishlist
 * Update wishlist items
 * View their wishlist

The application consists of three services:

1. **Flask Web Service**: Handles user interactions and provides RESTful API endpoints.
2. **PostgreSQL Database Service**: Stores wishlist data persistently.
3. **Redis Cache Service**: Improves performance by caching frequently accessed data.

All services run in **Docker containers**, using custom **Dockerfiles**, and are orchestrated using **Docker Compose**. The images are pushed to **Docker Hub** for easy deployment.

## Setup Instructions:
1. **Clone repository**
   - git clone https://github.com/praptiag1/Docker-Basic-Assignment
   - cd Docker-Basic-Assignment
2. **Run the Application**
Start all services using Docker Compose:
    - docker-compose up -d
This will start the Flask app, PostgreSQL database, and Redis cache in detached mode.
3. **Verify Running Containers**
    - docker ps
4. **Access the Application**
     http://localhost:5000
## Project Workflow
The Project contains 3 custome DockerFiles for web, database and cache services as Dockerfile.web, Dockerfile.db, Dockerfile.cache respectively.
1. The images are build:
    - docker build -t my-web-app -f Dockerfile.web .
    - docker build -t my-db -f Dockerfile.db .
    - docker build -t my-redis -f Dockerfile.cache .
2. List images:
   - docker images
     ![image](https://github.com/user-attachments/assets/cd93dcde-e7b8-4004-9e5a-699d143c770a)
3. Login to docker hub and enter credentials:
   - docker login
4. Tag images
    - docker tag my-web-app praptiag11/my-web-app:v1.0
    - docker tag my-db praptiag11/my-db:v1.0
    - docker tag my-redis praptiag11/my-redis:v1.0
      ![image](https://github.com/user-attachments/assets/61d66122-89af-4eb4-aa05-8d07bca519d9)
5. Push images to Docker Hub:
    - docker push praptiag11/my-web-app:v1.0
    - docker push praptiag11/my-db:v1.0
    - docker push praptiag11/my-redis:v1.0
      ![image](https://github.com/user-attachments/assets/e430dc7b-56e8-4e41-bb24-8d4f96a70f91)
6. Make docker compose YAML file
7. Run Application:
    - docker compose up -d
8. List all running containers:
    - docker ps
9. Access application:
     - http://localhost:5000

## Docker Hub
All images are pushed to Docker Hub for easy deployment. Pull them using:
  - docker pull praptiag11/my-web-app:v1.0
  - docker pull praptiag11/my-db:v1.0
  - docker pull praptiag11/my-redis:v1.0
## Web Interface
1. **Home Page**
   ![image](https://github.com/user-attachments/assets/2492d772-0479-4dca-a78c-3990223d0d36)
   
2. **Add items into wishlist**
   ![image](https://github.com/user-attachments/assets/8cda3220-c14b-4bec-9c42-61aade927080)
   
3. **Fetch the wishlist**
   ![image](https://github.com/user-attachments/assets/383431ed-351b-4213-b81d-f8cfdd67db2d)

4. **List of all Users**
   ![image](https://github.com/user-attachments/assets/860d9de2-3512-424e-b04b-d7c622b1ae21)

5. **Edit Wishlist**

   ![image](https://github.com/user-attachments/assets/fc3955c7-aa5d-46c4-969e-51bb333c77d7)

6. **Delete Wishlist**

   ![image](https://github.com/user-attachments/assets/807ca1e9-1331-4c06-acca-fb97152953f4)

## Docker Logs
The log of a running container can be seen using:
- docker logs <container_name>

## Docker network
New network can be created using 
- docker network create <network_name>
List all the network using
- docker network ls
Inspect the network using:
- docker network inspect <network_name>


