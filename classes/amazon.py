from time import sleep
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazoncaptcha import AmazonCaptcha

class AmazonScraper(ProductScraper):
    def __init__(self, product):
        super().__init__(product, "Amazon", "https://www.amazon.com")

    def scrape(self):
        self.open_browser()
        self.search_item()
        self.scrape_items()
        self.to_csv("amazon.csv")
        self.driver.quit()

    def open_browser(self):
        self.openPage()
        self.solve_captcha()

    def search_item(self):
        search_bar = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search_bar.click()
        search_bar.send_keys(self.product)
        sleep(1)
        search_bar.send_keys(Keys.RETURN)
        
    def scrape_items(self):
        links = self.get_links()
        print(f"Found {len(links)} items")
        for link in links:
            self.driver.get(link)
            info = self.get_item_info()
            self.add_item(info["name"], "Computer Parts", info["price"], info["store"], info["ratings"], info["reviews"], info["reviews_nr"])
            sleep(1)

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

    def get_links(self):
        links = []
        for i in range(2):
            current_page = self.driver.current_url
            product_listing = self.driver.find_elements(By.CSS_SELECTOR,('.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right'))
            print(f"Scraping page {i+1}")
            for product in product_listing:
                try: 
                    product_link = product.find_element(By.CSS_SELECTOR, 'a.a-link-normal')
                    if(current_page in product_link.get_attribute("href")):
                        continue

                    links.append(product_link.get_attribute("href"))
                except:
                    pass
            next_button = self.driver.find_element(By.XPATH, "//a[text()='Next']")
            next_button.click()
            sleep(2)

        return links[:20]
    
    def get_price(self):
        try:
            whole_price = self.driver.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
            fraction_price = self.driver.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        except:
            price = "N/A"

        return price
        
    def solve_captcha(self):
        self.driver.get("https://www.amazon.com/errors/validateCaptcha")
        link = self.driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute("src")
        captcha = AmazonCaptcha.fromlink(link)
        captcha_value = AmazonCaptcha.solve(captcha)
        self.driver.find_element(By.ID, "captchacharacters").send_keys(captcha_value)
        button = self.driver.find_element(By.CLASS_NAME, "a-button-text")
        button.click()

        
if __name__ == "__main__":
    scraper = AmazonScraper("rato gamer")
