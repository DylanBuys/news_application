# News Application

This project is containerized using **Docker**, so you don’t need to install Python or MySQL locally to run it.

---

## Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (for Mac, Linux, or Windows)
- Clone this repository:

```bash
git clone https://github.com/DylanBuys/news_application
cd news_project

1. Build the Docker Image
    Make sure you are in the project root folder.
    -docker build -t newsapp .

2. Run the Docker Container
    -docker run -p 8000:8000 --name newsapp_container newsapp
    Access the application at http://localhost:8000

3. Perform migrations inside running container
    -docker exec newsapp_container sh
    -python manage.py migrate

Command to Stop and Remove the Container
Stop the running container:
    -docker stop newsapp_container
Remove the container:
    -docker rm newsapp_container
To find containers with no names:
    -docker ps


Notes
Ensure Docker Desktop is running before executing any commands.
