from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoadContentPage(BasePage):

    LOAD_BUTTON = (By.XPATH, '//button[@id="load-content"]')
    LOAD_SLOW_CONTENT = (By.ID, "dynamic-content")
    SLOW_LOAD = (By.ID, "slow-load")




    def load_content(self):
        self.click_element(self.LOAD_BUTTON)
        self.get_element_text(self.LOAD_SLOW_CONTENT)
        assert "This content was loaded after a brief delay. Practice waiting for elements to appear in your tests." in self.get_element_text(self.LOAD_SLOW_CONTENT)


    def load_slow(self):
        self.click_element(self.SLOW_LOAD)
        self.get_element_text(self.LOAD_SLOW_CONTENT)
        assert "This content took 5 seconds to load." in self.get_element_text(self.LOAD_SLOW_CONTENT)