# requirements: install python packages

# importing all required packages, pandas, numpy, matplotlib, seaborn, requests,...
import pandas as pd
import numpy as np
import requests
import seaborn as sb
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup


# importing data file CSV format, rename csv

current_dir_path = os.path.dirname(os.path.realpath(__file__))
csv = pd.read_csv(os.path.join(current_dir_path, 'Courses.csv'))

# importing data using webscraping methode
home_page = requests.get(url='https://www.jobs.ie').text
soup = BeautifulSoup(home_page, 'html.parser')
all_categories = soup.find_all("section", {"class": "jobs-by-category accordion"})[0].find_all("a")

category_names = list()
category_counts = list()

for link in all_categories:
    category_text = link.next
    category_count = link.find_all("span")[0].next
    print(category_text + " " + category_count)
    category_names.append(category_text)
    category_counts.append(category_count)

output_dict = {"category_text": category_names, "category_count": category_counts}

scraped_df = pd.DataFrame.from_dict(output_dict)


# data discovery, column names? number of columns and rows, missing values, duplicate data, primary key?
pd.set_option('display.max_rows', 50)
# data type
print(type(csv))
# CSV headers
print(csv.keys())
# shape of csv
print(csv.shape)

# data cleaning


# data analysis
df = pd.DataFrame(csv, columns=['CourseID', 'skills'])
print(df)

# data visualisation

# analysis conclusion
