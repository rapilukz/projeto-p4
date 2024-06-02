from time import sleep
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class WortenScrapper(ProductScraper):
    def __init__(self, product):
        super().__init__(product, "Worten   ", "https://www.worten.pt/")

    def open_browser(self):
        self.openPage()
        self.close_cookies()

    def scrape(self):
        self.open_browser()
        self.search_item()

    def close_cookies(self):
        sleep(1)
        print('Closing cookies')
        cookies_button = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/section/footer/button[3]")
        cookies_button.click()

    def search_item(self):
        sleep(1)
        search_bar = self.driver.find_element(By.ID, "search")
        search_bar.click()
        search_bar.send_keys(self.product)
        search_bar.send_keys(Keys.RETURN)


# Usage example
if __name__ == "__main__":
    scraper = WortenScrapper("ryzen 5 3600")
    try:
        scraper.scrape()
    finally:
        scraper.close_browser()