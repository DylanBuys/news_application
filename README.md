# news_application
## How to run this application

1. This project is containerized with docker, meaning you don't need to install Python or MySQL locally to run it
2.
3. ## Prerequisites
4. *Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
5. *Clone this repository
6.    -git clone https://github.com/DylanBuys/news_application.git

8. Build the image
9. Open your terminal in the project root folder and run:
10.    -'''bash docker build -t news-app .
11. Run the container
12.    -docker run -p 8000:8000 --name news-app:latest
