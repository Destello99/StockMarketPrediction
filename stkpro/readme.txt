Commands to run before working:

https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-database#install-redis - To run Redis server

python manage.py runserver

celery -A stkPro beat -l INFO

celery -A stkPro worker -l INFO --concurrency 1 -P solo