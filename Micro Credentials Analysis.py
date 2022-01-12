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
address = pd.read_csv(os.path.join(current_dir_path, 'Awarding_Body_Address.csv'), encoding='cp1252')

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

# adding new column 'Degree' in order to select sectors most likely to benefit from a credit-bearing course
degree = ['True', 'True', 'True', 'True', 'True', 'False', 'False', 'False', 'True', 'False', 'True', 'True', 'True',
          'False', 'True', 'False', 'True', 'False', 'True', 'True', 'True', 'True', 'True', 'True', 'False', 'False',
          'True', 'True', 'True', 'True', 'False', 'False', 'False', 'False', 'True', 'False', 'False', 'False',
          'True', 'True', 'False', 'False', 'False', 'True', 'False']
scraped_df['Degree'] = degree
vacancies_df = scraped_df.loc[scraped_df['Degree'] == 'True']

# In order to sort my category_count values, I needed to convert the data type to a float
vacancies_df["category_count"] = vacancies_df["category_count"].astype(float)

# creating a for loop to add the type of awarding body
for Type, row in courses.iterrows():
    if "Institute of Technology" in row['Awarding_Body']:
        courses.loc[Type, "Awarding_Body_Type"] = "IoT"
    else:
        courses.loc[Type, "Awarding_Body_Type"] = 'University'

courses.to_csv(r'courses_type.csv')
courses_type = pd.read_csv(os.path.join(current_dir_path, 'courses_type.csv'))

# removing duplicates from the courses dataframe
courses_df = pd.DataFrame(courses_type, columns=['ID', 'CourseID', 'Title', 'Awarding_Body', 'School', 'Credit',
                                                 'skills', 'Awarding_Body_Short', 'Course_Area', 'Course_Area_ID',
                                                 'Awarding_Body_Type'])
print("There are " + str(courses_df.duplicated(subset=['CourseID', 'Title']).sum()) + " duplicates in this dataframe.")

clean_courses_df = courses_df.drop_duplicates(subset=['CourseID', 'Title'], keep='first')
print("There are " + str(clean_courses_df.duplicated(subset=['CourseID', 'Title']).sum()) +
      " duplicates after the drop function was used.")

# merging the clean courses dataframe together with the Address dataframe
address_df = pd.DataFrame(address, columns=['Awarding_Body', 'Full_Address', 'County', 'Country'])
merged_df = pd.merge(clean_courses_df, address_df, on='Awarding_Body', how='left')


# grouping the course data by course area ID to provide me with a total count of courses per area
merged_group_course_area = merged_df['Course_Area'].value_counts()

# data visualisation

# visuals for Vacancy data
sns.barplot(x="category_count",
            y="category_text",
            data=vacancies_df,
            order=vacancies_df.sort_values('category_count', ascending=False).category_text)
plt.xlabel("Vacancies", size=15)
plt.ylabel("Sector's", size=15)
plt.title("Number of vacancies per sector", size=18)
plt.savefig("VacanciesPerSector.png", dpi=100)
plt.show()

# visuals for course data
palette = ['tab:purple', 'tab:pink']
sns.countplot(y="Awarding_Body_Short",
              data=merged_df,
              hue='Awarding_Body_Type',
              palette=palette,
              order=merged_df['Awarding_Body_Short'].value_counts().index)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel("# of Courses", size=15)
plt.ylabel("Awarding Body", size=15)
plt.title("NUMBER OF COURSES PER AWARDING BODY", size=18)
plt.savefig("CoursesPerAwardingBody.png", dpi=100)
plt.show()

sns.countplot(y="County",
              data=merged_df,
              hue='Awarding_Body_Type',
              palette=palette,
              order=merged_df['County'].value_counts().index)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel("# of Courses", size=15)
plt.ylabel("County", size=15)
plt.title("NUMBER OF COURSES PER COUNTY", size=18)
plt.savefig("CoursesPerCounty.png", dpi=100)
plt.show()


plt.subplot(111, polar=True)
plt.bar(x=0, height=10, width=np.pi/2, bottom=5)
vacancies_df = vacancies_df.sort_values(by=['category_count'])
plt.figure(figsize=(20, 10))
ax = plt.subplot(111, polar=True)
plt.axis('off')
upperLimit = 100
lowerLimit = 30
max = vacancies_df['category_count'].max()
slope = (max - lowerLimit) / max
heights = slope * vacancies_df.category_count + lowerLimit
width = 2*np.pi / len(vacancies_df.index)
indexes = list(range(1, len(vacancies_df.index)+1))
angles = [element * width for element in indexes]
plt.title("NUMBER OF VACANCIES PER SECTOR", size=15)
bars = ax.bar(
    x=angles,
    height=heights,
    width=width,
    bottom=lowerLimit,
    linewidth=2,
    edgecolor="white",
    color="#A020F0")
labelPadding = 4
for bar, angle, height, label in zip(bars,angles, heights, vacancies_df["category_text"]):
    rotation = np.rad2deg(angle)
    alignment = ""
    if angle >= np.pi/2 and angle < 3*np.pi/2:
        alignment = "right"
        rotation = rotation + 180
    else:
        alignment = "left"

    ax.text(
        x=angle,
        y=lowerLimit + bar.get_height() + labelPadding,
        s=label,
        ha=alignment,
        va='center',
        rotation=rotation,
        rotation_mode="anchor",
        fontsize=7)
plt.savefig("VacanciesPerSectorCircle.png", dpi=100)
plt.show()

sns.countplot(y="Course_Area",
              data=merged_df,
              order=merged_df['Course_Area'].value_counts().index)
plt.xlabel("# of Courses per Area", size=15)
plt.ylabel("Course Area", size=15)
plt.title("NUMBER OF COURSES PER AREA", size=18)
plt.savefig("CoursesPerArea.png", dpi=100)
plt.show()
