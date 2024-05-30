from classes.product_scraper import ProductScraper

class pcComponentes(ProductScraper):
    def __init__(self, URL):
      super().__init__("PC Componentes", URL):
