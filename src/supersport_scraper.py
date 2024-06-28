import json
import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import click_element, scroll_into_view_and_click


DATA_FILE_PATH = "\\".join(__file__.split("\\")[:-2]) + "\\data\\supersport\\"


def main():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    day = "27"

    url = f"https://www.supersport.hr/sport/dan/{day}"
    driver.get(url)

    time.sleep(4)

    sport_offers = driver.find_elements(By.XPATH, '//div[contains(@class, "sport")]')
    for offer_idx in range(len(sport_offers)):
        element = sport_offers[offer_idx]
        try:
            sport = element.find_element(By.CLASS_NAME, "sport-naziv").text
        except:
            sport = ""

        if sport != "NOGOMET":
            continue

        print("\n---------------------\n", sport)
        panel_div = element.find_element(By.CLASS_NAME, "panel")
        exp_span = panel_div.find_element(By.CLASS_NAME, "icon")

        if not exp_span:
            continue

        click_element(driver, exp_span)

        time.sleep(0.5)

        league_container = driver.find_element(By.XPATH, '//div[contains(@class, "listbar") and contains(@class, "lige")]')
        league_elements = league_container.find_elements(By.CLASS_NAME, "listbar-item")

        leagues = {}
        for i, league_element in enumerate(league_elements):
            league_element = league_elements[i]
            timer = time.time()

            league = league_element.text

            #scroll_into_view_and_click(driver, league_element)
            #click_element(driver, league_element)
            #print(league_element.get_attribute())
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", league_element)
            time.sleep(0.5)
            league_element.click()
            time.sleep(0.5)

            layout_div = driver.find_element(By.CLASS_NAME, "sportska-liga")
            sector_div = layout_div.find_element(By.CLASS_NAME, "razrade")
            table_div = sector_div.find_element(By.CLASS_NAME, "razrada")
            rows = table_div.find_elements(By.CLASS_NAME, "ponuda")

            print()
            print("League:", league)
            print("---------------------")

            games = {}
            for j, row in enumerate(rows):
                layout_div = driver.find_element(By.CLASS_NAME, "layout-col")
                sector_div = layout_div.find_element(By.CLASS_NAME, "razrade")
                table_div = sector_div.find_element(By.CLASS_NAME, "razrada")
                row = table_div.find_elements(By.CLASS_NAME, "ponuda")[j]

                game = row.find_element(By.CLASS_NAME, "ponuda-naziv").text
                print("Game:", game)

                clickable = row.find_element(By.CLASS_NAME, "ponuda-info")
                click_element(driver, clickable)
                time.sleep(0.2)

                bet_sector = driver.find_element(By.CLASS_NAME, "ponude-razrada")
                bets = bet_sector.find_elements(By.XPATH, "./*")

                bet_coefficients = {}
                for bet in bets:
                    offers = bet.find_elements(By.XPATH, './div[contains(@class, "ponude")]')

                    if len(offers) > 1:
                        continue

                    coefficients_list = offers[0].find_elements(By.CLASS_NAME, "tecaj-tecaj")
                    coefficient_name_list = offers[0].find_elements(By.CLASS_NAME, "tecaj-naziv")
                    if len(coefficients_list) > 2:
                        continue

                    bet_name = bet.find_element(By.CLASS_NAME, "razrada-header").text

                    coefficients = {}
                    for idx, k in enumerate(coefficients_list):
                        odd = float(k.text.replace(",", "."))
                        tip = coefficient_name_list[idx].text
                        coefficients[tip] = odd

                    print(f"\t- {bet_name}: {coefficients}")
                    bet_coefficients[bet_name] = coefficients

                games[game] = bet_coefficients

                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", league_element)
                time.sleep(0.5)
                league_element.click()
                time.sleep(0.5)

            leagues[league] = games

            league_container = driver.find_element(By.XPATH, '//div[contains(@class, "listbar") and contains(@class, "lige")]')
            league_elements = league_container.find_elements(By.CLASS_NAME, "listbar-item")

            print(f"PROGRES ... {(i+1) / len(league_elements) * 100:.2f}%\n -> {league}\n ->{time.time() - timer:.3f}s")

        for league in leagues:
            print("\n")
            print("League:", league)
            print("---------------------")
            print()
            for game in leagues[league]:
                print("Game:", game)
                for bet in leagues[league][game]:
                    print(f"\t- {bet}: {leagues[league][game][bet]}")

        save_data(sport, day, leagues)
        break

    driver.quit()


def save_data(name, date, data):
    with open(os.path.join(DATA_FILE_PATH, f"supersport_{name}_{date}-{datetime.now().month}-{datetime.now().year}.json"), "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
