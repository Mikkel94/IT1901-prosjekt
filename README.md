# IT1901-prosjekt
Prosjektarbeid IT1901 H17


## Requirements

Django 1.11.3

Python 3.6.2

Argon2 password hasher (skriv 'pip install django[argon2]' i terminal)

BCrypt password hasher ('skriv pip install bcrypt' i terminal)


## How to join the project

1. Go to https://www.anaconda.com/download/
2. Download Python 3.6 version for appropriate platform
3. In terminal type 'conda install django', follow instructions given in shell, this should install everything you need
4. Clone project into your folder
5. To start up site on you computer go project root in terminal. Type python manage.py runserver
6. Set project root to the first directory in this project named festival to avoid unresolved reference errors
7. Set project interpreter to the python version previously downloaded with anaconda

## Project structure

All html pages should extend base.html
All html pages are placed into the directory named templates
All static files (css/js/images etc) are placed into the corresponding subdirectory of directory named static
Views are linked to in each app, each apps view is included in the projects root file urls.py

## How to contribute to the project
```bash
pip install virtualenvwrapper
git clone https://github.com/Mikkel94/IT1901-prosjekt.git
cd IT1901-prosjekt
mkvirtualenv festival
workon festival
pip install -r requirements.txt
```

## How to start server to see everything:
1. Follow guide above to setup environment
2. In django root folder:
  1. python manage.py makemigrations
  2. python manage.py migrate
  3. python manage.py loaddata init
3. Go to url: localhost:8000/admin
4. Log in with usr: Admin, pw: Test123test
5. Go to Employees model here, and you will see all the usernames you can use, names correspond to their position as workers at the festival. 
6. All passwords are Test123test.
7 More info about the database that is also readable is in the file init.json.
