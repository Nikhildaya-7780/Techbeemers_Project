import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.dropdowns_select import DropdownsPage
from pages.checkbox_radiobutton import CheckboxRadioButtonPage
from pages.new_tab import NewTab
from pages.submit_form import SubmitFormPage
from pages.base_page import BasePage
import time
from pages.alerts_and_popups import AlertsAndPopups
from pages.load_content import LoadContentPage
from pages.show_hide_elements import Show_Hide_Elements


@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver
    driver.quit()




def test_login(driver):
    login_process = LoginPage(driver)
    login_process.access_url()
    login_process.enter_username()
    login_process.enter_email()
    login_process.enter_password()
    login_process.enter_bio()
    login_process = DropdownsPage(driver)
    login_process.select_country_dropdown("United States")
    login_process.select_languages("English")
    login_process = CheckboxRadioButtonPage(driver)
    login_process.interests_checkbox()
    login_process.gender_checkbox()
    login_process = SubmitFormPage(driver)
    login_process.submit()
    login_process.success_mes_confirm()
    login_process.reset()
    login_process.disable()
    alert = AlertsAndPopups(driver)
    alert.show_alerts()
    alert.confirm_ok()
    alert.prompt()
    alert.open_modal()
    load = LoadContentPage(driver)
    load.load_content()
    load.load_slow()
    show_hide = Show_Hide_Elements(driver)
    show_hide.show_element()
    show_hide.hide_element()
    time.sleep(5)


def test_new_window(driver):
    login_process = LoginPage(driver)
    login_process.access_url()
    new_tab = NewTab(driver)
    new_tab.jump_element()
    time.sleep(5)
    new_tab.new_window()
    time.sleep(5)

def test_browser_navigations(driver):
    login_process = LoginPage(driver)
    login_process.access_url()
    browser_nav = NewTab(driver)
    time.sleep(5)
    browser_nav.default_window()
    time.sleep(5)
    browser_nav.browser_back()
    time.sleep(5)
    browser_nav.browser_forward()
    time.sleep(5)
    browser_nav.browser_refresh()
    time.sleep(5)



