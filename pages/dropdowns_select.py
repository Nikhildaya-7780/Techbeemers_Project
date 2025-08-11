from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class DropdownsPage(BasePage):

    country_dropdown = (By.XPATH, "//select[@id='country']")
    languages = (By.XPATH, "//select[@id='languages']")


    def select_country_dropdown(self, country_name):
        self.select_by_text(self.country_dropdown, "United States")

    def select_languages(self, languages):
        self.select_by_text(self.languages, "English")