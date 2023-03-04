import json
import logging
import time

import allure
import requests
from testcases.base_class import BaseClass
from pages.vimeo.logged_out_home_page import LOHP
from pages.vimeo.video_manage_page import VideoManagerPage

mylogger = logging.getLogger()

class TestBaseClass(BaseClass):

    @allure.step("Login to swag labs")
    def login_to_vimeo(self, username, password):
        """
        login and navigate to video manager page, and switch to user specified in switchTo param.
        Pre-condition: the account should have atleast one folder to have the team switch dropdown to visible.
        and it should have a proper teammember as per test case.
        :param username: str
        :param password: str
        :return:
        """
        lohp = LOHP(self.driver)
        login_modal = lohp.click_on_login()
        login_modal.enter_email_id(username)
        login_modal.enter_password(password)
        lihp = login_modal.click_on_login_button()

    @allure.step("Login to vimeo")
    def login_to_vimeo(self, username, password):
        """
        login and navigate to video manager page, and switch to user specified in switchTo param.
        Pre-condition: the account should have atleast one folder to have the team switch dropdown to visible.
        and it should have a proper teammember as per test case.
        :param username: str
        :param password: str
        :return:
        """
        lohp = LOHP(self.driver)
        login_modal = lohp.click_on_login()
        login_modal.enter_email_id(username)
        login_modal.enter_password(password)
        lihp = login_modal.click_on_login_button()

    @allure.step("Login and navigate to video manager page")
    def login_and_navigate_to_video_manager_page(self, username, password, switchTo="currentUser"):
        """
        login and navigate to video manager page, and switch to user specified in switchTo param.
        Pre-condition: the account should have atleast one folder to have the team switch dropdown to visible.
        and it should have a proper teammember as per test case.
        :param username: str
        :param password: str
        :param switchTo: str 'currentUser' OR 'teamMember'
        :return:
        """
        lohp = LOHP(self.driver)
        lohp.wait_for_page_load()
        login_modal = lohp.click_on_login()
        login_modal.enter_email_id(username)
        login_modal.enter_password(password)
        lihp = login_modal.click_on_login_button()
        lihp.navigate_to_url("manage/videos")
        video_manager_page = VideoManagerPage(self.driver)
        time.sleep(1)
        video_manager_page.wait_for_presence_of_element_located(video_manager_page.TEAM_SWITCH_DROPDOWN)
        self.driver.execute_script("window.stop();")
        try:
            if switchTo == 'currentUser':
                video_manager_page.select_current_user_in_the_team_switch_dropdown()
            elif switchTo == 'teamMember':
                video_manager_page.select_first_team_member_in_the_team_switch_dropdown()
        except Exception as e:
            print(e)
        # pass
        return video_manager_page

    @allure.step("Find values")
    def find_values(self, key, json_repr):
        results = []

        def _decode_dict(a_dict):
            try:
                results.append(a_dict[key])
            except KeyError:
                pass
            return a_dict

        json.loads(json_repr, object_hook=_decode_dict)  # Return value ignored.
        return results[0]

    @allure.step("Get invite url from /users/{user_id}/")
    def get_invite_url(self, user_id, access_token):
        my_headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get(
            'https://master-api.ci.vimeows.com/users/' + str(user_id) + '/teammembers'
            , headers=my_headers)
        # Convert data to dict
        data = json.loads(response.text)
        # Convert dict to string
        data = json.dumps(data)
        print("/n" + data + "/n")
        mylogger.info('response for' + 'https://master-api.ci.vimeows.com/users/' + str(user_id) + '/teammembers :: '
                      + str(data))
        invite_url = self.find_values('invite_url', data)
        return invite_url