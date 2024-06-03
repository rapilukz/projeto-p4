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
        print('Scraping Worten')
        self.open_browser()
        self.search_item()
        self.scrape_items()
        self.to_csv("worten.csv")
        
    def scrape_items(self):
        sleep(1)
        links = self.get_links()
        for link in links:
            self.driver.get(link)
            info = self.get_item_info()
            self.add_item(info["name"], info["category"], info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])

    def get_item_info(self):
        sleep(1)
        product_name = self.driver.find_element(By.CSS_SELECTOR, ".title").text
        print('Scraping: ', product_name)
        unformated_price = self.driver.find_element(By.CSS_SELECTOR, ".value").text
        price = '€' + ''.join(unformated_price.split())
        category = self.driver.find_elements(By.CSS_SELECTOR, ".breadcrumbs__item__name")[-1].text
        rating = self.get_rating()
        reviews_nr = self.get_reviews_number()
        store = self.storeName
        reviews = []

        product_info = {
            "name": product_name,
            "price": price,
            "category": category,
            "store": store,
            "ratings": rating,
            "reviews_nr": reviews_nr,
            "reviews": reviews
        }

        return product_info
    
    def get_links(self):
        links = []
        products = self.driver.find_elements(By.CSS_SELECTOR, ".product-card--grid-container a")
        for product in products:
            links.append(product.get_attribute("href"))
        
        return links[:20]
    
    def get_rating(self):
        try:
            rating = self.driver.find_element(By.CSS_SELECTOR, ".rating__star-value.semibold span").text
        except:
            rating = "N/A"
        
        return rating
    
    def get_reviews_number(self):
        try :
            reviews_nr = int(self.driver.find_element(By.CSS_SELECTOR, ".rating__opinions span").text.split(" ")[0])
        except:
            reviews_nr = "N/A"
        
        return reviews_nr

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