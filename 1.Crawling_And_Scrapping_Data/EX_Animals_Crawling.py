#!/usr/bin/env python
# coding: utf-8

# <font size="10">
#     <b>
#         Wikipedia Extinct Species Crawling 
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


url_EX_Holocene = "https://en.wikipedia.org/wiki/Timeline_of_extinctions_in_the_Holocene"
param = "./Data/"
site_EX = "Timeline of extinctions in the Holocene - Wikipedia.html"
soup = BeautifulSoup(open(param + site_EX, encoding="utf8"), "html.parser")
table_tag = soup.find_all("table",attrs={"class":"wikitable sortable jquery-tablesorter"})


# <font size="3">
#     <b>
#         Function to crawl each link and get the main animal page data
#         <b></font>

# In[ ]:


def MakeDfByCrawlIngWiki(link):
    
    temp=0
    property_names = list()
    property_values = list()
    html = requests.get(link)
    soup = BeautifulSoup(html.content,"html.parser")

    tbl=soup.find("table",attrs={"class":"infobox biota"})
    if tbl != None:
        for row in tbl("tr"):
            for link in row.find_all('td'):
                if(len(row.find_all('td'))==2):
                    if temp==0:
                        property_names.append(link.get_text().strip())
                        temp=1
                    else:
                        if link.get_text().strip() == "Plantae":
                            df_range = len(property_names)
                            Extinct_Animals_df = pd.DataFrame([range(df_range)])
                            Extinct_Animals_df.columns = property_names
                            return Extinct_Animals_df
                        property_values.append(link.get_text().strip())
                        temp=0

        df_range = len(property_names)
        Extinct_Animals_df = pd.DataFrame([range(df_range)])
        Extinct_Animals_df.columns = property_names
        Extinct_Animals_df.iloc[0] = property_values

        return Extinct_Animals_df
    else:
        df_range = len(property_names)
        Extinct_Animals_df = pd.DataFrame([range(df_range)])
        Extinct_Animals_df.columns = property_names
        
        return Extinct_Animals_df


# <font size="3">
#     <b>
#         Crawling the tables of the main page and entering each animal link for further data scrapping
#         <b></font>

# In[ ]:


#Extracting main page data and calling link_crawl#

linksOfAnimalPages=list()
df_end = pd.DataFrame([range(1)])
isStart = True
count = 0

for table in table_tag:
    #table = soup.find("table")
    thread_tag = table.find("thead")
    body_tag = table.find("tbody")
    property_rows = thread_tag.find_all("th")
    animal_rows = body_tag.find_all("tr")
    listOfProperties=list()
    listOfAnimalData=list()
    
    for row in property_rows:
            listOfProperties.append(row.get_text(strip=True))
    df_range = len(listOfProperties)
    df = pd.DataFrame([range(df_range)])
    df.columns = listOfProperties
    dfOfAnimal = df

    for animal_row in body_tag: #foreach tr in current table
        animalDataCount = 0
        listOfAnimalData=list()
        a_tag = animal_row.find("a")
        
        if a_tag != -1:
            linksOfAnimalPages.append(a_tag["href"])
            listOfAnimalData.append(a_tag.get_text(strip=True))
            
            df_func = MakeDfByCrawlIngWiki(a_tag["href"])
            
        i_tag = animal_row.find("i")
        if i_tag != -1:
            listOfAnimalData.append(i_tag.get_text(strip=True))
        for td_row in animal_row:
            animalDataCount += 1
            if(animalDataCount == 6):
                listOfAnimalData.append(td_row.get_text(strip=True))
            if(animalDataCount == 8):
                b_tag = animal_row.find("b")
                if b_tag != -1 and b_tag != None:
                    listOfAnimalData.append(b_tag.get_text(strip=True))
            if(animalDataCount == 10):
                if(len(listOfProperties) != 6):
                    listOfAnimalData.append(td_row.get_text(strip=True))
                    dfOfAnimal.loc[0] = listOfAnimalData
                    df = df.append(dfOfAnimal)
                else:
                    listOfAnimalData.append(td_row.get_text(strip=True))
            if(animalDataCount == 12):
                listOfAnimalData.append(td_row.get_text(strip=True))
                if(dfOfAnimal.shape[1] == len(listOfAnimalData)):
                    dfOfAnimal.loc[0] = listOfAnimalData
                    df = df.append([dfOfAnimal])
        
    df = pd.concat([df,df_func], axis=1)                    
    if(isStart):
        df_end = df
        isStart = False
    else:
        df_end = df_end.append([df])
        
#df_end.to_csv('C:/Users/noypr/Downloads/ExAnimals.csv')

