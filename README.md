# AdHoc-Query-Builder

Project for Data Modelling course Spring Semester 2021

## Setting up the project

* Create virtual environment

python3 -m venv env
* Activate virtual env

```
source env/bin/activate
```
* Update pip

```
pip install --upgrade pip
```
* Installing dependencies

```
pip3 install -r requirements.txt
```
* Setting flask environment variables

```
export FLASK_APP=run.py
export FLASK_ENV=development (Do this step everytime when you start venv)
```
* Setting mysql database sonfigurations

  * Go to "config.py"
  * Change the values of "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE" according to your mysql configurations
* Running the application

```
flask run
```
