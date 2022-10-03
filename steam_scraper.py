import requests
import pathlib
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

ROOT = pathlib.Path(__file__).parent
FILE = ROOT.joinpath("steam_topsellers.csv")

try:
    topsellers = "https://store.steampowered.com/search/results/?query&start=0&count=100&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&os=win&infinite=1"
except requests.exceptions.RequestException as error:
    print(error)

def get_data(url:str):
    r = requests.get(url)
    data = dict(r.json())

    return data["results_html"]

def get_total_results(url:str):
    """Returns the total number of games found in a category."""
    r = requests.get(url)
    data = dict(r.json())
    results = data["total_count"]

    return int(results)

def parse_data(data:str):
    """Returns a list with dictionaries that contain the game title, price and the discounted price for each game."""
    games_list = []

    soup = BeautifulSoup(data, "html.parser")
    games = soup.find_all("a")

    for game in games:
        title = game.find("span", {"class" : "title"}).text
        price = game.find("div", {"class" : "search_price"}).text.strip().split("€")[0]
        
        try:
            discounted_price = game.find("div", {"class" : "search_price"}).text.strip().split("€")[1]
        except:
            discounted_price = price

        my_game = {
            "title" : title,
            "price" : price,
            "discounted_price" : discounted_price
        }

        games_list.append(my_game)

    return games_list

def export_to_csv(list):
    """Converts a list given as parameter in a CSV file."""
    dataframe = pd.concat(pd.DataFrame(i) for i in list)
    dataframe.to_csv(FILE, index = False)

def iterate_topsellers(stop = 100, count = 25):
    """Returns a new CSV file which contains the topselling games on Steam.com. By default it will return the first 100 topselling games.
    
    Args:
        * stop -> (int): how many games should be returned. Default is 100.
        * count > (int): how many games to iterate through at once. Default is 25.

    Raises:
        * ValueError: if stop is less than 25 or more than the total number of games found in the topsellers category.
        * ValueError: if count is less than 25 or more than 100. 
    """

    if stop < 25 or stop > get_total_results(topsellers):
        raise ValueError(f"stop parameter cannot be less than 25 or more than {get_total_results(topsellers)}.")
    if count < 25 or count > 100:
        raise ValueError("count parameter cannot be less than 25 or more than 100.")

    results = []

    print("Games scraped:")
    for i in range(0, stop, count):
        scraped_data = get_data(f"https://store.steampowered.com/search/results/?query&start={i}&count={count}&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&os=win&infinite=1")
        results.append(parse_data(scraped_data))

        print(i + count)
        sleep(0.5)

    print("Done. Results were converted to CSV.")

    export_to_csv(results)

iterate_topsellers()