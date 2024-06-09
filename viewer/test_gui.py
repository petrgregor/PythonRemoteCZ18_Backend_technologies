import time

from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

class GuiTestWithSelenium(TestCase):
    # Important: it uses real database
    # Important: server must be running

    def test_home_page_firefox(self):
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Welcome to HollyMovie' in selenium_webdriver.page_source

    def test_home_page_chrome(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Welcome to HollyMovie' in selenium_webdriver.page_source

    def test_home_page_edge(self):
        selenium_webdriver = webdriver.Edge()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Welcome to HollyMovie' in selenium_webdriver.page_source

    def test_signup(self):
        selenium_webdriver = webdriver.Firefox()
        selenium_webdriver.get('http://127.0.0.1:8000/accounts/signup/')
        """login_dropdown_menu = selenium_webdriver.find_element(By.ID, 'login-dropdown-menu')
        login_dropdown_menu.send_keys(Keys.RETURN)
        signup_button = selenium_webdriver.find_element(By.ID, 'signup')
        signup_button.send_keys(Keys.RETURN)"""
        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        time.sleep(2)
        username_field.send_keys('TestUser1')
        time.sleep(2)
        password1_field = selenium_webdriver.find_element(By.ID, 'id_password1')
        password1_field.send_keys('MojeSuperTajneHeslo123&')
        time.sleep(2)
        password2_field = selenium_webdriver.find_element(By.ID, 'id_password2')
        password2_field.send_keys('MojeSuperTajneHeslo123&')
        time.sleep(2)
        birth_date_field = selenium_webdriver.find_element(By.ID, 'id_birth_date')
        birth_date_field.send_keys('2020-01-01')
        time.sleep(2)
        biography_field = selenium_webdriver.find_element(By.ID, 'id_biography')
        biography_field.send_keys('Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. '
                                  'Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. '
                                  'Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. Nějaký dlouhý text. ')
        time.sleep(2)
        submit_button = selenium_webdriver.find_element(By.ID, 'id-submit')
        submit_button.send_keys(Keys.RETURN)

        assert 'A user with that username already exists.' in selenium_webdriver.page_source

# TODO: test login
# TODO: test add new movie
# TODO: test add new genre
# TODO: test add new creator
