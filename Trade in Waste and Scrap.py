# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 12:06:20 2022

@author: Jennifer
"""
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv(r'C:/Users/jenni/OneDrive/Documents/TTU School/Data Science Degree/' \
                 'Random Data Sets and Tableau/Trade in waste and scrap unclean combined.csv')

# Display the first few rows to inspect the data structure
df.head()

# Rename the first three columns for clarity
df.rename(columns={ df.columns[0]: "OECD Country" }, inplace = True)
df.rename(columns={ df.columns[2]: "HSCode" }, inplace = True)
df.rename(columns={ df.columns[1]: "Country" }, inplace = True)

# Display the updated DataFrame to verify column renaming
df.head()

# Define columns to forward fill vertically to handle missing data
cols_to_fill = ['OECD Country', 'Country']  # Combine both 'cols' and 'cols2' into one list

# Forward fill missing values in 'OECD Country' and 'Country' columns down the rows
df[cols_to_fill] = df[cols_to_fill].ffill()

# Forward fill missing values across all columns to handle missing data in rows
df = df.ffill(axis=1)

# Drop the 'OECD Country' column after filling, as it's no longer needed
df.drop(['OECD Country'], axis=1, inplace=True)

# Rename the columns
df.rename(columns = {'Unnamed: 3':'2003 Exports','Unnamed: 4':'2003 Imports', 
   'Unnamed: 5':'2004 Exports', 'Unnamed: 6':'2004 Imports',
   'Unnamed: 7':'2005 Exports','Unnamed: 8':'2005 Imports',
   'Unnamed: 9':'2006 Exports','Unnamed: 10':'2006 Imports',
   'Unnamed: 11':'2007 Exports','Unnamed: 12':'2007 Imports', 
   'Unnamed: 13':'2008 Exports','Unnamed: 14':'2008 Imports', 
   'Unnamed: 15':'2009 Exports','Unnamed: 16':'2009 Imports',
   'Unnamed: 17':'2010 Exports','Unnamed: 18':'2010 Imports',
   'Unnamed: 19':'2011 Exports','Unnamed: 20':'2011 Imports',
   'Unnamed: 21':'2012 Exports','Unnamed: 22':'2012 Imports',
   'Unnamed: 23':'2013 Exports','Unnamed: 24':'2013 Imports',
   'Unnamed: 25':'2014 Exports','Unnamed: 26':'2014 Imports',
   'Unnamed: 27':'2015 Exports','Unnamed: 28':'2015 Imports',
   'Unnamed: 29':'2016 Exports','Unnamed: 30':'2016 Imports'}, inplace = True)

# Display the updated DataFrame to verify column renaming
df.head()

# Drop the first two rows that contain duplicate information
df.drop([0,1], axis=0, inplace=True)

# Get a list of unique countries
df.Country.unique()

# Remove leading and trailing spaces from the 'Country' column to standardize country names
df['Country'] = df['Country'].str.strip()

# Standardize country names in the 'Country' column
df= df.replace('Viet Nam',"Vietnam")
df= df.replace('Türkiye', 'Turkey')
df= df.replace('Korea','South Korea')
df= df.replace("Côte d'Ivoire", "Cote d'Ivoire")

# Print unique countries for verification
df.Country.unique()

# Print unique HSCode
df.HSCode.unique()

# Remove leading and trailing spaces from the 'HSCode' column to standardize values
df['HSCode'] = df['HSCode'].str.strip()

# Define a list of non-numeric or invalid HSCode values to remove from the DataFrame
values_to_remove = ['Guyana', 'Chad', 'Andorra', 'Guam', 'Saint Pierre and Miquelon', 'Tonga', 'Zimbabwe']

# Create a Boolean mask for the rows to keep
mask = ~df['HSCode'].isin(values_to_remove)

# Select all rows except the ones that contain any of the specified values
df = df[mask]

# Print unique HSCode for verification
df.HSCode.unique()

# Filter DataFrame to include only relevant HS Codes (between 520000 and 529999)
# This keeps only yarn, cotton, and man-made fiber products
df=df.loc[(df['HSCode'] > 519999) & (df['HSCode'] < 530000)]

# Display the current data types of all columns
df.dtypes

# Convert 'HSCode' from object to string and then to integer for numeric operations
df['HSCode'] = df['HSCode'].astype('string').astype('int32')

# Convert 'Country' from object to string to ensure consistent text formatting
df['Country'] = df['Country'].astype('string')

#Replace .. with # Replace '..' with '0' in the DataFrame to prepare for numeric data type conversion
df= df.replace('..',"0")

# Define the range of years to change the column data types
years = range(2003, 2017)

# Create a dictionary to change data types to string
dtype_change = {f'{year} {trade}': 'string' for year in years for trade in ['Imports', 'Exports']}

# Change data types from object to string for all specified columns
df = df.astype(dtype_change)

# Remove all commas from the DataFrame to prepare for numeric conversion
df = df.replace(',','', regex=True)

# Define the range of years to consider for data type conversion
years = range(2003, 2017)

# Create a dictionary to specify columns to convert to float and generate column names
float_columns = {f'{year} {trade}': 'float' for year in years for trade in ['Imports', 'Exports']}

# Change the data type of the specified columns to float
df = df.astype(float_columns)
    
# Display the current data types of all columns to confirm the changes were successful
df.dtypes 

# Reset the DataFrame index after filtering and sorting
df = df.reset_index(drop=True)

# Group data by 'Country' and sum the numerical columns to aggregate trade data
df = df.groupby('Country', as_index=False).sum()

# Drop the duplicate 'HSCode' column as it is no longer needed after aggregation
df.drop(['HSCode'], axis=1, inplace=True)

# Reshape the DataFrame to convert year-specific columns into rows
df2=df.melt(id_vars=["Country"], 
        var_name="Year", 
        value_name="WeightInTons")

# Split the 'Year' column into 'Year' and 'Type of Shipment' based on space delimiter
df2[['Year', 'Type of Shipment']] = df2.Year.str.split (" ", expand = True)

# Assign negative values to 'WeightInTons' for 'Exports' to differentiate from 'Imports'
df2.loc[df2['Type of Shipment'] == 'Exports', 'WeightInTons'] *= -1

# Export the cleaned DataFrame to a CSV file
df2.to_csv('Trade_in_waste_and_scrap_clean.csv')

