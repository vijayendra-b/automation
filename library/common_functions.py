import time

import allure
import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


mylogger = logging.getLogger()


class CommonFunctions:

    def __init__(self, obj):
        global driver
        driver = obj

    @allure.step("Navigate to url {prefix}")
    def navigate_to_url(self, prefix):
        """
        Navigates to the sub-url prefix
        :param prefix:
        :return:
        """
        from testcases import conftest
        url = conftest.base_url + prefix
        self.wait_for_page_load()
        driver.get(url)
        time.sleep(1)
        self.wait_for_page_load(10)
        print("navigated to :" + prefix)

    @allure.step("is element present")
    def is_element_present(self, *locator):
        """
        :param locator:
        :return: boolean
        """
        try:
            driver.find_element(*locator)
            return True
        except NoSuchElementException as e:
            mylogger.info(e, exc_info=True)
            return False

    @allure.step("Wait for a specified element to be clickable")
    def wait_for_element_to_be_clickable(self, locator, wait_time=5):
        """
        An expectation for checking that an element, known to be present on the DOM of a page, is visible.
        Visibility means that the element is not only displayed but also has a height and width that is greater than 0.
        element is the WebElement returns the (same) WebElement once it is visible
        Wait for the element to be clickable
        :param locator:
        :param wait_time:
        :return:
        """
        try:
            WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            pass

    @allure.step("Wait for no staleness of specified element")
    def wait_for_no_staleness(self, element, time_in_sec=10):
        """
        :param element:
        :return:
        """
        WebDriverWait(driver, time_in_sec).until_not(EC.staleness_of(element))

    @allure.step("Wait for staleness of specified element")
    def wait_for_staleness(self, element, time_in_sec=10):
        """
        :param element:
        :return:
        """
        WebDriverWait(driver, time_in_sec).until(EC.staleness_of(element))

    @allure.step("Wait for presence of specified element")
    def wait_for_presence_of_element_located(self, locator, time_in_sec = 10):
        """
        An expectation for checking that an element is present on the DOM of a page.
        This does not necessarily mean that the element is visible.
        :param locator: - used to find the element
        :param time_in_sec:
        :return: the WebElement once it is located
        """
        try:
            return WebDriverWait(driver, time_in_sec).until \
                (EC.presence_of_element_located(locator))
        except TimeoutException:
            pass

    @allure.step("wait for element not present")
    def wait_for_element_not_present(self, element, time_in_sec=5):
        """
        An expectation for checking that an element is present on the DOM of a page.
        This does not necessarily mean that the element is visible.
        :param locator: - used to find the element
        :param time_in_sec:
        :return: the WebElement once it is located
        """
        return WebDriverWait(driver, time_in_sec).until_not \
            (EC.staleness_of(element))

    @allure.step("Wait for visibility of specified elements ")
    def wait_for_visibility_of_any_elements_located(self, locator):
        """
        :param locator:
        :return:
        """
        return WebDriverWait(driver, 10).until \
            (EC.visibility_of_any_elements_located(locator))

    @allure.step("Wait for specified element to be invisible")
    def wait_for_element_invisible(self, element, time_in_sec=10):
        """
        An expectation for checking that there is at least one element visible on a web page.
        locator is used to find the element.
        :param element: list of WebElements once they are located
        :param time_in_sec:
        :return:
        """
        try:
            return WebDriverWait(driver, time_in_sec).until \
                (EC.invisibility_of_element(element))
        except TimeoutException:
            pass

    @allure.step("Wait for specified text to be present in element")
    def wait_for_text_to_be_present_in_element(self, locator, search_string):
        """
        An expectation for checking if the given text is present in the specified element. locator, text
        :param locator:
        :param search_string:
        :return:
        """
        WebDriverWait(driver, 10).until \
            (EC.text_to_be_present_in_element(locator, search_string))

    @allure.step("wait for specified text to be present in element value attribute")
    def wait_for_text_to_be_present_in_element_value_attribute(self, locator, search_string):
        """
        An expectation for checking if the given text is present in the value attribute of specified textfield. locator,
         text
        :param locator:
        :param search_string:
        :return:
        """
        WebDriverWait(driver, 10).until \
            (EC.text_to_be_present_in_element_value(locator, search_string))

    @allure.step("Wait for url contains {sub_url}")
    def wait_for_url_contains(self, sub_url):
        """ An expectation for checking that the current url contains a
        case-sensitive substring.
        url is the fragment of url expected,
        returns True when the url matches, False otherwise
        """
        return WebDriverWait(driver, 10).until(EC.url_contains(sub_url))

    @allure.step("Move to specified element")
    def move_to_element(self, *locator):
        """
        Moving the mouse to the middle of an element.  - to_element: The WebElement to move to.
        :param locator:
        :return:
        """
        return ActionChains(driver).move_to_element(driver.find_element(*locator)).perform()

    @allure.step("Move to specified element and click")
    def move_to_element_and_click(self, *locator):
        """
        Moving the mouse to the middle of an element. and click on it.
        :param locator of the_element: The WebElement to move to.
        :return:
        """
        return ActionChains(driver).move_to_element(driver.find_element(*locator)).click().perform()

    @allure.step("Move to element_1 and click on element_2")
    def move_to_element_1_and_click_on_element_2(self, element1, element2):
        """
        Moving the mouse to the middle of an element. and click on it.
        :param locator of the_element: The WebElement to move to.
        :return:
        """
        return ActionChains(driver).move_to_element(element1).click(element2).perform()

    @allure.step("Check if given string has numbers")
    def has_numbers(self, inputString):
        """
        :param inputString:
        :return: boolean
        """
        return any(char.isdigit() for char in inputString)

    @allure.step("Get text from specified element")
    def get_text_from_element(self, *locator):
        """
        The text of the element.
        :param locator:
        :return:
        """
        try:
            return driver.find_element(*locator).text
        except Exception as e:
            mylogger.info(e, exc_info=True)
            return 'error'

    @allure.step("Refresh page and wait for page load")
    def refresh_and_wait_for_page_load(self):
        """
        refreshes the page and waits for page load
        :return:
        """
        driver.refresh()
        time.sleep(1)
        self.wait_for_page_load()

    # not working needs a fix
    def get_attribute_value(self, *locator, name_of_attribute):
        """
        :param locator:
        :param name_of_attribute:
        :return: value of the attribute
        """
        return driver.find_element(*locator).get_attribute(name_of_attribute)

    @allure.step("Click on specified element")
    def click_on_element(self, *locator):
        driver.find_element(*locator).click()

    @allure.step("Click on element using execute script")
    def click_using_execute_script(self, *locator):
        driver.execute_script("arguments[0].click({});", driver.find_element(*locator))

    @allure.step("Type into input field")
    def type_into_input_field(self, *locator, text):
        driver.find_element(*locator).send_keys(text)

    @allure.step("Switch to first browser tab")
    def switch_to_first_browser_tab(self):
        driver.switch_to.window(driver.window_handles[0])

    @allure.step("Switch to second browser tab")
    def switch_to_second_browser_tab(self):
        driver.switch_to.window(driver.window_handles[1])

    @allure.step("Get css property value of element")
    def get_css_property_value_of_element(*locator, property_name):
        element = driver.find_element(*locator)
        return element.value_of_css_property(property_name)

    @allure.step("Wait for page load")
    def wait_for_page_load(self, wait_seconds=5):
        try:
            count = 0
            while not (driver.execute_script('return document.readyState;').strip() == 'complete'):
                time.sleep(1)
                count = count + 1
                if count > wait_seconds:
                    break
        except TimeoutException:
            mylogger.info("document.readyState: "+driver.execute_script('return document.readyState;').strip())
            pass

    # not working needs a fix
    def type_into_element_with_delay(*locator, text):
        element = driver.find_element(*locator)
        element.click()
        element.clear()
        for c in text:
            element.send_keys(c)
            time.sleep(.2)
        time.sleep(.5)
