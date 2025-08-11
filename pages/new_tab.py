from selenium.webdriver.common.by import By
from webdriver_manager.core import driver

from pages.base_page import BasePage


class NewTab(BasePage):



    FORM_BUTTON = (By.CSS_SELECTOR, 'button[data-target="form-elements"]')
    DYNAMIC_BUTTON = (By.CSS_SELECTOR, 'button[data-target="dynamic-elements"]')
    NEW_TAB = (By.XPATH, "//a[normalize-space()='Selenium Website (New Tab)']")
    DEFAULT_LINK = (By.XPATH, "//a[@id='prevent-default-link']")
    BROWSER_BACK = (By.XPATH, "//button[@id='browser-back']")
    BROWSER_FORWARD = (By.ID, "browser-forward")
    BROWSER_REFRESH = (By.ID, "browser-refresh")


    def jump_element(self):
        self.click_element(self.FORM_BUTTON)
        self.click_element(self.DYNAMIC_BUTTON)

    def new_window(self):
        self.click_element(self.NEW_TAB)
        self.switch_to_new_window()

    def default_window(self):
        self.click_element(self.DEFAULT_LINK)

    def browser_back(self):
        self.click_element(self.BROWSER_BACK)

    def browser_forward(self):
        self.click_element(self.BROWSER_FORWARD)

    def browser_refresh(self):
        self.click_element(self.BROWSER_REFRESH)

