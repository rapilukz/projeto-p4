from classes.amazon import AmazonScraper

## initialize the AmazonScrapper class
amazon = AmazonScraper("https://www.amazon.com")


##Create an array of 20 items (computer parts) to be searched
items = ["motherboard", "processor", "ram", "gpu", "psu", "case", 
         "cooler", "monitor", "keyboard", "mouse", "headset", "microphone", 
         "webcam", "speakers", "printer", "scanner", "router", "switch", "access point", "cable"]


amazon.search_item("ryzen 5 3600x")