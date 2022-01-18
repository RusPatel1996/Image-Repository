# Instructions
\
*KNOWN ISSUES: the hosted application is very slow to upload images as it's using django server rather than gunicorn on Heroku with no multiprocessing. I did not have enough time to configure gunicorn settings properly or utilize multiprocessing with Celery or Django Q.*
\
*If you want a faster experience with this application then please follow the steps below and run it from a virtual python environment*

**Simply access this heroku link: https://shopify-data-eng-intern.herokuapp.com**
\
\
\
If you run into any problems accessing the website then you should be able to run it locally by following the listed steps: \
*Note: The following steps assume you are using windows*

1. Install Python > 3.4, so you can access pip package manager: https://www.python.org/downloads/
2. Make sure python and pip are on PATH env variables: https://docs.python.org/3/using/windows.html
3. Download git bash terminal: https://git-scm.com/download/win
4. Download this repository on your desktop, unzip it, and open the git bash terminal within the repo's directory
5. Install Virtualenv using ```python -m venv env```
7. Enter the virtual environment using ```source venv/Scripts/activate```
8. Install all dependencies using ```pip install -r requirements.txt```
10. The database should be ready but in case tables are missing, run ```python manage.py makemigrations``` followed by ```python manage.py migrate```
11. run ```python manage.py runserver``` and open the development server on the url given (usually http://127.0.0.1:8000/)

Some Lessons Learned:
- Always consider the file size, type, and contents as a security measurement.
- Downsizing images to store in the database and showing thumbnails of the downsized images are good ways to gain performance and save storage space.
- Utilizing multiprocessing and cache is paramount to a well-designed GUI based Image Repository Application. I was unable to configure cache properly as it was saving the initial no image uploaded page in the cache and reloading it even after images were inserted. 
- Properly use Git Branches to develop new features and configurations (don't crowd the master branch with unecessary commits)
- Using PostgreSQL from get go as Heroku utilizes PostgreSQL for Django deployments.
- Using a Linux environment to create the application for easier deployment to heroku or using Docker on windows. In either case, including redis and running gunicorn would prove to be easier.
