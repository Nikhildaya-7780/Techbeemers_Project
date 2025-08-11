from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AlertsAndPopups(BasePage):
    ALERT = (By.ID, 'js-alert')
    CONFIRM_BTN = (By.ID, 'js-confirm')
    CONFIRM_OK = (By.ID, 'confirm-ok')
    SHOW_PROMPT = (By.ID, 'js-prompt')
    PROMPT_INPUT = (By.ID, 'prompt-input')
    PROMPT_SUBMIT = (By.ID, 'prompt-submit')
    OPEN_MODAL = (By.ID, 'open-modal')
    ALERT_RESULT = (By.ID, 'alert-result')
    MODAL_CONTENT = (By.CLASS_NAME, 'modal-content')
    MODAL_CLOSE = (By.ID, "modal-close-btn")


    def show_alerts(self):
        self.click_element(self.ALERT)
        print(self.get_element_text(self.ALERT_RESULT))

    def confirm_ok(self):
        self.click_element(self.CONFIRM_BTN)
        self.click_element(self.CONFIRM_OK)
        print(self.get_element_text(self.ALERT_RESULT))

    def prompt(self):
        self.click_element(self.SHOW_PROMPT)
        self.enter_text(self.PROMPT_INPUT, "Nikhil", 10)
        self.click_element(self.PROMPT_SUBMIT)

    def open_modal(self):
        self.click_element(self.OPEN_MODAL)
        print(self.get_element_text(self.MODAL_CONTENT))
        self.click_element(self.MODAL_CLOSE)


