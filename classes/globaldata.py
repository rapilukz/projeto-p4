from time import sleep
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GlobalDataScraper(ProductScraper):
    def __init__(self, product):
        super().__init__(product, "GlobalData", "https://www.globaldata.pt/")

    def scrape(self):
        self.open_browser()
        self.search_item()
        self.scrape_items()

    def open_browser(self):
        self.open_sealth_browser()
        self.close_cookies()

    def scrape_items(self):
        sleep(1)
        links = self.get_links()
        print(f"Found {len(links)} items")
        for link in links:
            self.driver.get(link)
            info = self.get_item_info()
            # self.add_item(info["name"], "Computer Parts", info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])

    def get_item_info(self):
        name = self.driver.find_element(By.CSS_SELECTOR, "h1.mb-0.h4.h2-md").text
        print("Scrapping: ", name)

    def close_cookies(self):
        print('Closing cookies')
        self.driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()

    def search_item(self):
        sleep(1)
        search_bar = self.driver.find_element(By.XPATH, "/html/body/header/div[2]/div[4]/div/form/input")
        search_bar.click()
        search_bar.send_keys(self.product)
        search_bar.send_keys(Keys.RETURN)

    def get_links(self):
        sleep(1)
        links = []
        products = self.driver.find_elements(By.CSS_SELECTOR, "[data-widget='hits'] .row")
        # only loop through the first 20 products
        for product in products[:20]:
            link = product.find_element(By.CSS_SELECTOR, "a.text-inherit.text-decoration-none.js-gtm-product-link-algolia").get_attribute("href")
            links.append(link)
    
        return links

# Usage example
if __name__ == "__main__":
    scraper = GlobalDataScraper("ryzen 5 3600")
    try:
        scraper.scrape()
    finally:
        scraper.close_browser()