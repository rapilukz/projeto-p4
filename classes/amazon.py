from time import sleep
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from amazoncaptcha import AmazonCaptcha

class AmazonScraper(ProductScraper):
    def __init__(self, URL):
        super().__init__("Amazon", URL)

    def search_item(self, item):
        self.openPage()
        self.solve_captcha()
        search_bar = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search_bar.click()
        search_bar.send_keys(item)
        sleep(1)
        search_bar.send_keys(Keys.RETURN)
        
        product = self.driver.find_element(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
        product.click()
        sleep(1)
        info = self.get_item_info()
        self.add_item(info["name"], "Computer Parts", info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])
    
    def get_item_info(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))
        product_name = self.driver.find_element(By.ID, "productTitle").text
        price_whole = self.driver.find_element(By.CSS_SELECTOR,'.a-section.a-spacing-none.aok-align-center.aok-relative .a-price-whole').text
        price_fraction = self.driver.find_element(By.CSS_SELECTOR,'.a-section.a-spacing-none.aok-align-center.aok-relative .a-price-fraction').text
        rating = self.driver.find_element(By.ID, "acrPopover").get_attribute("title")
        store = self.storeName 
        reviews_number = self.driver.find_element(By.ID, "acrCustomerReviewText").text.split(" ")[0]
        reviews = self.get_reviews()

        product_info = {
            "name": product_name,
            "price": f"{price_whole}.{price_fraction}",
            "store": store,
            "ratings": rating,
            "reviews_nr": reviews_number,
            "reviews": reviews
        }
        return product_info

    def get_reviews(self):
        reviews_button = self.driver.find_element(By.XPATH, '//*[@id="cr-pagination-footer-0"]/a')
        reviews_button.click()
        
        ## Get all elements with data-hook="review-body"
        sleep(1)
        reviews = self.driver.find_elements(By.CSS_SELECTOR, '[data-hook="review"]')
        ## review list should be a dictionary with the review text and the user name
        reviews_list = []
        for review in reviews:
            user = review.find_element(By.CSS_SELECTOR, '.a-profile-name').text
            text = review.find_element(By.CSS_SELECTOR, '[data-hook="review-body"]').text
            reviews_list.append({"review": text, "user": user})

        return reviews_list
        

    def solve_captcha(self):
        self.driver.get("https://www.amazon.com/errors/validateCaptcha")
        link = self.driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute("src")
        captcha = AmazonCaptcha.fromlink(link)
        captcha_value = AmazonCaptcha.solve(captcha)
        self.driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
        button = self.driver.find_element(By.CLASS_NAME, "a-button-text")
        button.click()
        
if __name__ == "__main__":
    URL = "https://www.amazon.com"
    scraper = AmazonScraper(URL)