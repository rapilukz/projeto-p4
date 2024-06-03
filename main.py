from classes.amazon import AmazonScraper
from classes.worten import WortenScrapper

amazon = AmazonScraper("ryzen 5 3600x")
worten = WortenScrapper("ryzen 5 3600")

amazon.scrape()
worten.scrape()

