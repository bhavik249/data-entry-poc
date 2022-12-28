# data-entry-poc

1. Clone the source code from GitHub
```
git clone git@github.com:bhavik249/data-entry-poc.git
cd data-entry-poc
```

2. Building and using virtual environment 
```
python3 -m venv env
source env/bin/activate
```

3. Install the requirements package
```
pip install -r requirements.txt
```

4. Migrate the database

```
python manage.py migrate
```

5. Create a super user with following command; So you can login into the admin site:

```
python manage.py createsuperuser
```

6. Run server

```
python manage.py runserver
```

You can go to the http:///127.0.0.1:8000 to view the application running.