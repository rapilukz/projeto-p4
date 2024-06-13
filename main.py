from classes.amazon import AmazonScraper
from classes.worten import Wortenscraper
from classes.nanochip import NanochipScraper
from classes.chip7 import chip7Scraper
from classes.pcDiga import pcDigascraper
from classes.pccomponentes import pcComponentesscraper
from utils.products import products
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Initialize the webdriver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

## Initialize the scrapers
worten = Wortenscraper(driver)
amazon = AmazonScraper(driver)
nanochip = NanochipScraper(driver)
chip7 = chip7Scraper(driver)
pcDiga = pcDigascraper(driver)
# pcComponentes = pcComponentesscraper(driver)

## Scrape the products
driver.get("https://www.google.com")
for idx, product in enumerate(products):
    print(f"Scraping {product}... {idx + 1}/{len(products)}")
    amazon.scrape_item(products[product]["amazon"])
    worten.scrape_item(products[product]["worten"])
    nanochip.scrape_item(products[product]["nanochip"])
    chip7.scrape_item(products[product]["chip7"])
    pcDiga.scrape_item(products[product]["pcdiga"])
    # pcComponentes.scrape_item(products[product]["pcComponentes"])

## Save the data
amazon.to_csv("amazon.csv")
worten.to_csv("worten.csv")
nanochip.to_csv("nanochip.csv")
chip7.to_csv("chip7.csv")
pcDiga.to_csv("pcdiga.csv")
# pcComponentes.to_csv("pcComponentes.csv")

driver.close()