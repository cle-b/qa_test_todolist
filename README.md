# qa_test_todolist

This project is an implementation of a test for a job interview.

The goal is to test a TODO application composed of two parts:
  * a RESTFul API which stores the tasks in a database 
  *  a Single page application web UI to make the application usage easier.

# Technical choices

The tests has been written in Python and tested on Ubuntu 19.04 (dev) and 18.04 (ci).

The following frameworks have been used:
  - pytest (for the tests management)
  - selenium (for the web automation)
  - requests (for the REST API client)

The source code is on github (https://github.com/cle-b/qa_test_todolist). Travis-ci is used for the CI.

# How to run the tests

## prerequisites

Ubuntu with Python 3.7.

A selenium webdriver installed locally or a selenium grid. 

If necessary, a shell script `run_selenium_grid.sh` is available in the repository in order to setup a selenium grid locally using docker.

```sh
sudo ./run_selenium_grid.sh
```

For these tests, only Firefox and Chrome have been used.

## setup your environment

First, do the classic things (clone repo, create a virtual env, install python requirements...)

```
git clone https://github.com/cle-b/qa_test_todolist.git
cd qa_test_todolist
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Then you have to create 3 environment variables that will be used in order to configure the test.

```
export QA_TODOAPP_BASEURL="http://example.com"
export QA_TODOAPP_USERNAME="USER1"
export QA_TODOAPP_PASSWORD="PASS1"
```

## run the tests

There are many ways to launch the tests, depending on your setup and what you want to test.

If you just want to test the REST API, use the following command:

```
pytest -s -v -m api 
```

If you want to test the WebApp, you have to specify which driver to use. For example, with a local Firefox driver:

```
pytest -s -v -m web --driver firefox
```

With a remote Chrome (at least if you run the selenium grid locally with docker):

```
pytest -s -v -m web --driver Remote --capability browserName chrome
```

For more details on webdriver selection, see https://pytest-selenium.readthedocs.io/en/latest/user_guide.html#specifying-a-browser

### advanced configuration

Tests have been marked so you can easily choose to test a specific feature. For example, if you want to test the authentication for the REST API and the WebAPP:

```
pytest -s -v -m "(web or api) and authentication" --driver Remote --capability browserName chrome
```

The list of markers is in the `pytest.ini` file.

You can generate a report with debug informations with the --html option:

```
pytest -s -v -m "(web or api) and authentication" --driver Remote --capability browserName chrome --html=report.html
```

You can also used the tox command in order to launch preconfigured tests:

```
tox -e py37-api
tox -e py37-remotefirefox
tox -e py37-remotechrome
```

When the tests are executed through tox, the report is automatically saved in the `reports` directory.

(flake8, black and py37-pr are tox environments that have been created only for the development, not in order to run the tests).
