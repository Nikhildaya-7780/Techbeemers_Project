from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class SubmitFormPage(BasePage):

    submit_button = (By.XPATH, '//button[@id="submit-btn"]')
    reset_button = (By.XPATH, '//button[@id="reset-btn"]')
    disable_button = (By.XPATH, '//button[@id="disabled-btn"]')
    success_message = (By.XPATH, '//div[@id="form-result"]')


    def submit(self):
        self.click_element(self.submit_button)

    def success_mes_confirm(self):
        self.wait_for_success_message(self.success_message)

    def reset(self):
        self.click_element(self.reset_button)

    def disable(self):
        self.is_enabled(self.disable_button)

