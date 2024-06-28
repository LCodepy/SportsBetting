import time

from selenium.common import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement


def click_element(driver, element: WebElement) -> bool:
    try:
        driver.execute_script("arguments[0].click();", element)
        return True
    except:
        return False


def scroll_into_view_and_click(driver, element: WebElement) -> bool:
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    for _ in range(20):
        time.sleep(0.1)
        try:
            element.click()
            return True
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            pass
    else:
        return False

