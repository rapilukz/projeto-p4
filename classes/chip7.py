import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from product_scraper import ProductScraper

class chip7Scraper(ProductScraper):
    def closeCookies(self):
        pass
    def searchProduct(self):
        searchBar = self.driver.find_element(By.XPATH,'//*[@id="main-searchBox"]/div/form/input')
        searchBar.send_keys(self.product)
    def scrape(self):
        gridXpath = '//*[@id="main-hits"]/div/ol'
        linksXpath = './/a'
        productGrid = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, gridXpath))
        )
        
        elements = productGrid.find_elements(By.XPATH, linksXpath)
        hrefs = set([element.get_attribute('href') for element in elements if element.get_attribute('href')])
        
        print(f"Found {len(hrefs)} links in the page")

        for link in hrefs:
            self.driver.get(link)
            #get name
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
            rating = "-"
            review = []
            print(name, category, price, self.storeName, rating, nrReviews)
            print("----------------")
            time.sleep(1)