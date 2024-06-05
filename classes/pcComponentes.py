from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from product_scraper import ProductScraper

class pcComponentesScrapper(ProductScraper):
    def __init__(self, product):
      super().__init__(product, "PC Componentes", "https://www.pccomponentes.pt/")
      
    def open_browser(self):
      self.openPage()
      self.close_cookies()
      
    def scrape(self):
      self.open_browser()
      self.search_item()
      
    def close_cookies(self):
      sleep(1)
      print('Closing cookies')
      try:
        sleep(1)
        cookies_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "cookiesAcceptAll"))
        )
        cookies_button.click()
      except:
        print('No cookies button found')
        
    def search_item(self):
      search_bar = self.driver.find_element(By.XPATH,'//*[@id="search"]')
      search_bar.send_keys(self.product)
      # sleep(1)
      # search_bar = WebDriverWait(self.driver, 10).until(
      #     EC.presence_of_element_located((By.ID, "search"))
      # )
      # search_bar.click()
      # search_bar.send_keys(self.product)
      # search_bar.send_keys(Keys.RETURN)    
      
    
# def main():
#     x = pcComponentesScrapper("mouse gamer")
#     # x.open_browser()
#     # x.search_item()
#     #time.sleep(1)
#     x.scrape()
    
# Usage example
if __name__ == "__main__":
    scraper = pcComponentesScrapper("ryzen 5 3600")
    scraper.scrape()