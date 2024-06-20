import pandas as pd
import glob
import os

def createDataframe():
    path = './data' # use your path

    all_files = glob.glob(os.path.join(path, "*.csv"))
    print(all_files)

    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    return df