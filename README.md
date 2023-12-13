# CPSC 471 Project - Musicrant

Created and tested with Python 3.11.6.
Note that one of the required packages (mysqlclient) does not work with Python 3.12.

Compile and run instructions (for Windows):
1. Install MySQL. MySQL Server is not needed because the project database is currently hosted on AWS. 
2. Create a Python virtual environment with `py -m venv venv`.
3. Activate the virtual environment with `venv\Scripts\activate.bat`.
4. Change directory to 471Project\MyProject. Install the required packages in the virtual environment with `py -m pip install -r requirements.txt`.
5. Now run `py manage.py runserver`, and the website should be up and running at http://127.0.0.1:8000/.
