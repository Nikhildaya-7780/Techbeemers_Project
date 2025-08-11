from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from pages.base_page import BasePage


class Show_Hide_Elements(BasePage):

    TOGGLE = (By.ID, "toggle-visibility")
    TOGGLE_ELEMENT = (By.ID, "toggle-element")



    def show_element(self):
        self.click_element(self.TOGGLE)
        self.is_element_displayed(self.TOGGLE_ELEMENT)
        if visibility_of_element_located(self.TOGGLE_ELEMENT):
            print("Toggle button enabled")
#        assert "This element can be toggled visible/hidden" in self.is_element_displayed(self.TOGGLE_ELEMENT)

    def hide_element(self):
        self.click_element(self.TOGGLE)
        print ("Toggle disabled")

