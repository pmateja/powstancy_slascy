#!/usr/bin/env python3

import os
import sys
from requests import get
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
import json


"""
It's just a simple script to download names of Silesian insurgents from museum page.
Why? Because the site is down. Ok, but why? I'm using those names in my horror stories. It's just a nice name database.
The site is now available on archive.org.

"""


def get_page(url):
    page = get(url)
    return page.content


def get_pages_urls(url):
    print("Fetching pages from {}".format(url))
    page = get_page(url)
    try:
        page = BeautifulSoup(page, "html.parser")
        select = page.find("select")
        return [i.get("value") for i in select.find_all("option")]
    except:
        return [url]


def get_alphabet_urls(url):
    print("Fetching alphabet from {}".format(url))
    page = get_page(url)
    page = BeautifulSoup(page, "html.parser")
    div = page.find(id="literki")
    return [i.get("href") for i in div.find_all("a")]


def get_data(url):
    print("Fetching data from {}".format(url))
    page = get_page(url)
    page = BeautifulSoup(page, "html.parser")
    table = page.find(id="lista_osob")
    names = []
    try:
        for tr in table.find_all("tr")[1:]:
            last_name = tr.find("td")
            first_name = last_name.find_next()
            place = first_name.find_next()
            names.append({
                "First name": first_name.text,
                "Lase name": last_name.text,
                "Place": place.text
                })
        return names
    except:
        return []

def run():
    base_url = "http://web.archive.org/web/20160412234021/http://phps.muzeumslaskie.pl/"
    index = "powstancy.php"
    database = []
    for alphabet_url in get_alphabet_urls(urljoin(base_url, index)):
        pages = get_pages_urls(urljoin(base_url, alphabet_url))
        if len(pages) == 0:
            pages.append(alphabet_page)
        for page_url in pages:
            database += get_data(urljoin(base_url, page_url))
    with open("output.json", "w") as f:
        f.write(json.dumps(database, sort_keys=True, indent=4))



if __name__ == "__main__":
    run()
