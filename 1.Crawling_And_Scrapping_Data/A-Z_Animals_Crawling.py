#!/usr/bin/env python
# coding: utf-8

# <font size="10">
#     <b>
#         A-Z Animals Site Crawling 
#         <b></font>

# In[ ]:


import requests
import bs4
from bs4 import BeautifulSoup  
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


# <font size="3">
#     <b>
#         Opening the downloaded site page 
#         <b></font>

# In[ ]:


url = "https://a-z-animals.com/animals/"
param = "./Data/"
siteName ="All Animals A-Z List - Animal Names _ AZ Animals.html"
soup = BeautifulSoup(open(param + siteName), "html.parser")


# <font size="3">
#     <b>
#         Getting each animal's page link and creating a links data frame 
#         <b></font>

# In[ ]:


linksOfAnimalPages=list()
listOfAnimals=soup.find_all("li",attrs={"class":"list-item col-md-4 col-sm-6"})

for row in listOfAnimals:
    a_tag=row.find_all("a")
    
    for a_rows in a_tag:
        linksOfAnimalPages.append(a_rows.get('href'))
        
animal_links_df = pd.DataFrame({"link_for_Animal_page":linksOfAnimalPages})
animal_links_df


# <font size="3">
#     <b>
#         Function to crawl each link and get the animal's data into lists and merge them into a data frame to return
#         <b></font>

# In[ ]:


def MakeDfByCrawlingAToZAnimalz(link):
    
    property_names = list()
    property_values = list()
    html = requests.get(link)
    soup = BeautifulSoup(html.content,"html.parser")
    div_tag = soup.find_all("div",attrs={"class":"row animal-facts-box"})

    if(len(div_tag) != 0):
        dt_tag = div_tag[0].find_all("dt"),div_tag[1].find_all("dt")
        dd_tag = div_tag[0].find_all("dd"),div_tag[1].find_all("dd")
        Conservation_tag = div_tag[0].find("li")
        li_tag = div_tag[0].find_all("li")

        property_names.append("Conservation Status")
        property_names.append("Locations")
        for index in range(0,2):
            for rows in dt_tag[index]:
                for row_a in rows:
                    property_names.append(row_a.get_text())

        if(len(li_tag)>2):
            locations = list()
            
            for index in range(1,len(li_tag)):
                locations.append(li_tag[index].get_text())
            locations_tuple = tuple(locations)
            property_values.append(li_tag[0].get_text())
            property_values.append(locations_tuple)
            for index in range(0,2):
                for rows in (dd_tag[index]):
                    property_values.append(rows.get_text())     
                    
        elif(len(li_tag) == 2):
            for index in range(0,2):            
                property_values.append(li_tag[index].get_text())  
            for index in range(0,2):
                for rows in (dd_tag[index]):
                    property_values.append(rows.get_text())

        if(len(li_tag)>=2):
            df_range = len(property_names)
            df = pd.DataFrame([range(df_range)])
            df.columns = property_names
            df.loc[0] = property_values
            return df
        
    df_empty = pd.DataFrame({'A' : []})
    return df_empty


# <font size="3">
#     <b>
#         Creating the full data frame by appending each animal df
#         <b></font>

# In[ ]:


df = MakeDfByCrawlingAToZAnimalz(animal_links_df.iloc[0][0])
for i in range(1,len(animal_links_df)):
    dfi = MakeDfByCrawlingAToZAnimalz(animal_links_df.iloc[i][0])
    if(not dfi.empty):
        df = df.append([dfi])
        
rows = len(df.axes[0])
df.index = range(rows)
#df.to_csv('C:/Users/noypr/Downloads/A-Z.csv')

