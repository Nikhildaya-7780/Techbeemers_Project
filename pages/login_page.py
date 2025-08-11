import config
from config import BASE_URL
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):

        # Locators

        user_name = (By.XPATH, "//input[@id='username']")
        email = (By.XPATH, "//input[@id='email']")
        password = (By.XPATH, "//input[@id='password']")
        bio = (By.XPATH, "//textarea[@id='bio']")
        country_dropdown = (By.XPATH, "//select[@id='country']")
        languages = (By.XPATH, "//input[@id='languages']")
        interests = (By.XPATH, '//input[@type="checkbox"]')
        gender = (By.XPATH, '//input[@name="gender"]')
        submit_button = (By.XPATH, '//button[@id="submit-btn"]')
        reset_button = (By.XPATH, '//button[@id="reset-btn"]')
        disable_button = (By.XPATH, '//button[@id="disabled-btn"]')


        def access_url(self):
                self.open_url(BASE_URL)

        def enter_username(self):
                self.enter_text(self.user_name, "Nikhil")

        def enter_username_2_char(self):
                self.enter_text(self.user_name, "Ni")

        def enter_email(self):
                self.enter_text(self.email, "testnikhil7708@yopmail.com")

        def enter_password(self):
                self.enter_text(self.password, "Nikhil@123456")

        def enter_only_four_char(self):
                self.enter_text(self.password, "Nikh")

        def enter_bio(self):
                self.enter_text(self.bio, "I am a dedicated automation tester who can automate anything")








