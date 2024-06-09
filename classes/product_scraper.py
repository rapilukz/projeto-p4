import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ProductScraper():
    def __init__(self, storeName, driver):
        self.storeName = storeName
        self.driver = driver
        self.df = pd.DataFrame(columns=["name", "category", "price", "store", "ratings", "reviews", "reviews_nr"])

    def to_csv(self, fileName):
        self.df.to_csv(f"./data/{fileName}", index = False)
        print(f"Data saved successfully to {fileName}")

    def close_browser(self):
        self.driver.quit()
        print("Browser closed successfully")

    @staticmethod
    def combine_csvs(outputName, *inputFiles):
        combinedDf = pd.concat((pd.read_csv(f) for f in inputFiles), ignore_index=True)
        combinedDf.to_csv(outputName, index=False)
        print(f"All csv files combined into {outputName}")

    def goToNextPage(self):
        pass

    def got_back(self):
        self.driver.back()

    def add_item(self, name, category, price, store, ratings, reviews, reviews_nr):
        new_row = { "name": name, "category": category, "price": price, "store": store, "ratings": ratings, "reviews": reviews, "reviews_nr": reviews_nr }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)