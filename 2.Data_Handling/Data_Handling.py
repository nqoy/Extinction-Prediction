#!/usr/bin/env python
# coding: utf-8

# <font size="10">
#     <b>
#         Data Handling
#         <b></font>

# In[1]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


# <font size="3">
#     <b>
#         Importing both our species data frames
#         <b></font>

# In[2]:


file_param = "./Data/"
Ex_csv = "ExAnimals.csv"
AZ_csv ="A-Z.csv"
df_AZ = pd.read_csv(file_param + AZ_csv, header=0, sep=',')
df_EX = pd.read_csv(file_param + Ex_csv, header=0, sep=',')


# <font size="3">
#     <b>
#         Handling the Extinct data frame - Dropping Duplicats, Renaming Columns to match the living species df
#         <b></font>

# In[3]:


df_EX.drop_duplicates(inplace = True)
df_EX["Conservation Status"] = "Extinct"
df_EX = df_EX.rename(columns={"Species:": "Species","Kingdom:": "Kingdom","Phylum:": "Phylum","Class:": "Class",
                               "Order:": "Order","Family:": "Family","Genus:": "Genus","Subphylum:": "Subphylum",
                               "Subfamily:": "Subfamily","Tribe:": "Tribe","Subtribe:": "Subtribe","Clade:": "Clade",
                               "Suborder:": "Suborder","Infraclass:": "Infraclass","Subspecies:": "Subspecies",
                                "Subgenus:": "Subgenus","Common name": "Common Name", "Former range": "Locations",
                                "Causes": "Biggest Threat"})


# <font size="3">
#     <b>
#         Merging both data frame into one
#         <b></font>

# In[4]:


df = df_AZ.append(df_EX)
rows = len(df.axes[0])
df.index = range(rows)
df.drop("Unnamed: 0", axis=1, inplace=True)
df


# <font size="8">
#     <b>
#         Cleaning The Data Frame
#         <b></font>

# <font size="3">
#     <b>
#         Merging columns with the same meaning
#         <b></font>

# In[5]:


df['Birth rate'] = df["Average Litter Size"].fillna(df["Average Spawn Size"])
df['Conception Period'] = df["Gestation Period"].fillna(df["Incubation Period"])
df["Scientific Name"].fillna(df["Binomial name"], inplace = True)
df["Scientific Name"].fillna(df['Other Name(s)'], inplace = True)
df["Scientific Name"].fillna(df['Common Name'], inplace = True)
df['Common Name'].fillna(df['Scientific Name'], inplace = True)


# <font size="3">
#     <b>
#         Deleting None-Relevent\Problamtic-Data\Merged columns
#         <b></font>

# In[6]:


columns_to_delete = ["Prey","Name Of Young","Group Behavior","Fun Fact","Estimated Population Size"
                     ,"Most Distinctive Feature","Habitat","Number Of Species","Location",
                     "Slogan","Group","Top Speed","Weight","Length","Age of Sexual Maturity","Age of Weaning","Distinctive Feature",
                     "Temperament","Training","Height","Main Prey","Favorite Food","Subphylum","Subfamily","Species","Tribe",
                     "Subtribe","Clade","Suborder","Infraclass","Subspecies", "Subgenus","Litter Size","Gestation Period",
                     "Average Litter Size", "Binomial name","Last record","Declared extinct", "Genus", "Kingdom",'Other Name(s)','Lifestyle']


df.drop(columns_to_delete, axis=1, inplace=True)


# <font size="3">
#     <b>
#         Deleting Columns by missing data threshold
#         <b></font>

# In[7]:


columns_with_N_data_to_delete = 130
df_clean_col = df.dropna(axis = 1, thresh = columns_with_N_data_to_delete)
rows = len(df_clean_col.axes[0])
df_clean_col.index = range(rows)


# In[8]:


df_clean_col


# <font size="8">
#     <b>
#         Handling Missing Data
#         <b></font>

# <font size="6">
#     <b>
#         Dividing the Dataframe and filling missing values
#         <b></font>

# <font size="3">
#     <b>
#         Extracting the uniqe elements to execute the split and initialize the column names to be handled
#         <b></font>

# In[9]:


class_to_split_list = df_clean_col.Class.dropna().unique().tolist()
columns_to_most_frequent_value = ['Phylum','Class', 'Order','Family','Diet','Color',"Locations"
                                  'Skin Type','Predators','Lifespan','Type','Birth rate','Conception Period']
df_no_nan = pd.DataFrame(columns = df_clean_col.columns)


# <font size="3">
#     <b>
#         Function to replace missing data of spesific columns
#         <b></font>

# In[10]:


def replace_missing_values(df, columns_to_most_frequent_value):
 
    for col in df:
        if col in columns_to_most_frequent_value:
            if df[col].mode().empty:
                continue  
            df[col].fillna(df[col].mode()[0], inplace=True)
            
    return df.copy()


# <font size="3">
#     <b>
#         Splitting The clean data frame by <font size="5">Class</font>, the specific Class-DF is splitted further by <font size="5">Order</font> and missing data is replaced.
#         After replcing the missing data, we append each Order-DF to a new DF.
#         <b></font>

# <font size="3">
#     <b>
# The new and full DF that includes all of the data by Order will replace missing data by the Class property.
#                 <b></font>

# In[11]:


for calss_name in class_to_split_list:
    df_class_split = df_clean_col[df_clean_col['Class'] == calss_name]
    order_to_split_list = df_class_split.Order.dropna().unique().tolist()
    for order_name in order_to_split_list:
        if not order_to_split_list:
            df_no_nan.append(df_class_split)
            continue #Empty
        df_order_split = df_class_split[df_class_split['Order'] == order_name]
        df_no_nan = df_no_nan.append(replace_missing_values(df_order_split,columns_to_most_frequent_value))
    df_no_nan = replace_missing_values(df_no_nan,columns_to_most_frequent_value)
        
rows = len(df_no_nan.axes[0])
df_no_nan.index = range(rows)


# In[12]:


df_no_nan


# <font size="6">
#     <b>
#         Text Analyzation
#         <b></font>

# <font size="3">
#     <b>
#         Initializing the words/lettes and properties split to extrect from the strings in "Biggest Threat" column
#         <b></font>

# In[13]:


column_to_split = "Biggest Threat"
threat_split_columns =["Habitat Loss","Climate Change","Human Influance","Pollution",
                       "Hunting","Predation","Disease","Invasive Species","Food Competition"]

Habitat_loss_text = ["dry","graz","vegetation","habitat","destru","land","envir","defo","lack"]
Climate_change_text = ["clim" "change","warm","temp","drou","aridi","fire"]
Human_influance_text = ["event","dry","catt","sewa","floo","pump","impo","extrac","log","over","exter","agric","capt","huma","man","trap","road","harve","acc","veh","trad","fur","damm","mini","arti","coll","cru","by ca","cons","comm","hyb"]
Pollution_text = ["poll","poi","pest", "cide","acidi","sewa"]
Hunting_text = ["hunt","poac","perse","fishing"]
Predation_text = ["pred","carni","prey","consu"]
Disease_text = ["dise","patho","chytr","malar","ferti"]
invasive_species_text = ["introd","invas"]
food_competition_text = ["starv","compet","reduc","loss","food"]

list_of_threat_texts =[Habitat_loss_text, Climate_change_text, Human_influance_text, Pollution_text,
                       Hunting_text,Predation_text, Disease_text, invasive_species_text, food_competition_text]

for threat_name in threat_split_columns:
    df_no_nan[threat_name] = 0
df_no_nan["Number Of Threats"] = 0


# <font size="3">
#     <b>
#         Initializing the words/lettes to extrect from the strings in "Lifespan","Birth rate" and "Conception Period" columns
#         <b></font>

# In[14]:


date_kind_text ={'year':360,'month':30, 'week':7}
number_text_dic = {'one':1,'two':2,'three':3,'four':4,'five':5,'six' : 6, 'seven':7,'eight':8,'nine':9,'ten':10,
                            "11":11,"10":10,"15":15,"12":12,"9":9,"8":8,"13":13,"20":20,'4':4,'14':14,'6':6,'50':50,
                            '25':25,'16':16,'unknown':4,'the':3,'1':1,'2':2,'3':3,'45':45,'30':30,'40':40,'1.5':1.5,'a':7,
                            'immortal':1000,'01':1 ,'5':5,'millions':2000000 }

list_of_date_columns =["Lifespan","Birth rate","Conception Period"]


# <font size="3">
#     <b>
#         Initializing the words/lettes and properties split to extrect from the strings in "Locations" column
#         <b></font>

# In[15]:


continent_list =["Africa","America","Asia","Europe","Oceania","Ocean","Antarctica"]
Africa_text = ["Africa","Algeria","Angola","Benin","Botswana","Burkina Faso","Burundi","Cameroon","Cabo Verde","Central African Republic","Chad","Comoros","Congo","Congo (Democratic Republic of the)","Cפte d'Ivoire","Djibouti","Egypt","Equatorial Guinea","Eritrea","Ethiopia","Gabon","Gambia","Ghana","Guinea","Guinea-Bissau","Kenya","Lesotho","Liberia","Libya","Madagascar","Malawi","Mali","Mauritania","Mauritius","Mayotte","Morocco","Mozambique","Namibia","Niger","Nigeria","Rיunion","Rwanda","Saint Helena, Ascension and Tristan da Cunha","Sao Tome and Principe","Senegal","Seychelles","Sierra Leone","Somalia","South Africa","South Sudan","Sudan","Swaziland","Tanzania, United Republic of","Togo","Tunisia","Uganda","Western Sahara","Zambia","Zimbabwe","Vulnerable","Northern and centralAndes","Patagonia","Rocky Mountains","CorsicaandSardinia","Southern Rocky Mountains","Pampas and Patagonia","EasternBeringia","Maghreb"]
America_text = ["America","United States","USA","Anguilla","Antigua and Barbuda","Argentina","Aruba","Bahamas","Barbados","Belize","Bermuda","Bolivia","Bonaire, Sint Eustatius and Saba","Brazil","Canada","Cayman Islands","Chile","Colombia","Costa Rica","Cuba","Curaחao","Dominica","Dominican Republic","Ecuador","El Salvador","Falkland Islands","French Guiana","Greenland","Grenada","Guadeloupe","Guatemala","Guyana","Haiti","Honduras","Jamaica","Martinique","Mexico","Montserrat","Nicaragua","Panama","Paraguay","Peru","Puerto Rico","Saint Barthיlemy","Southern Cone","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Sint Maarten","Suriname","Trinidad and Tobago","Turks and Caicos Islands","United States of America","Uruguay","Venezuela","Virgin Islands","Virgin Islands","Northern Maghreb","Arabian Peninsula","Mesopotamia","Northern Siberia","Timor","Timor","Cyrenaicacoast","Barbuda",]
Asia_text = ["Asia","Eurasia","Afghanistan","Armenia","Azerbaijan","Bahrain","Bangladesh","Bhutan","Brunei Darussalam","Cambodia","China","Cyprus","Georgia","Hong Kong","India","Indonesia","Iran (Islamic Republic of)","Iraq","Israel","Japan","Jordan","Kazakhstan","Korea (Democratic People's Republic of)","Korea (Republic of)","Kuwait","Kyrgyzstan","Lao People's Democratic Republic","Lebanon","Macao","Malaysia","Maldives","Mongolia","Myanmar","Nepal","Oman","Pakistan","Palestine, State of","Philippines","Qatar","Saudi Arabia","Singapore","Sri Lanka","Syrian Arab Republic","Taiwan, Province of China","Tajikistan","Thailand","Timor-Leste","Turkey","Turkmenistan","United Arab Emirates","Uzbekistan","Viet Nam","Yemen""Southern Cone","North Atlanticand theMediterranean","SoutheasternTasmania","Northern Maghreb","Central ridge ofSt Helenaisland","North Atlantic and western Mediterranean","Tristan da Cunha","Portuguese-Galicianborder","St. Vincent","Northern CaucasusandTranscaucasianshore of theBlack Sea","Northern Andes",]
Europe_text = ["Europe","Eurasia","Réunion","ֵland Islands","Albania","Andorra","Rֳ©union","Austria","Belarus","Belgium","Bosnia and Herzegovina","Bulgaria","Croatia","Czech Republic","Denmark","Estonia","Faroe Islands","Finland","France","Germany","Gibraltar","Greece","Guernsey","Holy See","Hungary","Iceland","Ireland","Isle of Man","Italy","Jersey","Latvia","Liechtenstein","Lithuania","Luxembourg","Macedonia (the former Yugoslav Republic of)","Malta","Moldova (Republic of)","Monaco","Montenegro","Netherlands","Norway","Poland","Portugal","Romania","Russian Federation","San Marino","Serbia","Slovakia","Slovenia","Spain","Svalbard and Jan Mayen","Sweden","Switzerland","Ukraine","United Kingdom of Great Britain and Northern Ireland","Cape Verde","Caucasus Mountains","Near East","St Kilda, Scotland","ContinentalCascadia","Arabian Peninsula and the Near East","St Luciamountains",]
Oceania_text = ["Oceania","American Samoa","Australia","Fiji","French Polynesia","Guam","Kiribati","Micronesia","Nauru","New Caledonia","New Zealand","Niue","Palau","Papua New Guinea","Pitcairn","Samoa","Tokelau","Tonga","Tuvalu","Vanuatu","Wallis and Futuna","UpperRio Grande","Arabian Peninsula","Rio Grande","Aridoamerica","Maui, Lana'i, and Molokai, Hawaii",]
Ocean_text=["Ocean","Island","Rodrigues","Saint Helena","Hispaniola","Corsica and Sardinia","Cook Islands","Marshall Islands","Norfolk Island","Northern Mariana Islands","Solomon Islands","Lake","Taiwan","Atlas Mountains","Iberian Peninsula","Pyrenees",]
Antarctica_text = ["Antarctica"]

list_of_continent_texts = [Africa_text, America_text, Asia_text,
                           Europe_text, Oceania_text, Ocean_text, Antarctica_text]

for continent in continent_list:
    df_no_nan[continent] = 0
df_no_nan["Number Of Locations"] = 0


# <font size="3">
#     <b>
#         Initializing the words/lettes to combine same elements with diffrent names for "Skin Type" column
#         <b></font>

# In[16]:


skin_type_text ={'shell':"Shell",'spik':"Hair", 'scales':"Scales",'plates':"Hard Skin",
                 'hair':"Hair",'wool':"Fur",'skin':"Smooth",'tough':"Hard Skin",
                 'rough':"Hard Skin"}


# <font size="3">
#     <b>
#         Iterating for each index on the DF and filling the data by the text analyzation keys
#         <b></font>

# In[17]:


df_split = df_no_nan
df_split["IsExtinct"] = 0 
j = 0

for i in range(0,len(df_split.index)):
    
    ##Threats split
    index_in_list_count = 0
    for threat_text in list_of_threat_texts:
        for threat_letters in threat_text:
            if threat_letters in str(df_split["Biggest Threat"].values[i]).lower():       
                df_split[threat_split_columns[index_in_list_count]].iloc[i] = 1
                df_split["Number Of Threats"].iloc[i] += 1
                break
        index_in_list_count += 1
      
    ##Locations split
    index_in_list_count = 0
    for continent_text in list_of_continent_texts:
        for continent_letters in continent_text:
            if continent_letters in str(df_split["Locations"].values[i]):
                if(continent_list[index_in_list_count] in str(df_split["Locations"].values[i])):
                    if(continent_letters in continent_list[index_in_list_count]):
                        df_split[continent_list[index_in_list_count]].iloc[i] = 1
                        df_split["Number Of Locations"].iloc[i] += 1
                        break
        index_in_list_count += 1
        
    if(df_split["Number Of Locations"].iloc[i] == 0):
        if(j < 7):
            j = 0
        df_split["Number Of Locations"].iloc[i] = 1
        df_split[threat_split_columns[j]].iloc[i] = 1
        index_in_list_count += 1
        j += 1
        
    ##Counting predetors
    predetors_count = df_split["Predators"].iloc[i].count(",")
    df_split["Predators"].iloc[i] = predetors_count + 1
    
    ##Is_Extinct
    if "Extinct" in str(df_split["Conservation Status"].values[i]):
        df_split["IsExtinct"].iloc[i] = 1

##Getting values from text

    #Integers
    for column_name in list_of_date_columns:
        text = str(df_split[column_name].values[i]).lower().split()
        digit = 0
        date_kind = 0
        for word in text:
            if digit == 0:
                if word.isdigit():
                    digit = int(word)
            if digit == 0:
                for key_number_text in number_text_dic.keys():
                    if key_number_text in word:
                        digit = number_text_dic.get(key_number_text)
                        break

            for key_date_kind_text in date_kind_text.keys():
                if key_date_kind_text in word:
                    date_kind = date_kind_text.get(key_date_kind_text)
                    
        if date_kind == 0:
            date_kind = 1
        digit *= date_kind

        if column_name == 'Lifespan':
            df_split[column_name].iloc[i] = round(digit / 360)
        elif column_name == 'Conception Period':
            df_split[column_name].iloc[i] = round(digit / 7)
        else:
            df_split[column_name].iloc[i] = round(digit)
            
    ##Skin Type
    text = str(df_split["Skin Type"].values[i]).lower()
    for skin_type_name in skin_type_text:
        if skin_type_name in text:
            df_split["Skin Type"].iloc[i] = skin_type_text.get(skin_type_name)
            break


# <font size="3">
#     <b>
#         Dropping columns that were split
#         <b></font>

# In[18]:


df_split.drop("Biggest Threat", axis = 1, inplace = True)
df_split.drop("Locations", axis = 1, inplace = True)
df_split.replace(np.nan, "None", inplace = True)
#df_split.to_csv('C:/Users/noypr/Downloads/df_full.csv')


# In[19]:


df_split


# <font size="8">
#     <b>
#         Data Convertion
#         <b></font>

# <font size="3">
#     <b>
#         Converting columns with unique and limited elements from categorial to numeric values
#         <b></font>

# In[20]:


categorical_columns_to_numeral = ["Phylum","Class","Order","Family","Skin Type","Diet","Color","Type"]
df_to_numeric = df_no_nan

for col in categorical_columns_to_numeral:
        df_to_numeric[col] = pd.factorize(df_to_numeric[col])[0]
        df_to_numeric[col] = df_to_numeric[col].astype("category")
#df_to_numeric.to_csv('C:/Users/noypr/Downloads/df_numeric.csv')


# In[21]:


df_to_numeric

