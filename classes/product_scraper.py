import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ProductScraper():
    def __init__(self, storeName, URL):
        self.storeName = storeName
        self.URL = URL
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

    def got_back(self):
        self.driver.back()
    
    def print_details(self):
        print(f"The store name is {self.storeName}")
        print(f"The URL is {self.URL}")
        # print(self.driver)

    def openPage(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.URL)
        
    #Pseudo abstract method xdd
    def scrape(self):
        pass