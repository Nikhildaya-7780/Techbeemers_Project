#import pytest
#from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# @pytest.fixture(scope="session")
#def driver():
 #   chrome_options = Options()
 #   chrome_options.add_argument("--start-maximized")
 #   chrome_options.add_argument("--disable-extensions")

  #  service = Service(ChromeDriverManager().install())
   # driver = webdriver.Chrome(service=service, options=chrome_options)

  #  yield driver
  #  driver.quit()


