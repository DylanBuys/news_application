# news_application
## How to run this application

This project is containerized with docker, meaning you don't need to install Python or MySQL locally to run it

## Prerequisites
*Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
*Clone this repository
     -git clone (repo-link)

1. Build the image
   Open your terminal in the project root folder and run:
       -'''bash docker build -t news-app .
2. Run the container
       -docker run -p 8000:8000 --name news-app:latest
