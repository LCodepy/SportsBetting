import json
import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import click_element


DATA_FILE_PATH = "\\".join(__file__.split("\\")[:-2]) + "\\data\\crobet\\"


def main():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    day = "27.04.2024"

    url = f"https://www.lutrija.hr/crobet#/sport/SearchBySport=0&Day='{day}'"
    driver.get(url)

    time.sleep(4)

    sport_offers = driver.find_elements(By.CLASS_NAME, value="c-offer-sport")
    for element in sport_offers:
        if element.text != "NOGOMET":
            continue

        sport = element.text

        print("\n---------------------\n", element.text)
        exp_span = element.find_element(By.CLASS_NAME, "exp")

        if not exp_span:
            continue

        try:
            click_element(driver, exp_span)
        except:
            try:
                accept_cookies_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                accept_cookies_btn.click()
                time.sleep(1)
                exp_span.click()
            except:
                pass

        time.sleep(1)

        sport_offer_divs = driver.find_elements(By.XPATH, '//div[contains(@class, "c-offer-sport") and contains(@class, "open")]')
        for idx, sport_offer_div in enumerate(sport_offer_divs):
            if element.text == sport_offer_div.text:
                break
        expandable = sport_offer_divs[idx].find_element(By.CLASS_NAME, "expandable")
        league_elements = expandable.find_elements(By.CLASS_NAME, "c-offer-competition")

        leagues = {}
        for i, league_element in enumerate(league_elements):
            timer = time.time()

            click_element(driver, league_element)
            time.sleep(0.5)

            sector_div = driver.find_element(By.CLASS_NAME, "sektor-selected")
            table_div = sector_div.find_element(By.XPATH, '//div[contains(@class, "competition") and contains(@class, "nogomet")]')
            rows = table_div.find_elements(By.TAG_NAME, "tbody")[1:]

            league = table_div.find_element(By.CLASS_NAME, "selected-competition").text
            # print()
            # print("League:", league)
            # print("---------------------")

            games = {}
            for row in rows:
                game = row.find_element(By.CLASS_NAME, "match").find_elements(By.TAG_NAME, "span")[-1].text
                # print("Game:", game)

                clickable = row.find_element(By.CLASS_NAME, "event")
                if not click_element(driver, clickable):
                    # print("Not clickable.")
                    continue

                bet_sector = driver.find_element(By.CLASS_NAME, "sektor-details")
                while True:
                    try:
                        submenu = bet_sector.find_element(By.CLASS_NAME, "bb-submenu")
                        break
                    except:
                        time.sleep(0.1)

                all_bets_button = submenu.find_elements(By.TAG_NAME, "span")[-1]

                click_element(driver, all_bets_button)
                time.sleep(0.2)

                bets = bet_sector.find_elements(By.CLASS_NAME, "betevent")

                bet_coefficients = {}
                for bet in bets:
                    coefficients_list = bet.find_elements(By.CLASS_NAME, "playtip")
                    if len(coefficients_list) > 2:
                        continue

                    bet_name = bet.find_element(By.CLASS_NAME, "subheader-name").text[1:]

                    coefficients = {}
                    for k in coefficients_list:
                        tip = k.find_element(By.CLASS_NAME, "tip").text
                        coefficients[tip] = float(k.find_element(By.CLASS_NAME, "odd").text.replace(",", "."))

                    # print(f"\t- {bet_name}: {coefficients}")
                    bet_coefficients[bet_name] = coefficients

                games[game] = bet_coefficients

            leagues[league] = games

            print(f"PROGRES ... {(i+1) / len(league_elements) * 100:.2f}%\n -> {league}\n -> {time.time() - timer:.3f}s")

        for league in leagues:
            print("\n")
            print("League:", league)
            print("---------------------")
            print()
            for game in leagues[league]:
                print("Game:", game)
                for bet in leagues[league][game]:
                    print(f"\t- {bet}: {leagues[league][game][bet]}")

        save_data(sport, day.split(".")[0], leagues)
        break

    driver.quit()


def save_data(name, date, data):
    with open(os.path.join(DATA_FILE_PATH, f"crobet_{name}_{date}-{datetime.now().month}-{datetime.now().year}.json"), "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
