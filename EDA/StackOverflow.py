# -*- coding: utf-8 -*-
"""EDA on Stack Overflow Developer Survey .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qk36Nzs8QYgpOSijM9rW8QnQi-hUgzly

# Import, Downloading and checking the given dataset
"""

# Downloading files from stack overflow dataset using opendatasets library

!pip install opendatasets
import opendatasets as od

od.download('stackoverflow-developer-survey-2020')

# verifying the dowloaded content

import os
os.listdir('stackoverflow-developer-survey-2020')

# storing the specific datasets using pandas

import pandas as pd
survey_raw_df=pd.read_csv('stackoverflow-developer-survey-2020/survey_results_public.csv')
survey_raw_df

# viewing the list of columns

survey_raw_df.columns

# Checking the schema of the above columns by using the schema csv file

schema_raw=pd.read_csv('stackoverflow-developer-survey-2020/survey_results_schema.csv',index_col='Column').QuestionText
schema_raw

"""# Data preparation and Cleaning"""

# Selecting subset of relevant columns required for our purpose

selected_columns = [
    # Demographics
    'Country',
    'Age',
    'Gender',
    'EdLevel',
    'UndergradMajor',
    # Programming experience
    'Hobbyist',
    'Age1stCode',
    'YearsCode',
    'YearsCodePro',
    'LanguageWorkedWith',
    'LanguageDesireNextYear',
    'NEWLearn',
    'NEWStuck',
    # Employment
    'Employment',
    'DevType',
    'WorkWeekHrs',
    'JobSat',
    'JobFactors',
    'NEWOvertime',
    'NEWEdImpt'
]
len(selected_columns)

# extracting a copy of these columns in a new dataframe survey_df

survey_df=survey_raw_df[selected_columns].copy()
schema=schema_raw[selected_columns]

# Some basic information of the extracted df

survey_df.shape

survey_df.info()

# Only two columns have numeric values , so lets convert some other columns relevant to numeric type

survey_df['Age1stCode'] = pd.to_numeric(survey_df.Age1stCode, errors='coerce')
survey_df['YearsCode'] = pd.to_numeric(survey_df.YearsCode, errors='coerce')
survey_df['YearsCodePro'] = pd.to_numeric(survey_df.YearsCodePro, errors='coerce')

# Some basic statistics about numeric columns

survey_df.describe()

# There seems to be a problem with the age column, as the minimum value is 1 and the maximum is 279. This is a common issue with surveys: responses may contain invalid values due to accidental or intentional errors while responding. A simple fix would be to ignore the rows where the age is higher than 100 years or lower than 10 years as invalid survey responses.

survey_df.drop(survey_df[survey_df.Age < 10].index, inplace=True)
survey_df.drop(survey_df[survey_df.Age > 100].index, inplace=True)

# The same holds for WorkWeekHrs. Let's ignore entries where the value for the column is higher than 140 hours. (~20 hours per day).

survey_df.drop(survey_df[survey_df.WorkWeekHrs > 140].index, inplace=True)

#The gender column also allows for picking multiple options. We'll remove values containing more than one option to simplify our analysis.

survey_df['Gender'].value_counts()

import numpy as np
survey_df.where(~(survey_df.Gender.str.contains(';',na=False)),np.nan,inplace=True)

# Data cleaned up for further analysis. Lets take a look at our sample data

survey_df.sample(10)

"""# Explroratory Analysis and Visualisation"""

# Importing and template making for matplotlib and seaborn

# Commented out IPython magic to ensure Python compatibility.
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline

sns.set_style('darkgrid')
matplotlib.rcParams['font.size']=14
matplotlib.rcParams['figure.figsize']=(9,5)
matplotlib.rcParams['figure.facecolor']='#00000000'

# Analysis on Country

# Let's look at the number of countries from which there are responses in the survey and plot the ten countries with the highest number of responses

schema.Country

survey_df.Country.nunique()

top_countries=survey_df.Country.value_counts().head(10)
top_countries

# Visualise this using a bar chart

plt.figure(figsize=(12,6))
plt.xticks(rotation=75)
plt.title(schema.Country)
sns.barplot(x=top_countries.index,y=top_countries)

# Analysis on Age

# The distribution of respondents' age is another crucial factor to look at. We can use a histogram to visualize it.

plt.figure(figsize=(12,6))
plt.title(schema.Age)
plt.xlabel('Age')
plt.ylabel('Number of respondents')
plt.hist(survey_df.Age, bins=np.arange(10,80,5),color='purple');

# Analysis on Gender

# Let's look at the distribution of responses for the Gender. It's a well-known fact that women and non-binary genders are underrepresented in the programming community, so we might expect to see a skewed distribution here.

schema.Gender

gender_counts=survey_df.Gender.value_counts()
gender_counts

# Using the pie chart to visualise the above

plt.figure(figsize=(12,6))
plt.title(schema.Gender)
plt.pie(gender_counts,labels=gender_counts.index,autopct='%1.1f%%',startangle=180);

# Education Level analysis

# Formal education in computer science is often considered an essential requirement for becoming a programmer. However, there are many free resources & tutorials available online to learn programming. Let's compare the education levels of respondents to gain some insight into this. We'll use a horizontal bar plot here.

sns.countplot(y=survey_df.EdLevel)
plt.xticks(rotation=75);
plt.title(schema['EdLevel'])
plt.ylabel(None);

# Q: What are the most popular programming languages in 2020?

survey_df.LanguageWorkedWith

def split_multicolumn(col_series):
    result_df = col_series.to_frame()
    options = []
    # Iterate over the column
    for idx, value  in col_series[col_series.notnull()].iteritems():
        # Break each value into list of options
        for option in value.split(';'):
            # Add the option as a column to result
            if not option in result_df.columns:
                options.append(option)
                result_df[option] = False
            # Mark the value in the option column as True
            result_df.at[idx, option] = True
    return result_df[options]

languages_worked_df=split_multicolumn(survey_df.LanguageWorkedWith)
languages_worked_df

languages_worked_percentages=languages_worked_df.mean().sort_values(ascending=False)*100
languages_worked_percentages

plt.figure(figsize=(12,12))
sns.barplot(x=languages_worked_percentages,y=languages_worked_percentages.index)
plt.title('Languages used in the past year')
plt.xlabel('count')