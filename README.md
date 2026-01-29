# news_application
1. First create the virtual enviroment, install from requirements.txt (pip install -r requirements.txt)
2. Then you would want to run migrations
3.      -navigate to news_project(same directory as manage.py)
4.      -run python manage.py makemigrations, then migrate
5.  Once migrations have been done correctly, begin to build application
6.      -run docker build -t news-app:latest ./  (to build app)
7.      -then run docker run -p 8000:8000 --name news-app news-app:latest
8.      -then click on the link in the terminal.
