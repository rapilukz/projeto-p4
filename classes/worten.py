from time import sleep
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WortenScrapper(ProductScraper):
    def __init__(self, driver):
        super().__init__("Worten", driver)

    def scrape_item(self, URL):
        self.driver.get(URL)
        self.close_cookies()
        info = self.get_item_info()
        self.add_item(info["name"], info["category"], info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])

    def get_item_info(self):
        sleep(1)
        product_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".title"))
        ).text
        
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
    
    def get_rating(self):
        try:
            rating = self.driver.find_element(By.CSS_SELECTOR, ".rating__star-value.semibold span").text
        except:
            rating = "N/A"
        
        return rating
    
    def get_reviews_number(self):
        try:
            reviews_nr = int(self.driver.find_element(By.CSS_SELECTOR, ".rating__opinions span").text.split(" ")[0])
        except:
            reviews_nr = "N/A"
        
        return reviews_nr

    def close_cookies(self):
        sleep(1)
        try:
            cookies_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div/section/footer/button[3]"))
            )
            cookies_button.click()
        except:
            pass

# Usage example
if __name__ == "__main__":
    scraper = WortenScrapper()
    try:
        scraper.scrape()
    finally:
        scraper.close_browser()
