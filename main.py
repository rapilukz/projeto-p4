from classes.amazon import AmazonScraper
from classes.globaldata import GlobalDataScraper

## Example of how to use the AmazonScraper class
# amazon = AmazonScraper("ryzen 5 3600x")
# try:
#     amazon.scrape()
# finally:
#     amazon.close_browser()

## Example of how to use the GlobalDataScraper class
globaldata = GlobalDataScraper("ryzen 5")
try:
    globaldata.scrape()
finally:
    globaldata.driver.quit()
