import pandas as pd
import numpy as np
import re

def clean(df: pd.DataFrame) -> pd.DataFrame:
  """Takes in the Graduate Employment data as a pandas dataframe,
  and returns the cleaned version for plotting

  Args:
      df (pd.DataFrame): Graduate Employment survey dataframe

  Returns:
      pd.DataFrame: Cleaned data for visualisation
  """
  # Remove the rows with na (str)
  df = df[df['employment_rate_overall'] != 'na']

  # Specify the datatypes of columns
  cols_to_change = [col for col in df.columns if col not in 
                    ['year', 'university', 'school', 'degree']]
  df = df.astype(dtype={
    col: 'float64' for col in cols_to_change
  })

  # Change the datatype of year column
  df['year'] = pd.to_datetime(df['year'], format="%Y")

  # Cleaning the school column
  # Remove any details from brackets
  df['school'] = df['school'].str.replace(r'\(.*?\)', '', regex=True)

  # Remove any special characters from the back
  df['school'] = df['school'].str.replace(r'[\*|\\|\#]+', '', regex=True)

  # Remove the white space after dash
  df['school'] = df['school'].str.replace(r'-\s', '-', regex=True)

  # Remove leading and trailing whitespace
  df['school'] = df['school'].str.strip()

  # Cleaning the degree column
  # Remove special characters from the back
  df['degree'] = df['degree'].str.replace(r'[\*|\\|\#|\^|\.]+', '', regex=True)

  # Extract out if they were honours or cum laude programs
  df['advanced'] = np.where(df['degree'].str.contains(r'Honours|\(Hons\)|Cum\s+Laude'), 1, 0)
  remove_advanced = r'\s+with\s+Honours|\(Hons\)|\(?Cum\sLaude\sand\sabove\)?'
  df['degree'] = df['degree'].str.replace(remove_advanced, '', regex=True)

  # Remove the length of degree
  df['degree'] = df['degree'].str.replace(r'\([^()]*\d[^()]*\)', '', regex=True)

  # Remove non-degree related terms
  df['degree'] = df['degree'].str.replace(r'\(LLB\)|\(MBBS\)|\(Land\)', '', regex=True)

  # Some degree types are hidden between brackets so we extract them
  temp = df['degree'].str.extract(r'\(([^)]+)\)')
  df.loc[temp[~temp[0].isna()].index, 'degree'] = temp[~temp[0].isna()][0]

  # Some degrees are also only expressed after the word "in"
  temp = df['degree'].str.extract(r'\bin\b\s+(.*?)$')
  df.loc[temp[~temp[0].isna()].index, 'degree'] = temp[~temp[0].isna()][0]

  # Remove term "Bachelor of"
  df['degree'] = df['degree'].str.replace(r'Bachelor\sof\s?', '', regex=True, case=False)

  # Replace some special characters with their word equivalents
  df['degree'] = df['degree'].str.replace('&', 'and')
  df['degree'] = df['degree'].str.replace('/', ' and ')
  df['degree'] = df['degree'].str.replace('with', '')
  df['degree'] = df['degree'].str.replace(r'\s+', ' ', regex=True)
  df['degree'] = df['degree'].str.replace(r's$', '', regex=True)

  # Remove leading and trailing whitespace
  df['degree'] = df['degree'].str.strip()

  # Reset the index
  df = df.reset_index(drop=True)

  return df