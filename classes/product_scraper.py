import pandas as pd
from selenium import webdriver

class ProductScraper():
    def __init__(self, product, storeName, URL):
        self.product = product
        self.storeName = storeName
        self.URL = URL
        self.driver = ""
        self.df = pd.DataFrame(columns=["name", "category", "price", "store", "ratings", "reviews", "reviews_nr"])

    def to_csv(self, fileName):
        self.df.to_csv(fileName, index = False)
        print(f"Data saved successfully to {fileName}")

    @staticmethod
    def combine_csvs(outputName, *inputFiles):
        combinedDf = pd.concat((pd.read_csv(f) for f in inputFiles), ignore_index=True)
        combinedDf.to_csv(outputName, index=False)
        print(f"All csv files combined into {outputName}")

    def goToNextPage(self):
        pass
    
    def print_details(self):
        print(f"The product is {self.product}")
        print(f"The store name is {self.storeName}")
        print(f"The URL is {self.URL}")
        # print(self.driver)

    def openPage(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)
        
    #Pseudo abstract method xdd
    def scrape(self):
        pass