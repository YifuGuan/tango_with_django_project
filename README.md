# Rango

Reference: Tango With Django, written by Leif Azzoparidi and David Maxwell

# Lab1:
Initiate project and create repository with Git.

# Lab2:
Go through the first 4 chapters of textbook

In Chapter 2, we learn how to test our code, by using code in prompt: python manage.py test rango.*** (name of test file)

In Chapter 3, we learn how to initiate a rango app, and add a basic request dealing method in view.py, then connect the app with project by adding URL to urlsparttern list in project's urls.py

<<<<<<< HEAD
# Lab3:
In Chapter5, we learn how to deal with Model and Template.
When creating models, 
--firstly, design ER diagram, making sure entities and relationship of model.
Secondly, create entities class in models.py in app folder. (dont forget to modify __str__() method).
--Thirdly, type $ python manage.py migrate to initialised database.
--Fourthly, type $ python manage.py createsuperuser to create a superuser account for future modification
--Fifthly, type $ python manage.py makemigrations rango to update rango's model
--To check the setting, typing $ python manage.py sqlmigrate rango 0001 to show the SQL statements of entities. Then typing $ python manage.py migrate to update the database.
--To better interact with Django model, we use Django shell ($ python manage.py shell). --For futher GUI, we should login as an admin to our application and coding in admin.py of rango folder.
--For antomatically populating entites into database, we should code a script file.
In this file, get_or_create method can be used to create an instance and invoke save method to save data to database.
=======
In Chapter 4, we learn how to import media source to our app, 1). static resource, 2). media resource 
>>>>>>> 9c78de59619b05e4dc1e5e02112fd7de833af906
