import pandas as pd
from selenium import webdriver
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonScraper(ProductScraper):
    def __init__(self, URL):
        super().__init__("Amazon", URL)


    def search_item(self):
        self.openPage()
        id = "twotabsearchtextbox"
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, id)))
        self.search_bar = self.driver.find_element(id)
        self.search_bar.send_keys("motherboard")
        self.send_keys(Keys.RETURN)
        
if __name__ == "__main__":
    URL = "https://www.amazon.com"
    scraper = AmazonScraper(URL)