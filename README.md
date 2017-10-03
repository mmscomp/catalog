# Catalog Full Stack Program 
Source code for running Catalog Program

# Installation
Install python 2.7.12, Virtual Machine (VM) box, and Vagrant
Download VM configuration from https:/github.com/udacity/fullstack-nanodegree-vm. 

# Run the VM
Change to downloaded directory. This contains VM files.
To make vagrant online, run 'vagrant up'.
With vagrant ssh, do update and upgrade.
This will install required files including psycopg2 for database connection
Change to shared vagrant directory.

# Files
At the top level, there are two main files - app1DB.py and app1.py; the former is
the database setup file and the latter is the main python file.
In the directory named 'templates', there are many html files.
The css code is included in the 'main' html file.
For third party authentication, you need to include client secret files.

# Run the program
Run 'python app1.py' (w/o the quotes)  to bring the server up.
Open a browser and type 'localhost:5000/' or 'localhost:5000/catalog'.
This will load the main catalog page.
You will be able to view the contents of different categories by clicking the 
appropriate buttons.
You will need to register if you like to manipulate your own catagory items.

Acknowledgements:
Udacity Full Stack Course
Udacity Authorization and authentication course
