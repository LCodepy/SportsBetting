import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


driver = webdriver.Chrome()
driver.get("https://www.sofascore.com/betting-tips-today")

itr = 0
drops = {}
n_updates = 0
while itr < 100:
    start_time = time.time()

    new_drops = {}

    elements = driver.find_elements(By.CLASS_NAME, 'Box.gxNTXI')

    for element in elements:
        try:
            title = element.find_elements(By.CLASS_NAME, "Box.iCwxSI")[0].get_attribute("title")
            drop = element.find_elements(By.CLASS_NAME, "Text.kJWPsG")[0].get_attribute("innerHTML")
            new_drops[title] = drop
        except:
            pass

    if drops != new_drops:
        print("Drops updated!")
        n_updates += 1
        drops = new_drops.copy()

    driver.refresh()

    itr += 1
    time.sleep(30)

print("UPDATES:", n_updates)

driver.quit()
