import os
import re
import time


from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox import options as firefox_options


def get_driver(headless=False):
    """Returns a selenium firefox webdriver
    Args:
        headless (bool, optional): Whether to hide the browser. Defaults to False.
    Returns:
        selenium.webdriver.Firefox: firefox webdriver
    """
    if headless:
        options = firefox_options.Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        driver = webdriver.Firefox()
    return driver

def get_page(count=10,headless=False):
  driver = get_driver(headless=headless)

  pages = []

  for page_number in range(1, count+1):
    #page_url = f"https://www.logic-immo.com/vente-immobilier/options/grouplocalities=1_0,21_0,12_0,8_0,84_1,11_0,13_0/groupprptypesids=1,2/page={page_number}"
    page_url = f"https://www.seloger.com/list.htm?projects=2%2C5&types=2%2C1&natures=1%2C2%2C4&places=%5B%7B%22divisions%22%3A%5B2238%5D%7D%5D&enterprise=0&qsVersion=1.0&LISTING-LISTpg={page_number}"
    #page_url = f"https://www.leboncoin.fr/_immobilier_/offres/p-{page_number}"
    driver.get(page_url)
    time.sleep(13)
    pages.append(driver.page_source.encode("utf-8"))
  return pages

def save_pages(pages):
  os.makedirs("data", exist_ok=True)
  for page_nb, page in enumerate(pages):
    with open(f"data/page_{page_nb}.html", "wb") as f_out: 
      f_out.write(page)

def parse_pages():
  pages_paths = os.listdir("data")

  results = pd.DataFrame()
  results = pd.DataFrame()
  pages_paths = os.listdir("data")
  for pages_path in pages_paths:
      with open(os.path.join("data", pages_path), "rb") as f_in:
          page = f_in.read().decode("utf-8")
          results = results.append(parse_page(page))
  return results

def parse_page(page):

  soup = BeautifulSoup(page,"html.parser")
  result = pd.DataFrame()

  result["price (€)"] = [
     clean_price(tag) for tag in soup.find_all(attrs={"class": "Price__PriceWrapper-sc-1g9fitq-1 cHTIJq"})
  ]

  result["type"] = [
      clean_type(tag) for tag in soup.find_all(attrs={"class": "ContentZone__Title-wghbmy-4 clOuRb"})
  ]

  result["adresse"] = [
      clean_postal_code(tag) for tag in soup.find_all(attrs={"class": "ContentZone__Address-wghbmy-0 bZvSwz"})
  ]

  areas = soup.find_all(attrs={"class": "ContentZone__TagsLine-wghbmy-6 cNYziv"})
  result["description"] = [tag.text.strip() for tag in areas]
     

  # areas = soup.find_all(attrs={"class": "announceDtlPrice"})
  # areas = soup.find_all(attrs={"class": "Price__PriceContainer-sc-1g9fitq-0 knHjrC"})
  # #areas = soup.find_all(attrs={"class": "sc-fHxwqH hAXnvi"})
  # result["price"] = [tag.text.strip() for tag in areas]
  return result

def clean_price(tag):
    text = tag.text.strip()
    price = int(text.replace("€", "").replace(" ", ""))
    return price

def clean_type(tag):
    text = tag.text.strip()
    return text.replace("Location ", "")


def clean_surface(tag):
    text = tag.text.strip()
    return int(text.replace("m²", ""))


def clean_rooms(tag):
    text = tag.text.strip()
    rooms = int(text.replace("p.", "").replace(" ", ""))
    return rooms


def clean_postal_code(tag):
    text = tag.text.strip()
    match = re.match(".*\(([0-9]+)\).*", text)
    return match.groups()[0]


def main():
  #pages = get_page()
  #save_pages(pages)
  results = parse_pages()
  print("--------------------------------------------------------")
  print("--- LANCEMENT DU BOT DE WEBSCRAPPING SUR SELOGER.COM ---")
  print("-------------- NOMBRE DE PAGES VOULU : 10 --------------")
  print("--------------------------------------------------------")
  print(results)
main()
url = "https://www.logic-immo.com/vente-immobilier/options/grouplocalities=1_0,21_0,12_0,8_0,84_1,11_0,13_0/groupprptypesids=1,2/page=1"