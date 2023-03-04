# automation

## Executing Test Scripts in a Docker Container:

### Executing Test Scripts in parallel mode using docker:

- Download the docker-compose.yaml file

- Run below command in terminal (from directory containing docker-compose.yaml):

- `docker-compose up --scale chrome={n} --scale firefox=0 --scale edge=0`

Where n should be same as N_PROCESSES in yaml file, for example 2 for this MODULE_NAME mentioned above as it has two
modules under tourpoints

We can update these fields as needed MODULE_NAME, CI_URL , BROWSER and N_PROCESSES fields, given example below for
reference.

`MODULE_NAME = TestCases/TeamManagePage/tourpoints`

`BROWSER = chrome`

`CI_URL = https://www.saucedemo.com/`

`N_PROCESSES = 2` Note: For single browser and single process, we can set n and N_PROCESSES values to 1 .

### To observe live test script execution (running in a container):

- Open url http://localhost:4444/ui#/sessions

- Click on the Video icon

- Enter password secret and click on ACCEPT button

- To observe html reports of the test scripts executed:

- Open new terminal and cd to same directory containing yaml file

- Run command allure serve test_report/

This is a QA Automation Project - designed using Python, Pytest and html-reporter OR allure_report

## For complete Automation Testing setup in the local machine

- Install [latest](https://www.python.org/downloads/macos/) Python 3.x,

- Install [Pytest](https://docs.pytest.org/en/6.2.x/getting-started.html)
    - `pip install -U pytest`

- Install [selenium](https://selenium-python.readthedocs.io/installation.html) for python
    - `pip install selenium`

- Download and Install [Pycharm editor](https://www.jetbrains.com/pycharm/download/#section=mac)

- Import the `automation` project in pycharm

### For html-reporter

- Install [html-reporter](https://pypi.org/project/pytest-html-reporter/)
    - `pip3 install pytest-html-reporter`

- Executing all tests under TestCases directory and Generate html-reporter report
    - `pytest TestCases/ --html-report=./report/report.html`

- Test execution reports will get generated in `report` folder under project root folder

### For allure html report

- Installing allure
    - `pip install allure-pytest`

- Executing tests for allure report
    - `pytest --alluredir=allure_report/ TestCases/`

- Generating Allure report
    - `allure serve allure_report/`

### Publishing Allure Report to vimeo github qa-blr-test-reports pages

- step 1: After test execution is completed run command `allure serve allure_report/` to generate report
- step 2: Copy path of `allure_report` folder from terminal.
- step 3: Run command to open report in a finder folder e.g. `open /var/folders/....../allure_report`
- step 4: Clone repository to local
  machine
- step 5: Switch to 'main' branch
- step 6: Replace all contents from `allure_report` (refer step 3) to the `qa-blr-test-reports`
- step 7: git add, commit, push changes to `main` remote branch of `qa-blr-test-reports`

Now allure report can be accessed online using following url 

### Executing only tests with specific markers (tags)

e.g. smoketest

`pytest TestCases/ -m smoketest`
