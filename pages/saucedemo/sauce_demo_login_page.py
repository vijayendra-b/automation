import time

from selenium.webdriver.common.by import By

from library.common_functions import CommonFunctions


class LoginPage(CommonFunctions):

    def __init__(self, obj):
        global driver
        driver = obj

    USERNAME = (By.CSS_SELECTOR, ".login-box #user-name")
    PASSWORD = (By.CSS_SELECTOR, ".login-box #password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-box input#login-button")
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def login_to_swag_labs(self, username, password):
        # import pdb
        # pdb.set_trace()
        self.wait_for_presence_of_element_located(self.USERNAME)
        driver.find_element(*self.USERNAME).send_keys(username)
        self.wait_for_visibility_of_any_elements_located(self.PASSWORD)
        driver.find_element(*self.PASSWORD).send_keys(password)
        driver.find_element(*self.LOGIN_BUTTON).click()

    def logout(self):
        self.wait_for_visibility_of_any_elements_located(self.MENU)
        driver.find_element(*self.MENU).click()
        driver.find_element(*self.LOGOUT_LINK).click()

    def get_error_message(self):
        return self.get_text_from_element(*self.ERROR_MESSAGE)
