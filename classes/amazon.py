from time import sleep
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazoncaptcha import AmazonCaptcha

class AmazonScraper(ProductScraper):
    def __init__(self, driver):
        super().__init__("Amazon", driver)
        
    def scrape_item(self, URL):
        self.solve_captcha()
        self.driver.get(URL)
        sleep(2)
        info = self.get_item_info()
        self.add_item(info["name"], "Computer Parts", info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])

    def get_item_info(self):
        product_name = self.driver.find_element(By.ID, "productTitle").text
        print('Scraping: ', product_name)
        price = self.get_price()
        rating = self.driver.find_element(By.ID, "acrPopover").get_attribute("title")
        store = self.storeName 
        try:
            reviews_number = self.driver.find_element(By.ID, "acrCustomerReviewText").text.split(" ")[0]
            reviews = self.get_reviews()
        except:
            reviews_number = "N/A"
            reviews = "N/A"        

        product_info = {
            "name": product_name,
            "price": price,
            "store": store,
            "ratings": rating,
            "reviews_nr": reviews_number,
            "reviews": reviews
        }

        return product_info
    
    def get_reviews(self):
        reviews = self.driver.find_elements(By.CSS_SELECTOR, '[data-hook="review-collapsed"] span')
        reviews_list = []
        for review in reviews:
            reviews_list.append(review.text)
            
        return reviews_list
    
    def get_price(self):
        try:
            whole_price = self.driver.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
            fraction_price = self.driver.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        except:
            price = "N/A"

        return price
        
    def solve_captcha(self):
        try:
            self.driver.get("https://www.amazon.com/errors/validateCaptcha")
            link = self.driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute("src")
            captcha = AmazonCaptcha.fromlink(link)
            captcha_value = AmazonCaptcha.solve(captcha)
            self.driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
            button = self.driver.find_element(By.CLASS_NAME, "a-button-text")
            button.click()
        except:
            print("No captcha found")

        
if __name__ == "__main__":
    scraper = AmazonScraper("rato gamer")
