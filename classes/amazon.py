from time import sleep
import pandas as pd
from selenium import webdriver
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

        info = self.get_item_info()
    
    def get_item_info(self):
        product = self.driver.find_element(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
        product.click()

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