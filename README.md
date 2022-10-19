## Description

A simple script that scrapers the 'Top Sellers' page on [Steam.com](https://store.steampowered.com/search/?filter=topsellers&os=win). As of now, it scrapers only the aforementioned page, and the _game title_, _full price_, and _discounted price_ from this page.

## Prerequisites

In order they were used:

* [requests](https://requests.readthedocs.io/en/latest/) -> for accessing and retrieving the data.
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) -> for parsing the data.
* [pandas](https://pandas.pydata.org/) -> for converting data to CSV & saving it.

## How It Works

By running the program as it is, it will return a CSV file with the first 100 games scraped.

To change that, give as first argument to '_iterate_topsellers()_' function the number of games you want to retrieve the price. You can also change how many games to iterate through at once, by giving as second argument a number between 25 and 100. This is automatically set to 25.
