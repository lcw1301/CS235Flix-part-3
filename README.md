# CS235Flix Web App

## Description

A web app that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

Navigate to the location/folder that you chose before, which now contains the *CS235Flix part 2* directory (i.e. the directory that has the movie_app\ and tests\ directories plus other files), and access the *CS235Flix part 2* directory.
Instructions as shown below:
```shell
C:\Users\Home> cd Documents\GitHub\CS235Flix-part-2
```

Next set of instructions:
```shell
C:\Users\Home> cd Documents\GitHub\CS235Flix-part-2 py -3 -m venv venv
C:\Users\Home> cd Documents\GitHub\CS235Flix-part-2 venv\Scripts\activate
C:\Users\Home> cd Documents\GitHub\CS235Flix-part-2 pip install -r requirements.txt
```

## Execution

**Running the application**

From the *CS235Flix* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
C:\Users\Home> cd Documents\GitHub\CS235Flix-part-2 flask run
```` 

## Configuration

The *CS235Flix/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

## Testing

Testing requires that file *CS235Flix/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *CS235Flix/tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'Home', 'Documents', 'GitHub', 'CS235Flix-part-2', 'tests', 'data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\Home> cd Documents\GitHub\CS235Flix-part-2\tests\data`

You can then run tests from within PyCharm.

**Running the tests via the Command Prompt window**

From the *CS235Flix* directory, and within the activated virtual environment (see *venv\Scripts\activate* in the **Installation** guide):
```shell
C:\Users\Home> cd Documents\GitHub\CS235Flix-part-2 python -m pytest
```