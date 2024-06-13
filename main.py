from classes.amazon import AmazonScraper
from classes.worten import WortenScrapper
from classes.nanochip import NanochipScraper
from utils.products import products
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Initialize the webdriver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

## Initialize the scrapers
worten = WortenScrapper(driver)
amazon = AmazonScraper(driver)
nanochip = NanochipScraper(driver)

## Scrape the products
driver.get("https://www.google.com")
for idx, product in enumerate(products):
    print(f"Scraping {product}... {idx + 1}/{len(products)}")
    amazon.scrape_item(products[product]["amazon"])
    worten.scrape_item(products[product]["worten"])
    nanochip.scrape_item(products[product]["nanochip"])

## Save the data
amazon.to_csv("amazon.csv")
worten.to_csv("worten.csv")
nanochip.to_csv("nanochip.csv")

driver.close()