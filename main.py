from classes.amazon import AmazonScraper
from classes.worten import WortenScrapper

## Example of how to use the AmazonScraper class
# amazon = AmazonScraper("ryzen 5 3600x")
# try:
#     amazon.scrape()
# finally:
#     amazon.close_browser()

## Example of how to use the WortenScrapper class
worten = WortenScrapper("ryzen 5 3600")
worten.scrape()

