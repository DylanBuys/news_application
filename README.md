# News Application

This project is containerized using **Docker**, so you don’t need to install Python or MySQL locally to run it.

---

## Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (for Mac, Linux, or Windows)
- Clone this repository:

```sh
        git clone https://github.com/DylanBuys/news_application
        cd news_application/news_project
```


## 1. Build the Docker Image
    Make sure you are in the project root folder.
       ```sh
               docker build -t newsapp .
       ```

## 2. Run the Docker Container
       ```sh
             docker run -p 8000:8000 --name newsapp_container newsapp
       ```
    Access the application at http://localhost:8000

## 3. Perform migrations inside running container
       ```sh
            docker exec newsapp_container sh
            python manage.py migrate
       ```

### Stop the running container:
    ```sh
        docker stop newsapp_container
    ```
### Remove the container:
    ```sh
         docker rm newsapp_container
    ```
### To find containers with no names:
    ```sh
         docker ps
    ```


Notes
Ensure Docker Desktop is running before executing any commands.
