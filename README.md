# News Application

This project is containerized using **Docker**, so you don’t need to install Python or MySQL locally to run it.

---

## Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (for Mac, Linux, or Windows)
- Clone this repository:

```bash
git clone https://github.com/DylanBuys/news_application
cd news_project

Build the Docker Image
Make sure you are in the project root folder.

Mac / Linux:
docker build -t newsapp .

Windows (PowerShell / CMD):
docker build -t newsapp .

Run the Docker Container
Mac / Linux:
docker run -p 8000:8000 --name newsapp_container newsapp
Windows (PowerShell / CMD):
docker run -p 8000:8000 --name newsapp_container newsapp
Access the application at http://localhost:8000

Perform migrations inside running container
docker exec newsapp_container sh
python manage.py migrate

Stop and Remove the Container
Stop the running container:
docker stop newsapp_container
Remove the container:
docker rm newsapp_container
To find containers with no names:
docker ps

Rebuild the Image After Changes
If you make changes to the code, rebuild the image:
docker build -t newsapp .

Notes
This setup works on Mac, Linux, and Windows.
Ensure Docker Desktop is running before executing any commands.
The application is exposed on port 8000 by default.
