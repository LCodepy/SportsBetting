import os
import json
import string

import requests
import pyautogui
from dotenv import load_dotenv
from unidecode import unidecode


load_dotenv()

API_KEY = os.environ["API_KEY"]
CX = os.environ["CX"]


# def get_club_name(query, api_key=API_KEY, cx=CX):
#     url = f"https://www.googleapis.com/customsearch/v1?q={query + ' football club'}&cx={cx}&key={api_key}&num=1"
#     response = requests.get(url)
#     data = response.json()
#     if "items" in data and len(data["items"]) > 0:
#         title = data["items"][0]["title"]
#         return title.split(" - ")[0]


def check_if_same_name(name1, name2):
    name1 = name1.split()
    name2 = name2.split()

    for word1 in name1:
        for word2 in name2:
            if word1 == word2:
                return True
    return False


def map_club_names(clubs):
    filtered_clubs = {b: [] for b in clubs}
    for b in clubs:
        for g in clubs[b]:
            club1, club2 = g
            club1 = " ".join(list((filter(lambda x: not (x.upper() and len(x) == 2) and not x.isnumeric(), club1.split()))))
            club2 = " ".join(list((filter(lambda x: not (x.upper() and len(x) == 2) and not x.isnumeric(), club2.split()))))
            filtered_clubs[b].append((club1, club2))

    name_mappings = {}

    for b in range(len(filtered_clubs.keys())-1):
        for g1 in filtered_clubs[list(filtered_clubs.keys())[b]]:
            for g2 in filtered_clubs[list(clubs.keys())[b+1]]:
                if check_if_same_name(g1[0], g2[0]):
                    if g1[0] not in name_mappings:
                        name_mappings[g1[0]] = g2[0]
                    if g2[0] not in name_mappings:
                        name_mappings[g2[0]] = g2[0]
                    if g1[1] not in name_mappings:
                        name_mappings[g1[1]] = g2[1]
                    if g2[1] not in name_mappings:
                        name_mappings[g2[1]] = g2[1]
                if check_if_same_name(g1[1], g2[1]):
                    if g1[1] not in name_mappings:
                        name_mappings[g1[1]] = g2[1]
                    if g2[1] not in name_mappings:
                        name_mappings[g2[1]] = g2[1]
                    if g1[0] not in name_mappings:
                        name_mappings[g1[0]] = g2[0]
                    if g2[0] not in name_mappings:
                        name_mappings[g2[0]] = g2[0]

    return name_mappings


def map_all_club_names(leagues, bookkeepers):
    mappings = {}

    for league in leagues:
        club_names = {b: [] for b in bookkeepers}
        for bookkeeper in bookkeepers:
            for game in bookkeepers_data[bookkeeper][league]:
                game_name = game.replace("\n", " ").replace(".", " ")
                if game_name.count("-") != 1:
                    continue
                club_names[bookkeeper].append(
                    (unidecode(game_name.split("-")[0].strip()), unidecode(game_name.split("-")[1].strip())))

        mappings[league] = map_club_names(club_names)

    return mappings


def get_club_name(league, name):
    name = " ".join(list((filter(lambda x: not (x.upper() and len(x) == 2 and x.upper()[0] in string.ascii_uppercase and x.upper()[1] in string.ascii_uppercase) and not x.isnumeric(), name.split())))).replace(".", " ").strip()
    if name not in club_names_mapping[league]:
        return
    return club_names_mapping[league][name]


countries = ['Afganistan', 'Albanija', 'Alžir', 'Andora', 'Angola', 'Antigva i Barbuda', 'Argentina', 'Armenija', 'Australija', 'Austrija', 'Azerbejdžan', 'Bahami', 'Bahrein', 'Bangladeš', 'Barbados', 'Belgija', 'Beliz', 'Benin', 'Bocvana', 'Bolivija', 'Bosna i Hercegovina', 'Brazil', 'Brunej', 'Bugarska', 'Burkina Faso', 'Burundi', 'Butan', 'Centralnoafrička Republika', 'Crna Gora', 'Danska', 'Dominika', 'Dominikanska Republika', 'Džibuti', 'Egipat', 'Ekvador', 'Ekvatorska Gvineja', 'Engleska', 'Eritreja', 'Estonija', 'Esvatini', 'Etiopija', 'Fidži', 'Filipini', 'Finska', 'Francuska', 'Gabon', 'Gambija', 'Gana', 'Grenada', 'Gruzija', 'Grčka', 'Gvajana', 'Gvatemala', 'Gvineja', 'Gvineja-Bisao', 'Haiti', 'Holandija', 'Honduras', 'Hrvatska', 'Indija', 'Indonezija', 'Irak', 'Iran', 'Irska', 'Island', 'Italija', 'Izrael', 'Jamajka', 'Japan', 'Jemen', 'Jordan', 'Južni Sudan', 'Južnoafrička Republika', 'Kambodža', 'Kamerun', 'Kanada', 'Katar', 'Kazahstan', 'Kenija', 'Kina', 'Kipar', 'Kirgistan', 'Kiribati', 'Kolumbija', 'Komori', 'Kongo', 'Kosovo', 'Kostarika', 'Kuba', 'Kuvajt', 'Laos', 'Latvija', 'Lesoto', 'Liban', 'Liberija', 'Libija', 'Lihtenštajn', 'Litva', 'Luksemburg', 'Madagaskar', 'Malavi', 'Maldivi', 'Malezija', 'Mali', 'Malta', 'Maroko', 'Maršalova Ostrva', 'Mauricijus', 'Mauritanija', 'Mađarska', 'Meksiko', 'Mikronezija', 'Mjanmar', 'Moldavija', 'Monako', 'Mongolija', 'Mozambik', 'Namibija', 'Nauru', 'Nemačka', 'Nepal', 'Niger', 'Nigerija', 'Nikaragva', 'Nizozemska', 'Norveška', 'Novi Zeland', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua Nova Gvineja', 'Paragvaj', 'Peru', 'Poljska', 'Portugal', 'Ruanda', 'Rumunjska', 'Rusija', 'Salvador', 'Samoa', 'San Marino', 'Sao Tome i Principe', 'Saudijska Arabija', 'Sejšeli', 'Senegal', 'Sierra Leone', 'Singapur', 'Sirija', 'Sjedinjene Američke Države', 'Sjeverna Koreja', 'Sjeverna Makedonija', 'Slovačka', 'Slovenija', 'Solomonova Ostrva', 'Somalija', 'Srbija', 'Sudan', 'Surinam', 'Sveti Kits i Nevis', 'Sveti Lucija', 'Sveti Vincent i Grenadini', 'Tadžikistan', 'Tajland', 'Tanzanija', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad i Tobago', 'Tunis', 'Turkmenistan', 'Turska', 'Tuvalu', 'Uganda', 'Ujedinjeni Arapski Emirati', 'Ujedinjeno Kraljevstvo', 'Ukrajina', 'Urugvaj', 'Uzbekistan', 'Vanuatu', 'Vatikan', 'Venecuela', 'Vijetnam', 'Zambija', 'Zelenortska Ostrva', 'Zimbabve', 'Čad', 'Češka', 'Čile', 'Škotska', 'Španjolska', 'Šri Lanka', 'Švicarska', 'Švedska']

bookkeepers = {}

with open("C:\\Users\\SKECPC\\Desktop\\ROOT\\Private\\Programming\\Big_projects\\Python\\SportsBettingAI\\data\\supersport\\supersport_NOGOMET_27-4-2024.json", "r", encoding="latin2") as file:
    bookkeepers["supersport"] = json.load(file)

with open("C:\\Users\\SKECPC\\Desktop\\ROOT\\Private\\Programming\\Big_projects\\Python\\SportsBettingAI\\data\\crobet\\crobet_NOGOMET_27-4-2024.json", "r", encoding="latin2") as file:
    bookkeepers["crobet"] = json.load(file)

bookkeepers_data = {b: {} for b in bookkeepers}
same_leagues = {b: set() for b in bookkeepers}
for bookkeeper, leagues in bookkeepers.items():
    leagues_sorted = sorted(leagues.keys())
    for league in leagues_sorted:
        league_data = bookkeepers[bookkeeper][league]
        league_name = league.replace("liga ", "").split("-")[0].strip().upper()
        if "ŽENE " in league_name:
            league_name.replace("ŽENE ", "")
            league_name += "(Ž)"
        idx = -1

        if league_name.split()[0] == "KINESKA":
            league_name = "KINA" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0] == "JUŽNOKOREJSKA":
            league_name = "JUŽNA KOREJA" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0] == "LITVANSKA":
            league_name = "LITVA" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0] == "SJEVERNOIRSKA":
            league_name = "SJEVERNA IRSKA" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0] == "TALIJANSKA":
            league_name = "ITALIJA" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0] == "ČILEANSKA":
            league_name = "ČILE" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0] == "PERUANSKA":
            league_name = "PERU" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0] == "MALTEŠKA":
            league_name = "MALTA" + " " + " ".join(league_name.split(" ")[1:])
        elif league_name.split()[0].lower().capitalize() not in countries:
            if "SKI " in league_name:
                idx = league_name.index("SKI ")
            elif "SKA " in league_name:
                idx = league_name.index("SKA ")

            if idx != -1:
                league_name.replace("SKI ", "")
                league_name.replace("SKA ", "")
                country = league_name[:idx]
                for c in countries:
                    if country in c.upper():
                        country = c.upper()
                        break
                league_name = country + " " + " ".join(league_name.split(" ")[1:])

        same_leagues[bookkeeper].add(league_name)
        bookkeepers_data[bookkeeper][league_name] = league_data

leagues = set()
for i in range(1, len(same_leagues.keys())):
    leagues1 = same_leagues[list(same_leagues.keys())[i-1]]
    leagues2 = same_leagues[list(same_leagues.keys())[i]]
    leagues = leagues.union(leagues1.intersection(leagues2))
leagues = list(sorted(leagues))

bet_names_mapping = {"ISHOD BEZ NERIJEŠENOG": "UTAKMICA BEZ NERIJEŠENOG", "OBA DAJU GOL 1.POL.": "OBA DAJU GOL U 1.POL."}

club_names_mapping = map_all_club_names(leagues, bookkeepers)
print(club_names_mapping)
bet_options = set()
game_bet_data = {l: {} for l in leagues}
for league in leagues:
    print("\n", league)
    print("--------------")

    for bookkeeper in bookkeepers:
        print(" ->", bookkeeper)

        games = bookkeepers_data[bookkeeper][league]
        for game in games:
            game_name = game.replace("\n", " ")
            if game_name.count("-") != 1:
                print(f"[APP] Skipped game {game_name!r} because of multiple hyphens.")
                continue

            club1 = get_club_name(league, unidecode(game_name.split("-")[0].strip()))
            club2 = get_club_name(league, unidecode(game_name.split("-")[1].strip()))
            if not club1 or not club2:
                print(f"[APP] Skipped game {game_name!r} because there isn't that game at the other bookkeeper.")
                continue
            filtered_game_name = club1 + " - " + club2

            reversed_name = False
            if filtered_game_name not in game_bet_data[league]:
                c1, c2 = filtered_game_name.split(" - ")
                if c2 + " - " + c1 in game_bet_data:
                    reversed_name = True
                    filtered_game_name = c2 + " - " + c1
                else:
                    game_bet_data[league][filtered_game_name] = {}

            print("    -", filtered_game_name)
            for bet in games[game]:
                bet_options.add(bet.upper())
                if bet.upper() not in game_bet_data[league][filtered_game_name]:
                    game_bet_data[league][filtered_game_name][bet.upper()] = {}
                if reversed_name:
                    keys = list(games[game][bet].keys())
                    values = list(games[game][bet].values())
                    game_bet_data[league][filtered_game_name][bet.upper()][bookkeeper] = {keys[0]: values[1], keys[1]: values[0]}
                else:
                    game_bet_data[league][filtered_game_name][bet.upper()][bookkeeper] = games[game][bet]
                print("    ->", game_bet_data[league][filtered_game_name][bet.upper()][bookkeeper])

arbitrages = {}
print("\n"*5)
for league in game_bet_data:
    print()
    print(league)
    for game in game_bet_data[league]:
        print("  ->", game)
        for bet_option in bet_options:
            if bet_option in game_bet_data[league][game]:
                print("      ->", bet_option)
                max_coefficient1 = 1
                bookkeeper1 = ""
                max_coefficient2 = 1
                bookkeeper2 = ""
                for bookkeeper in bookkeepers:
                    if bookkeeper not in game_bet_data[league][game][bet_option]:
                        continue
                    print(f"          - {bookkeeper}: {game_bet_data[league][game][bet_option][bookkeeper]}")
                    bets = list(game_bet_data[league][game][bet_option][bookkeeper].values())
                    if bets[0] > max_coefficient1:
                        max_coefficient1 = bets[0]
                        bookkeeper1 = bookkeeper
                    if bets[1] > max_coefficient1:
                        max_coefficient2 = bets[1]
                        bookkeeper2 = bookkeeper

                arb = 1 / max_coefficient1 + 1 / max_coefficient2
                if arb < 1:
                    print("          - ARBITRAGE: ", round(arb * 100, 3))

                    if game not in arbitrages:
                        arbitrages[game] = []
                    arbitrages[game].append((bet_option, round(arb * 100, 3)))

print(arbitrages)
