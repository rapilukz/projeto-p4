import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from classes.product_scraper import ProductScraper

class chip7Scraper(ProductScraper):
    def __init__(self, driver):
        super().__init__("Chip7", driver)

    def scrape_item(self, URL):
        self.driver.get(URL)
        # self.close_cookies()
        info = self.get_item_info()
        # print(info)
        self.add_item(info["name"], info["category"], info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])

    def get_item_info(self):
        time.sleep(1)
        nameXpath = '//*[@id="content"]/div[1]/div[2]/div[2]/h1'
        name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, nameXpath))
        )
        name = name.text
        # print(name)
        
        #get category
        categoryXpath = '//*[@id="content"]/div[1]/div[1]/div/nav/ol/li[1]/div/a'
        category = self.driver.find_element(By.XPATH, categoryXpath)
        category = category.text
        # print(category)
        
        #get price
        priceXpath = '//*[@id="content"]/div[1]/div[2]/div[2]/div[5]/div[1]/div'
        price = self.driver.find_element(By.XPATH, priceXpath)
        price = price.text
        # print(price)
    
        #get nr_reviews
        nrReviews = 0
        print(nrReviews)
        rating = "N/A"
        reviews = []

        # print(rating)
        # print(reviews)
        product_info = {
            "name": name,
            "price": price,
            "category": category,
            "store": self.storeName,
            "ratings": rating,
            "reviews_nr": nrReviews,
            "reviews": reviews
        }
        return product_info