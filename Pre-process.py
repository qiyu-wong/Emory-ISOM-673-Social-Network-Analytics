# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:19:09 2020

@author: 10331
"""
import pandas as pd

with open('C:/Users/10331/OneDrive/Desktop/SNA project/amazon-meta.txt', 'r', encoding="utf8") as file:
    data = file.read().replace("\n","")


data = data.split("Id:")
    
df = pd.DataFrame(data)

df.head()

df = df.iloc[1:,:]

df.iloc[1,0]

labels = ["reviews:", "categories:", "similar:", "salesrank:","group:","title:", "ASIN:"]

df = df.rename(columns={0: 'Id'})

df.columns

for i in range(len(labels)):
    tmp = df.Id.str.split(labels[i],expand = True)
    df["Id"] = tmp[0]
    df[labels[i]] = tmp[1]
    #for j in range(len(df)):

df.dtypes

pd.set_option('display.max_columns', 10)

df

#%%

review = df.loc[:,["Id","reviews:"]]

labels = ["avg rating:", "downloaded:"]

review = review.rename(columns={"reviews:": 'total'})

for i in range(len(labels)):
    tmp = review.total.str.split(labels[i],expand = True)
    review["total"] = tmp[0]
    review[labels[i]] = tmp[1]
    
tmp = review.total.str.split(" ",expand = True)
review["total"] = tmp[2]

#%%

review = review.rename(columns={"avg rating:": 'avg_rating'})
tmp = review.avg_rating.str.split(" ",1,expand = True)

tmp = tmp.rename(columns={1: 'avg_rating'})
tmp = tmp.avg_rating.str.split(" ",1,expand = True)

review["avg_rating"] = tmp[0]
review["reviews"] = tmp[1]

review

#%%
import re

tmp = review['reviews'].apply(lambda x: re.sub(r'\s+\d{4}-',"*", str(x)))
tmp = pd.DataFrame(tmp)

tmp = tmp.reviews.str.split("*",expand = True)

#%%
#tmp = review.reviews.str.rsplit("\r",expand = True)

#tmp = review.reviews.str.extract('(\d{4}-\d{1,2}-\d{1,2}\s+cutomer:\s+\S{14}\s+rating:\s+\d+\s+votes:\s+\d+\s+helpful:\s+\d+)', expand=True)

#%%
tmp = tmp.iloc[:,1:]

review = review.drop("reviews",axis=1)

tmp = pd.concat([review,tmp],axis=1)

tmp.columns

tmp = tmp.melt(id_vars=['Id', 'total', 'avg_rating', 'downloaded:'])

labels = ["helpful:", "votes:","rating:","cutomer:"]

for i in range(len(labels)):
    tmp2 = tmp.value.str.split(labels[i],expand = True)
    tmp["value"] = tmp2[0]
    tmp[labels[i]] = tmp2[1]

tmp2.dropna(subset=['cutomer:'], inplace=True)

review = tmp.iloc[:,:]

review
