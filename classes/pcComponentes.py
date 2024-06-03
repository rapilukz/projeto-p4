
from classes.product_scraper import ProductScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class pcComponentesScrapper(ProductScraper):
    def __init__(product, self, URL):
      super().__init__(product, "PC Componentes", "https://www.pccomponentes.pt/")
