#!/usr/bin/env python
# coding: utf-8

# <font size="10">
#     <b>
#         Machine Learning 
#         <b></font>

# In[1]:


import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings("ignore")


# <font size="6">
#     <b>
#         Importing our species data frame
#         <b></font>

# In[2]:


file_param = "./Data/"
clean_n_full_df_csv = "df_numeric.csv"

df = pd.read_csv(file_param + clean_n_full_df_csv, header=0, sep=',')
df.drop("Unnamed: 0",inplace=True, axis=1) 
df


# <font size="6">
#     <b>
#         Dropping string columns with no meaning to prediction
#         <b></font>

# In[3]:


string_columns_to_drop = ["Scientific Name","Conservation Status"]
df.set_index('Common Name',inplace=True)
df.drop(string_columns_to_drop,inplace=True, axis=1) 


# In[4]:


df


# In[5]:


df.corr()


# <font size="6">
#     <b>
#         Machine Learning process
#         <b></font>

# In[6]:


features = df.columns[df.columns != 'IsExtinct']
X = df[features]
y = pd.Series(df['IsExtinct'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf_model = LogisticRegression().fit(X_train, y_train)
y_pred = clf_model.predict(X_test)

resDF = pd.DataFrame({"Actual":y_test,"Predicted":y_pred})

resDF["correct"] = abs((resDF["Actual"] + resDF["Predicted"]) - 1)
resDF[resDF["correct"] == 1]


# In[7]:


print("correct %:",len(resDF[resDF["correct"] == 1]) / len(resDF))


# <font size="6">
#     <b>
#         Feature Engineering and DataFrame Prediction
#         <b></font>

# <font size="3">
#     <b>
#         Trying to get an even better prediction accuracy, we combined the numeric columns "Birth rate" and "Conception Period"
#         <b></font>

# In[8]:


acc_df = df
acc_df["Birth rate AND Conception Period"] = acc_df["Birth rate"]*acc_df["Conception Period"]
acc_df.drop("Birth rate",axis=1,inplace =True)
acc_df.drop("Conception Period",axis=1,inplace =True)


# In[9]:


features = acc_df.columns[acc_df.columns != 'IsExtinct']
X = acc_df[features]
y = pd.Series(acc_df['IsExtinct'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf_model = LogisticRegression().fit(X_train, y_train)
y_pred = clf_model.predict(X_test)

resDF = pd.DataFrame({"Actual":y_test,"Predicted":y_pred})

resDF["correct"] = abs((resDF["Actual"] + resDF["Predicted"]) - 1)
resDF[resDF["correct"] == 1]


# In[10]:


print("correct %:",len(resDF[resDF["correct"] == 1]) / len(resDF))


# <font size="3">
#     <b>
#         After creating a better accuracy we used the model to predict all of the species status
#         <b></font>

# In[11]:


predict = clf_model.predict(X)
df['Prediction'] = predict
predict_df = df[['IsExtinct','Prediction']]
#predict_df.to_csv('C:/Users/noypr/Downloads/df_full_ex_prediction.csv')


# In[12]:


predict_df


# <font size="3">
#     <b>
#         Showing the Species that are predicted to get extinct by the model
#         <b></font>

# In[13]:


df_got_ex = predict_df[(predict_df.IsExtinct == 0) & (predict_df.Prediction == 1)]


# In[14]:


df_got_ex

