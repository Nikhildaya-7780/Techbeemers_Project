import time

from selenium.common import TimeoutException, ElementNotInteractableException, ElementClickInterceptedException, \
    NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from typing import Tuple
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def resilient_click(driver, locator):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
    element.click()




class BasePage(object):
    def __init__(self, driver, timeout=10):
        self.switch_to = None
        self.window_handles = None
        self.current_window_handle = None
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)


    def open_url(self, url):
        self.driver.get(url)

    def click_element(self, locator: Tuple[str, str], timeout: int = 10, verify_locator: Tuple[str, str] = None, verify_timeout: int = 5):
        print(f"[INFO] Clicking element: {locator}")

        try:
            # Validate locator strategy
            if locator[0] not in [By.ID, By.XPATH, By.CLASS_NAME, By.CSS_SELECTOR, By.NAME, By.TAG_NAME, By.LINK_TEXT, By.PARTIAL_LINK_TEXT]:
                raise ValueError(f"[ERROR] Invalid locator strategy: {locator[0]}")

            # Wait for element to be present and clickable
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

            element = self.driver.find_element(*locator)

            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            # Hide overlapping iframes (ads)
            self.driver.execute_script("""
                document.querySelectorAll('iframe[src*="ads"], iframe[id*="ad"]').forEach(frame => {
                    frame.style.display = 'none';
                });
            """)

            # Try native click
            try:
                element.click()
                print("[INFO] Native click succeeded")
            except ElementClickInterceptedException:
                print("[WARN] Native click intercepted. Trying ActionChains...")
                try:
                    ActionChains(self.driver).move_to_element(element).click().perform()
                    print("[INFO] ActionChains click succeeded")
                except Exception as e:
                    print(f"[ERROR] ActionChains failed: {e}. Trying JS click...")
                    self.driver.execute_script("arguments[0].click();", element)
                    print("[INFO] JavaScript click succeeded")

            # Optional post-click verification
            if verify_locator:
                try:
                    WebDriverWait(self.driver, verify_timeout).until(
                        EC.presence_of_element_located(verify_locator)
                    )
                    print(f"[INFO] Verified click success via: {verify_locator}")
                except TimeoutException:
                    self._capture_screenshot("click_verification_failed")
                    raise Exception(f"[ERROR] Click on {locator} did not lead to expected element {verify_locator}")

        except TimeoutException:
            self._capture_screenshot("click_timeout")
            raise Exception(f"[ERROR] Timeout: Element {locator} not clickable after {timeout} seconds.")
        except Exception as e:
            self._capture_screenshot("click_exception")
            raise Exception(f"[ERROR] Unexpected error during click: {e}")



    def find_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            print(f"Timed out trying to find_element: {locator}")

    def get_element_text(self, locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.text
        except TimeoutException:
            print(f"Timed out trying to get text: {locator}")
            return None

    def enter_text(self, locator, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
        except TimeoutException as te:
            self.log_error(f"Timeout while locating element {locator}: {te}")
            raise
        except ElementNotInteractableException as ene:
            self.log_error(f"Element not interactable {locator}: {ene}")
            raise

    def log_error(self, param):
        pass

    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def assert_text_equals(self, locator, expected_text, timeout=10):
        actual_text = self.get_element_text(locator)
        assert actual_text == expected_text, (
            f"Expected: '{expected_text}', but got: '{actual_text}'"
        )

    def is_element_enabled(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_enabled()
        except TimeoutException:
            return False

    def mouse_over(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
        except TimeoutException as e:
            self.log_error(f"Mouse over failed for {locator}: {e}")
            raise

    def drag_and_drop(self, source_locator, target_locator, timeout=10):
        try:
            source = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(source_locator)
            )
            target = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(target_locator)
            )
            action = ActionChains(self.driver)
            action.drag_and_drop(source, target).perform()
        except TimeoutException as e:
            self.log_error(f"Drag and drop failed: {e}")
            raise

    def wait_for_element_to_disappear(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException as e:
            self.log_error(f"Element did not disappear: {locator} — {e}")
            raise

    def refresh_page(self):
        try:
            self.driver.refresh()
        except Exception as e:
            self.log_error(f"Page refresh failed: {e}")
            raise

    def wait_for_text_in_element(self, locator, expected_text, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, expected_text)
            )
        except TimeoutException as e:
            self.log_error(f"Text not found: '{expected_text}' in {locator} — {e}")
            raise

    def get_element_attribute(self, locator, attribute, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.get_attribute(attribute)
        except TimeoutException as e:
            self.log_error(f"Failed to get attribute '{attribute}' from {locator} — {e}")
            raise

    def scroll_to_element(self, locator):
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except Exception as e:
            self.log_error(f"Scroll failed for {locator}: {e}")
            raise

    def get_elements_count(self, locator):
        try:
            elements = self.driver.find_elements(*locator)
            return len(elements)
        except Exception as e:
            self.log_error(f"Counting elements failed for {locator}: {e}")
            raise

    def handle_alert(self, action="accept"):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        if action == "Allow":
            alert.accept()
        elif action == "Block":
            alert.dismiss()

    from selenium.webdriver.support.ui import Select

    def select_by_text(self, locator, text):
        select = Select(self.driver.find_element(*locator))
        select.select_by_visible_text(text)

    def select_checkboxes_by_indexes(self, locator, indexes, timeout=10):

        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        checkboxes = self.driver.find_elements(*locator)

        for i in indexes:
            if i < len(checkboxes):
                checkbox = checkboxes[i]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                if not checkbox.is_selected():
                    try:
                        checkbox.click()
                    except ElementClickInterceptedException:
                        self.driver.execute_script("arguments[0].click();", checkbox)
            else:
                print(f" Index {i} is out of range. Available checkboxes: {len(checkboxes)}")

    def is_enabled(self, locator, timeout=10):

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_enabled()
        except TimeoutException:
            print(f"⚠️ Element with locator {locator} not found within {timeout} seconds.")
            return False

    def wait_for_success_message(self, locator, timeout=5):

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            print("✅ Success message appeared!")
            return True
        except:
            print("❌ Success message did NOT appear.")
            return False

    def verify_and_accept_alert(self, expected_text=None, timeout=10):
        """
        Waits for a JavaScript alert, validates its text, and accepts it.

        :param expected_text: Optional string to validate against alert text
        :param timeout: Max time to wait for alert
        """
        try:
            # Wait for alert to be present
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert

            # Get alert text
            actual_text = alert.text
            print(f"Alert appeared with text: '{actual_text}'")

            # Validate alert text if expected_text is provided
            if expected_text:
                assert actual_text == expected_text, f"Expected '{expected_text}', but got '{actual_text}'"

            # Accept the alert
            alert.accept()
            print("Alert accepted successfully.")

        except TimeoutException:
            print("Alert did not appear within timeout.")
            self.driver.save_screenshot("alert_timeout.png")
            raise
        except AssertionError as ae:
            print(f"Alert text mismatch: {ae}")
            self.driver.save_screenshot("alert_text_mismatch.png")
            raise
        except Exception as e:
            print(f"Unexpected error while handling alert: {e}")
            self.driver.save_screenshot("alert_handling_error.png")
            raise

    def verify_modal_popup(self, popup_locator, expected_text=None, timeout=10):
        """
        Verifies a custom modal popup and its text.
        """
        try:
            popup = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(popup_locator)
            )
            actual_text = popup.text
            print(f"Popup text: {actual_text}")

            if expected_text:
                assert expected_text in actual_text, f"Expected '{expected_text}' in popup, but got '{actual_text}'"

        except Exception as e:
            print(f"Modal popup validation failed: {e}")
            self.driver.save_screenshot("modal_popup_failed.png")
            raise

    def is_element_displayed(self, locator, timeout=5):
        """
        Checks if an element is visible on the page.

        :param locator: Tuple (By.ID, "element_id") or any By strategy
        :param timeout: Max time to wait for visibility
        :return: True if displayed, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False
        except Exception as e:
            print(f"Error checking visibility: {e}")
            return False

    def switch_to_new_window(self):
        original = self.driver.current_window_handle

        print("Waiting for new window/tab to open...")
        try:
            WebDriverWait(self.driver, 20).until(EC.number_of_windows_to_be(2))
        except TimeoutException:
            print(f"Timeout waiting for new window. Current handles: {self.driver.window_handles}")
            self._capture_screenshot("switch_to_new_window_timeout")
            raise Exception("Timed out waiting for new window/tab to open.")

        handles = self.driver.window_handles
        print(f"Window handles after wait: {handles}")

        for handle in handles:
            if handle != original:
                self.driver.switch_to.window(handle)
                print(f"Switched to new window: {handle}")
                return original  # Return the original handle for later switch-back

        self._capture_screenshot("no_new_window_found")
        raise Exception("No new window handle found. Only one window is open.")

    def _capture_screenshot(self, param):
        import os
        import datetime

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{param}_{timestamp}.png"
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
