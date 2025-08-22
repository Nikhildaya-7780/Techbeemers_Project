from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class TabsAndAccordions(BasePage):

    tab1 = (By.XPATH, "//button[@data-tab='tab1']")
    tab2 = (By.XPATH, "//button[@data-tab='tab2']")
    tab3 = (By.XPATH, "//button[@data-tab='tab3']")
    tab1_text = (By.ID, "tab1")
    tab2_text = (By.ID, "tab2")
    tab3_text = (By.ID, "tab3")
    tab3_input = (By.ID, "tab3-input")


    def select_tab(self):
        self.click_element(self.tab1)
        self.get_element_text(self.tab1_text)
        self.click_element(self.tab2)
        self.get_element_text(self.tab2_text)
        self.click_element(self.tab3)
        self.get_element_text(self.tab3_text)
        self.enter_text(self.tab3_input, "Nikhil", 10 )
