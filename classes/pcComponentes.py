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
      print("Scrapping PC Componentes")
      self.open_browser()
      print("Browser opened")
      self.search_item()
      self.scrape_items()
      self.to_csv("pcComponentes.csv")
      
    def scrape_items(self):
      sleep(1)
      links = self.get_links()  
      for link in links:
        self.driver.get(link)
        info = self.get_item_info()
        self.add_item(info["name"], info["price"])
    
    def get_item_info(self):
      sleep(1)
      product_name = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, "pdp-title"))
      ).text
      print('Scraping: ', product_name)
      
      unformated_price = self.driver.find_element(By.ID, "pdp-price-current-integer").text
      price = '€' + ''.join(unformated_price.split())
      
      product_info = {
        "name": product_name,
        "price": price
      }
      
      return product_info
    
    def get_links(self):
      links = []
      products = WebDriverWait(self.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sc-dhKdcB cxbDvY sc-fvwjDU bpDGAZ sc-hXCwRK ctOovi algolia-tracked"))
      )
      for product in products:
        links.append(product.get_attribute("href"))
        
      return links[:20]
      
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
      sleep(1)
      # search_bar = WebDriverWait(self.driver, 10).until(
      #   EC.presence_of_element_located((By.ID, "search"))
      # )
      search_bar = self.driver.find_element(By.ID,"search")
      print("Estou aqui")
      search_bar.click()
      print("Agora aqui")      
      search_bar.send_keys(self.product)
      print("Item found")
          
# Usage example
if __name__ == "__main__":
    scraper = pcComponentesScrapper("Ryzen 5 3600")
    try:
      scraper.scrape()
    finally:
      # scraper.close_browser()
      print("Pode fechar")