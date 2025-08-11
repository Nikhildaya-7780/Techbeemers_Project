from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class CheckboxRadioButtonPage(BasePage):

    interests = (By.XPATH, '//input[@type="checkbox"]')
    gender = (By.XPATH, '//input[@name="gender"]')

    def interests_checkbox(self):
        self.select_checkboxes_by_indexes(self.interests, [1, 2])

    def gender_checkbox(self):
        self.select_checkboxes_by_indexes(self.gender, [1])




