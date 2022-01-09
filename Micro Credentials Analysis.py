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

# importing data using webscraping methode (requests and beautifulsoup to parse HTML data)
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

# converting lists into a dictionary to allow me to reference key values
output_dict = {"category_text": category_names, "category_count": category_counts}
scraped_df = pd.DataFrame.from_dict(output_dict)

# adding new column 'Degree' in order to sort sectors most likely to benefit from a credit-bearing course
degree = ['True', 'True', 'True', 'True', 'True', 'False', 'False', 'False', 'True', 'False', 'True', 'True', 'True',
          'False', 'True', 'False', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'False',
          'True', 'True', 'True', 'True', 'False', 'False', 'False', 'False', 'True', 'False', 'True', 'False',
          'True', 'True', 'False', 'False', 'False', 'True', 'False']
scraped_df['Degree'] = degree
vacancies_df = scraped_df.loc[scraped_df['Degree'] == 'True']

# In order to sort my category_count values, I needed to convert the data type to a float
vacancies_df["category_count"] = vacancies_df["category_count"].astype(float)

# data cleaning
courses_df = pd.DataFrame(courses, columns=['ID', 'CourseID', 'Title', 'Awarding_Body', 'School', 'Credit', 'skills'])
print("There are " + str(courses_df.duplicated(subset=['CourseID', 'Title']).sum()) + " duplicates in this dataframe.")

clean_courses_df = courses_df.drop_duplicates(subset=['CourseID', 'Title'], keep='first')
print("There are " + str(clean_courses_df.duplicated(subset=['CourseID', 'Title']).sum()) +
      " duplicates after the drop function was used.")
# data analysis


# group courses by school/department and group by awarding body
# percentage of vacancies per sector
# slice/subset vacancies based on degree requirements
# sector_subset = scraped_df.loc[scraped_df.loc['Degree']>0, :]
# print(sector_subset)

# creating a for loop
for Type, row in courses.iterrows():
    if "Institute of Technology" in row['Awarding_Body']:
        courses.loc[Type, "Awarding Body Type"] = "IoT"
    else:
        courses.loc[Type, "Awarding Body Type"] = 'University'

courses.to_csv(r'courses_type.csv')

# data visualisation

# visuals for Vacancy data
sns.barplot(x="category_count",
            y="category_text",
            data=vacancies_df,
            order=vacancies_df.sort_values('category_count',ascending = False).category_text)
plt.xlabel("Vacancies", size=15)
plt.ylabel("Sector's", size=15)
plt.title("Number of vacancies per sector", size=18)
plt.savefig("VacanciesPerSector.png", dpi=100)
plt.show()

# visuals for course data
sns.countplot(y="Awarding_Body",
              data=clean_courses_df)
plt.xlabel("# of Courses", size=15)
plt.ylabel("Awarding Body", size=15)
plt.title("Number of courses per awarding body", size=18)
plt.savefig("CoursesPerAwardingBody.png", dpi=100)
plt.show()

sns.displot(data=clean_courses_df, y="Awarding_Body")
plt.show()

# analysis conclusion
