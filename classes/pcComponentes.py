import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from classes.product_scraper import ProductScraper

from seleniumbase import Driver

class pcComponentesScraper(ProductScraper):
    def __init__(self, driver):
        super().__init__("PC Componentes", driver)

    def close_cookies(self):
        try:
            cookies_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="cookiesrejectAll"]'))
            )
            cookies_button.click()
        except:
            pass
    
    def open_sealth_browser(self):
        self.driver = Driver(uc=True)
        # self.driver.get(self.URL)

    def scrape_item(self, URL, shortName):
        self.open_sealth_browser()
        self.driver.get(URL)
        self.close_cookies()
        info = self.get_item_info()
        self.close_browser()
        # print(info)
        self.add_item(shortName, info["name"], info["category"], info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])

    def get_item_info(self):
        time.sleep(1)
        nameXpath = '//*[@id="pdp-title"]'
        name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, nameXpath))
        )
        name = name.text.replace(",",";")
        # print(name)

        #get category
        categoryXpath = '//*[@id="root"]/main/div[1]/nav/div[1]/div[2]/a'
        category = self.driver.find_element(By.XPATH, categoryXpath)
        category = category.text.replace(",",";")
        # print(category)
        
        #get price
        priceXpath = '//*[@id="pdp-price-current-integer"]'
        test = '//*[@id="up-pdp-section-buybox"]/div[1]/div'
        price = self.driver.find_element(By.XPATH, priceXpath)
        price = price.get_attribute("innerText").replace(",", ".")[:-1]
        # print(f"The price is {price}")
        
        #get nr_reviews
        nrXpath = '//*[@id="pdp-section-opinion-info"]/span'
        try:
            nrReviews = self.driver.find_element(By.XPATH, nrXpath)
            nrReviews = nrReviews.text.split()[0][1:]
        except:
            nrReviews = 0
        # print(nrReviews)
        
        rating = "N/A"
        reviews = []
        if nrReviews != 0:
            #get rating
            ratingXpath = '//*[@id="product-summary"]/div[1]/div[1]/div/div[1]'
            rating = self.driver.find_element(By.XPATH, ratingXpath)
            rating = rating.text

            #get reviews
            reviewsCSSselector = ".sc-camqpD.jzxKEN.sc-klSPgc.fihMce"
            reviews = self.driver.find_elements(By.CSS_SELECTOR, reviewsCSSselector)
            reviews = [x.text for x in reviews]
            

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