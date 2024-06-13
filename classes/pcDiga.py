import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from classes.product_scraper import ProductScraper

class pcDigascraper(ProductScraper):
    def __init__(self, driver):
        super().__init__("PC Diga", driver)
        
    def searchProduct(self):
        searchBar = self.driver.find_element(By.XPATH,'//*[@id="searchbar"]')
        searchBar.send_keys(self.product)

    def scrape_item(self, URL):
        self.driver.get(URL)
        # self.close_cookies()
        info = self.get_item_info()
        # print(info)
        self.add_item(info["name"], info["category"], info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])

    def get_item_info(self):
        time.sleep(1)
        nameXpath = '//*[@id="body-overlay"]/div[2]/div[1]/main/div[2]/div[2]/div/div/h1'
        name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, nameXpath))
        )
        name = name.text
        # print(name)

        #click on ratings tab
        ratingsButtonXpath = '//*[@id="tablist-component-tab-tablist-tab-2"]'
        ratingButton = self.driver.find_element(By.XPATH, ratingsButtonXpath)
        ratingButton.click()
        
        #get category
        categoryXpath = '//*[@id="body-overlay"]/div[2]/div[1]/main/div[1]/div[1]/nav/ol/li[2]/a'
        category = self.driver.find_element(By.XPATH, categoryXpath)
        category = category.text
        # print(category)
        
        #get price
        priceXpath = '//*[@id="body-overlay"]/div[2]/div[1]/main/div[2]/div[2]/div/div/div[1]/div/div[1]/div'
        price = self.driver.find_element(By.XPATH, priceXpath)
        price = price.text
        # print(price)

        iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
        self.driver.switch_to.frame(iframe)
        
        #get nr_reviews
        nrXpath = '//*[@id="numberOfReviews"]/strong'
        try:
            nrReviews = self.driver.find_element(By.XPATH, nrXpath)
            nrReviews = 0
        except:
            nrReviews = self.driver.find_element(By.XPATH, '//*[@id="numberOfReviews"]')
            nrReviews = nrReviews.text.split()[0]
        # print(nrReviews)
        
        rating = "N/A"
        reviews = []
        if nrReviews != 0:

            self.driver.switch_to.default_content()
            iframe2Xpath = '//*[@id="tablist-component-tab-tablist-tabpanel-2"]/div/div/div/div/iframe'
            iframe2 = self.driver.find_element(By.XPATH, iframe2Xpath)
            
            self.driver.switch_to.frame(iframe2)
            #get rating
            ratingXpath = '//*[@id="tp-widget-wrapper"]/div/div[1]/div[1]/div[2]/span[1]'
            rating = self.driver.find_element(By.XPATH, ratingXpath)
            rating = rating.text
            # print(f"Rating: {rating}")
            
            #get reviews
            reviews = WebDriverWait(self.driver, 25).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "tp-widget-review__text"))
            )
            # print(f"{len(reviews)} number of reviews on the first page")
            reviews = [r.find_element(By.TAG_NAME, 'span').text for r in reviews]

        self.driver.switch_to.default_content()

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