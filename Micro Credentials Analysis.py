# requirements: install python packages

# importing all required packages, pandas, numpy, matplotlib, seaborn, requests,...
import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup



# importing data file CSV format, rename csv

current_dir_path = os.path.dirname(os.path.realpath(__file__))
courses = pd.read_csv(os.path.join(current_dir_path, 'Courses.csv'), encoding='cp1252')

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
scraped_df["category_count"] = scraped_df["category_count"].astype(float)
degree = [True, True, True, True, True, False, False, False, True, False, True, True, True, False, True,
          False, True, False, True, True, True, True, True, True, False, False, True, True, True, True,
          False, False, False, False, True, False, True, False, True, True, False, False, False, True, False]
scraped_df['Degree'] = degree

scraped_df_sorted = scraped_df.sort_values('category_count', ascending=False, inplace=True)
# data cleaning


# data analysis
courses_df = pd.DataFrame(courses, columns=['CourseID', 'skills'])


# group courses by school/department and group by awarding body
# percentage of vacancies per sector
# slice/subset vacancies based on degree requirements
# sector_subset = scraped_df.loc[scraped_df.loc['Degree']>0, :]
# print(sector_subset)

# creating a for loop
for type, row in courses.iterrows():
    if "Institute of Technology" in row ['Awarding Body']:
        courses.loc[type, "Awarding Body Type"] = "IoT"
    else:
        courses.loc[type,"Awarding Body Type"] ='University'

courses.to_csv(r'courses_type.csv')
courses.head()
# data visualisation

sns.barplot(x='category_count',
            y='category_text',

            data=scraped_df)
plt.show()
# analysis conclusion


