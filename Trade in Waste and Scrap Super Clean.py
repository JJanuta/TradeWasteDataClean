# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 12:06:20 2022

@author: Jennifer
"""

import pandas as pd

#Read in data
df=pd.read_csv(r'C:\\Users\\Jennifer\\Desktop\\Trade in waste and scrap unclean combined.csv')

#rename columns
df.rename(columns={ df.columns[0]: "OECD Country" }, inplace = True)
df.rename(columns={ df.columns[2]: "HSCode" }, inplace = True)
df.rename(columns={ df.columns[1]: "Country" }, inplace = True)

#Create variables for fill
cols = ['OECD Country']
cols2= ['Country']

#Forward Fill OECD Country and Country to fill in blank data
df.loc[:,cols] = df.loc[:,cols].ffill()
df.loc[:,cols2] = df.loc[:,cols2].ffill()
df.loc[:,cols2] = df.loc[:,cols2].ffill()
df.loc[:,cols] = df.loc[:,cols].ffill(axis=1)
df = df.ffill(axis=1, limit=1)

#Drop un
df.drop(['OECD Country'], axis=1, inplace=True)

#Rename Date Columns
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

#drop unnecessary rows
df.drop([0,1,1236,1237], axis=0, inplace=True)

#get Country List
df.Country.unique()

#remove space in front of countries
df['Country'] = df['Country'].str.strip()

#get HSCode List
df.HSCode.unique()

#Drop rows where HSCode is not provided. Data is not relevant
df.drop([342,490,623,640,1008,1130],axis=0,inplace=True)

#Check datatypes
df.dtypes

#Change HSCode data type to from object to string and then int
df['HSCode'] = df['HSCode'].astype('string').astype('int32')

#Change Country data type from object to string
df['Country'] = df['Country'].astype('string')

#Replace .. with 0 to prepare for datatype change
df= df.replace('..',"0")

#change data type from object to string before changing to float
df = df.astype({'2003 Imports': "string","2003 Exports": "string", 
                '2004 Imports': "string","2004 Exports": "string", 
                '2005 Imports': "string","2005 Exports": "string", 
                '2006 Imports': "string","2006 Exports": "string",
                '2007 Imports': "string","2007 Exports": "string", 
                '2008 Imports': "string","2008 Exports": "string", 
                '2009 Imports': "string","2009 Exports": "string", 
                '2010 Exports': "string","2010 Imports": "string",
                "2011 Exports": "string",'2011 Imports': "string",
                "2012 Exports": "string",'2012 Imports': "string",
                "2013 Exports": "string",'2013 Imports': "string",
                "2014 Exports": "string",'2014 Imports': "string",
                "2015 Exports": "string",'2015 Imports': "string",
                "2016 Exports": "string",'2016 Imports': "string"})

#Removed all commas before converting to float
df = df.replace(',','', regex=True)

#Change to float
df = df.astype({'2003 Imports': "float","2003 Exports": "float", 
                '2004 Imports': "float","2004 Exports": "float", 
                '2005 Imports': "float","2005 Exports": "float", 
                '2006 Imports': "float","2006 Exports": "float",
                '2007 Imports': "float","2007 Exports": "float", 
                '2008 Imports': "float","2008 Exports": "float", 
                '2009 Imports': "float","2009 Exports": "float", 
                '2010 Exports': "float","2010 Imports": "float",
                "2011 Exports": "float",'2011 Imports': "float",
                "2012 Exports": "float",'2012 Imports': "float",
                "2013 Exports": "float",'2013 Imports': "float",
                "2014 Exports": "float",'2014 Imports': "float",
                "2015 Exports": "float",'2015 Imports': "float",
                "2016 Exports": "float",'2016 Imports': "float"})  
    
#Check datatypes to confirm change
df.dtypes 
    
#Remove HS Codes not relevant
df=df.loc[(df['HSCode'] > 519999) & (df['HSCode'] < 530000)]

#Rename Countries
df= df.replace('Viet Nam',"Vietnam")
df= df.replace('Türkiye', 'Turkey')
df= df.replace('Korea','South Korea')

#Reset index
df = df.reset_index(drop=True)

#Add HSCodes together
df = df.groupby('Country', as_index=False).sum()

#Drop HSCode, no longer needed
df.drop(['HSCode'], axis=1, inplace=True)

#Make Years a column 
df2=df.melt(id_vars=["Country"], 
        var_name="Year", 
        value_name="WeightInTons")

#Separate the Year column into two while splitting the text
df2[['Year', 'Type of Shipment']] = df2.Year.str.split (" ", expand = True)

#Assign negative values to number of the export type
df2.loc[df2['Type of Shipment'] == 'Exports', 'WeightInTons'] *= -1

#Export to CSV
df2.to_csv('Trade_in_waste_and_scrap_clean.csv')

