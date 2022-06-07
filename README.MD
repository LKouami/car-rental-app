# Car Rent APP
## Application de location de voiture  ![N|Solid](https://img.icons8.com/officel/16/000000/car-rental.png) 


## Installation

Car Rental App is build with [Django](https://www.djangoproject.com/) v4.0.3.

Install the dependencies and devDependencies and start the server.

```sh
#Create virtualenv
virtualenv env
#Active your virtualenv then install requirements
pip install -r requirements.txt
#make migration for authentication module
python manage.py makemigration authentication
#make migration for rentmodule module
python manage.py makemigration rentmodule
#then migrate
python manage.py migrate
#create super user
python manage.py createsuperuser
#run project
python manage.py runserver
```


**Python Project ESGIS MASTER1 2021-2022**

