# UDIS

UDIS is a website designed for use by universities (especially the three major _classes_ of people found in universities, i.e, **Students**, **Faculty** and **Secretaries**). It tries to simplify and intuitively direct users to specific sub-systems that they seek within the university, along with implementing an authentication and verification system. 

## Features

- User verifiication system that does not allow any non-authenticated tasks.
  - Students cannot access other students' grades/profiles, while faculties and Secretaries can access the profiles of all students.
  - Students cannot edit their grade detaiils, faculties can also not edit grade details directly while secretaries can edit student grades.
  - Students can only view the larger information about the university, faculties have limited permissions with regards to editing stuff in the database, while secretaries hold all the power in whatever data is represented.
- A completely autmoated system to keep trrack of purchases across departments, research gants or whatever credit/debit transactions take place officially
- Facilities for students to register for their own courses for their current semesters.
- Partial keyword and full keyword searches for most searching funcionalities.

## Dependencies

The UDIS website system needs Python Django, HTML, CSS and PostgreSQL. Hence, to run this project simply install python (version 3.10 is preferable), install django (version 4.1.7), install PostgreSQL (latest version) and clone the repository (Detailed installation instructions are given below)

## Installation

- If python is not installed, go to www.python.org/downloads/ and download version 3.10 for your OS (or the latest release, if you arre completely sure of no loss of functionalities). Optionally, you may download some editor along with the python interpreter such as Jupyter Notebook, PyCharm or any other.
- Install PostgreSQL from [here](https://www.postgresql.org/download/)
- Start postgresql on your machine. On windows, use the service manager to force start the application, on Linux-based systems use `sudo service postgresql start`
- Migrate to your command prompt (or the Terminal) and enter `pip install pipenv` (if you're using Jupyter notebook, you can follow the iinsstructions to set up a venv [here](https://www.geeksforgeeks.org/using-jupyter-notebook-in-virtual-environment/))
- Use `git clone` to clone the project into your local machine. Do nt download the .zip or the .tar.gz file
- In the parent repository to the project, start a pipenv shell by running  `pipenv shell` (If you are already running python in a virtual environment, you may skip this step)
- Now, migrate to the directory with the `manage.py` file and run the commands `python manage.py makemigrations`, `python manage.py migrate` and `python manage.py runserver` to run thhe application.
- The application can be found at the website `127.0.0.1:8000`, as that is the default port for django and the IP address of the localhost. If you want to specify a different HTTP port, use `python manage.py runserver <Your.IP.address:PortNumber>` 
