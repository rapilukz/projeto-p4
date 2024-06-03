from classes.amazon import AmazonScraper
from classes.worten import WortenScrapper

worten = WortenScrapper("ryzen 5 3600")
amazon = AmazonScraper("ryzen 5 3600x")

worten.scrape()
amazon.scrape()

