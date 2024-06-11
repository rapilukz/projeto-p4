from time import sleep
import pandas as pd
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NanochipScraper(ProductScraper):

    def __init__(self,driver):
        super().__init__("Nanochip",driver)

    def scrape_item(self, URL):
        self.driver.get(URL)
        sleep(2)
        info = self.get_item_info()
        self.add_item(info["name"], "Computer Parts", info["price"], info["store"], None, None, None)

    def get_item_info(self):
        try:
            name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div/main/div[2]/div[1]/div/div/div[1]/div/h1'))  
            ).text

            price = None
            price_xpaths = [
                '/html/body/div[3]/div/div/div[1]/div/div/main/div[2]/div[1]/div/div/div[1]/div/p[1]/span/span/bdi',
                '/html/body/div[3]/div/div/div[1]/div/div/main/div[2]/div[1]/div/div/div[1]/div/p[1]/span/ins/span/bdi'
            ]

            for xpath in price_xpaths:
                try:
                    price = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    ).text
                    break
                except:
                    continue

            product_details = {
                "name": name,
                "price": price,
                "store": self.storeName,
            }
            return product_details
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    scraper = NanochipScraper("rato gamer")
