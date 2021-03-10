# AdHoc-Query-Builder

Project for Data Modelling course Spring Semester 2021

## Setting up the project

* Create virtual environment

```
python3 -m venv env
```
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
* Setting mysql database configurations

  * Go to "config.py"
  * Change the values of "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE" according to your mysql configurations
* Running the application

```
flask run
```
## Guidelines for contribution

* If you want to contribute:

  * Fork this repo
  * Clone the forked repo
  * Follow the "Setting up the project" steps
  * Checkout a new branch
  * Make changes and commit
  * Push changes and generate a Pull Request
  * Make sure your code is properly formatted and readable
