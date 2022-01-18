release: python manage.py migrate
web: gunicorn --bind :8000 --workers 3 --threads 2 Shopify_Data_Engineer_Intern_Challenge_Summer_2022.wsgi:application