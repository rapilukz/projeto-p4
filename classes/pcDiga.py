import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from product_scraper import ProductScraper

class pcDigaScraper(ProductScraper):
    def closeCookies(self):
        pass
    def searchProduct(self):
        searchBar = self.driver.find_element(By.XPATH,'//*[@id="searchbar"]')
        searchBar.send_keys(self.product)
    def scrape(self):
        gridXpath = '//*[@id="body-overlay"]/div[2]/div[1]/main/div/div[2]/div[2]/div[2]/div[1]'
        linksXpath = './/a'
        productGrid = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, gridXpath))
        )
        
        elements = productGrid.find_elements(By.XPATH, linksXpath)
        hrefs = set([element.get_attribute('href') for element in elements if element.get_attribute('href')])
        
        print(f"Found {len(hrefs)} links in the page")
        # print(hrefs)

        for link in hrefs:
            self.driver.get(link)
            #get name
            nameXpath = '//*[@id="body-overlay"]/div[2]/div[1]/main/div[2]/div[2]/div/div/h1'
            name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, nameXpath))
            )
            print(name.text)
            
            #get category
            categoryXpath = '//*[@id="body-overlay"]/div[2]/div[1]/main/div[1]/div[1]/nav/ol/li[2]/a'
            category = self.driver.find_element(By.XPATH, categoryXpath)
            print(category.text)
            
            #get price
            priceXpath = '//*[@id="body-overlay"]/div[2]/div[1]/main/div[2]/div[2]/div/div/div[1]/div/div[1]/div'
            price = self.driver.find_element(By.XPATH, priceXpath)
            print(price.text)
            
            #get rating
            # ratingsButtonXpath = '//*[@id="tablist-component-tab-tablist-tab-2"]'
            # scoreXpath = '//*[@id="tp-widget-wrapper"]/div/div[1]/div[1]/div[2]/span[1]'

            # ratingButton = self.driver.find_element(By.XPATH, ratingsButtonXpath)
            # ratingButton.click()

            # # Wait for the rating element and get the text
            # try:
            #     rating = WebDriverWait(self.driver, 3).until(
            #         EC.presence_of_element_located((By.XPATH, scoreXpath))
            #     )
            #     rating_value = rating.text
            # except TimeoutException:
            #     rating_value = 'NULL'


            # print(f"Rating: {rating_value}/5")
            
            
            #get reviews
            
            
            #get review_nr
            #

            print("----------------")
            time.sleep(1)

def main():
    x = pcDigaScraper("mouse gamer","PCDiga", "https://www.pcdiga.com/")
    x.openPage()
    x.searchProduct()
    time.sleep(1)
    x.scrape()
    
if __name__ == "__main__":
    main()