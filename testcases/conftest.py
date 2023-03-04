import platform
import pytest
from selenium import webdriver
from library import config_reader
from library.common_functions import CommonFunctions


base_url = None


def pytest_addoption(parser):
    '''
    Register argparse-style options and ini-style config values, called once at the beginning of a test run.
    :param parser:
    :return:
    '''
    parser.addoption("--ip", action="store", help="input ip")
    parser.addoption("--browser", action="store", help="input browser")
    parser.addoption("--ci_url", action="store", help="input ci_url")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    '''
    Called to create a TestReport for each of the setup, call and teardown runtest phases of a test item.
    :param item:
    :param call:
    :return:
    '''
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="class", autouse=True)
def setup(request):
    '''
    Setup for the test
    :param request:
    :return:
    '''

    global driver
    global run_type
    run_type = 'docker'  # 'docker', 'local'

    if platform.system() != "Darwin":

        global base_url

        if request.config.getoption('--ci_url') is not None:
            base_url = request.config.getoption('--ci_url')
        else:
            base_url = "https://master.ci.vimeows.com/"

        if request.config.getoption('--ip') is not None:
            host = request.config.getoption('--ip')
        else:
            host = 'localhost'

        browser = request.config.getoption('--browser')
        browser = browser

        if browser is not None:
            if browser == 'firefox':
                opt = webdriver.FirefoxOptions()
            elif browser == 'edge':
                opt = webdriver.EdgeOptions()
            elif browser == 'chrome':
                opt = webdriver.ChromeOptions()
        else:
            opt = webdriver.ChromeOptions()

        opt.add_argument('--remote-debugging-port=8000')
        opt.page_load_strategy = 'none'

        ce = "http://" + host + ":4444/wd/hub"

        driver = webdriver.Remote(command_executor=ce, options=opt)
    else:

        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver import Firefox
        if config_reader.read_config_data('Details', 'Browser') == 'Chrome':
            options = webdriver.ChromeOptions()

            # To consider Google Chrome Beta version
            # options.binary_location = "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"

            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option('prefs', {
                'credentials_enable_service': False,
                'profile': {
                    'password_manager_enabled': False
                }
            })
            options.page_load_strategy = 'none'
            #service = ChromeService(executable_path="./Drivers/chromedriver")
            driver = webdriver.Chrome(options=options)
        elif config_reader.read_config_data('Details', 'Browser') == 'Firefox':
            geekodriver_path = "./Drivers/geckodriver"
            driver = Firefox(executable_path=geekodriver_path)
        else:
            raise ValueError('No Proper browser name mentioned in the ./ConfigurationFiles/Config.cfg')
        base_url = config_reader.read_config_data('Details', 'Application_URL')

    # driver.maximize_window()
    if platform.system() == "Darwin":
        driver.maximize_window()

        '''To block some network calls which usually takes time to load commented it as it won't support 
        in docker container'''
        driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": [
            "https://analytics.tiktok.com/",
            "https://cds.taboola.com/",
            "https://tr.snapchat.com/",
            "https://pixel.tapad.com/",
            "https://wa.appsflyer.com/",
            "https://wa.onelink.me/",
            "https://simonsignal.com/",
            "https://bam-cell.nr-data.net/",
        ]})
        driver.execute_cdp_cmd('Network.enable', {})
    else:
        driver.set_window_size(1920, 1080)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)
    driver.get(base_url)
    CommonFunctions(driver).wait_for_page_load(10)
    request.cls.driver = driver
    yield driver
    driver.close()
    driver.quit()
