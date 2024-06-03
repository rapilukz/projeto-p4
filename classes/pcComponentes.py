
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class pcComponentesScrapper(ProductScraper):
    def __init__(product, self, URL):
      super().__init__(product, "PC Componentes", "https://www.pccomponentes.pt/")
      
    def open_browser(self):
      self.openPage()
      
    def scrape(self):
      self.open_browser()
      self.search_item()
      
    def search_item(self):
      search_bar = self.driver.find_element(By.ID, "search")
      search_bar.click()
      search_bar.send_keys(self.product)
      search_bar.send_keys(Keys.RETURN)    
      
if __name__ == "__main__":
  scraper = pcComponentesScrapper("nvidia geforce rtx 3060 ti")
  try:
    scraper.scrape()
  finally:
    scraper.close_browser()