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
    with open(f"data/page={page_nb}.html", "wb") as f_out: 
      f_out.write(page)

def parse_pages():
    pages_paths = os.listdir("data")

    # Filter out non-HTML files
    pages_paths = [f for f in pages_paths if f.endswith(".html")]

    results = pd.DataFrame()
    for pages_path in pages_paths:
        with open(os.path.join("data", pages_path), "rb") as f_in:
            page = f_in.read().decode("utf-8")
            results = results.append(parse_page(page))
    return results


def parse_page(page):
    soup = BeautifulSoup(page,"html.parser")
    result = pd.DataFrame()
    
    # Extract price
    price_tag = soup.find("span", class_="announceDtlPrice")
    price = price_tag.text.strip() if price_tag else None
    result["price"] = [price]
    
    # Extract type
    prop_type_tag = soup.find("span", class_="announceDtlInfosPropertyType")
    prop_type = prop_type_tag.text.strip() if prop_type_tag else None
    result["type"] = [prop_type]
    
    # Extract address
    address_tag = soup.find("div", class_="announcePropertyLocation")
    address = address_tag.text.strip() if address_tag else None
    result["address"] = [address]
    
    # Extract surface
    surface_tag = soup.find("span", class_="announceDtlInfos announceDtlInfosArea")
    surface = surface_tag.text.strip() if surface_tag else None
    result["surface"] = [surface]
    
    # Extract bedroom count
    bedrooms_tag = soup.find("span", class_="announceDtlInfos announceDtlInfosNbRooms bullet")
    bedrooms = bedrooms_tag.text.strip() if bedrooms_tag else None
    result["bedrooms"] = [bedrooms]
    
    return result



# def parse_page(page):

#   soup = BeautifulSoup(page,"html.parser")
#   result = pd.DataFrame()

#   result["price (€)"] = [
#      clean_price(tag) for tag in soup.find_all(attrs={"class": "announceDtlPrice"})
#   ]

#   result["type"] = [
#       clean_type(tag) for tag in soup.find_all(attrs={"class": "announceDtlInfosPropertyType"})
#   ]

#   result["adresse"] = [
#       clean_postal_code(tag) for tag in soup.find_all(attrs={"class": "announcePropertyLocation"})
#   ]

#   # areas = soup.find_all(attrs={"class": "ContentZone__TagsLine-wghbmy-6 cNYziv"})
#   # result["description"] = [tag.text.strip() for tag in areas]


#   m2 = soup.find_all(attrs={"class": "announceDtlInfos announceDtlInfosArea"})
#   result["surface"] = [tag.text.strip() for tag in m2] 

#   nbrePiece = soup.find_all(attrs={"class": "announceDtlInfos announceDtlInfosNbRooms bullet"})
#   result["nbrePiece"] = [tag.text.strip() for tag in nbrePiece]   
     

#   # areas = soup.find_all(attrs={"class": "announceDtlPrice"})
#   # areas = soup.find_all(attrs={"class": "Price__PriceContainer-sc-1g9fitq-0 knHjrC"})
#   # #areas = soup.find_all(attrs={"class": "sc-fHxwqH hAXnvi"})
#   # result["price"] = [tag.text.strip() for tag in areas]
#   return result

def clean_price(tag):
    text = tag.text.strip()
    price = int(text.replace("€", "").replace(" ", "").replace("\xa0", ""))
    return price

# def clean_price(tag):
#     text = tag.text.strip()
#     price = int(text.replace("€", "").replace(" ", ""))
#     return price

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
  print("-------------- NOMBRE DE PAGES VOULU : 500 --------------")
  print("--------------------------------------------------------")
  print(results)
main()
url = "https://www.logic-immo.com/vente-immobilier/options/grouplocalities=1_0,21_0,12_0,8_0,84_1,11_0,13_0/groupprptypesids=1,2/page=1"