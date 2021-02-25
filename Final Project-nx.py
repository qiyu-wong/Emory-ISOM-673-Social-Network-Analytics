
import pandas as pd

data = pd.read_csv("C:/Users/10331/OneDrive/Desktop/Social Network Analytics/Slides/Project/SNA project/review.csv")

import scipy as sp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

data.dtypes

edge = data.loc[:,["cutomer:","Id"]]
edge.columns.values[0] = "source"
edge.columns.values[1] = "target"

edge = edge.groupby(["source","target"]).size().reset_index().\
    rename(columns={0:'weight'})

edge = edge.iloc[:,0:2]

del data

import gc
gc.collect()

edge.dtypes

#%%

import psutil
psutil.virtual_memory()

tmp = edge.target.values.tolist()
tmp = sorted(set(tmp))

edge2 = edge.loc[edge["target"].isin(tmp[10000:]),:]
edge = edge.loc[edge["target"].isin(tmp[0:10000]),:]
edge2.to_csv("C:/Users/10331/OneDrive/Desktop/Social Network Analytics/Slides/Project/SNA project/edge.csv",index=False)
del edge2

#%%

gc.collect()
tmp1 = edge.target.values.tolist()
edge = pd.get_dummies(edge.source)
edge["customer"] = tmp1
tmp1 = sorted(set(tmp1))
gc.collect()

out = pd.DataFrame()
out2 = []
for i in tmp1:
    print(tmp1.index(i))
    c = edge.loc[edge.customer == i,:]
    if len(c) > 1:
        out2.append(i)
        c = c.groupby("customer").sum().reset_index()
        out = out.append(c)
        del c
        gc.collect()
cond = edge["customer"].isin(out2)
cond = np.invert(cond)
sum(cond)
edge = edge.loc[cond,:]
edge = edge.append(out)
del out
del out2
del cond
del tmp1
gc.collect()

edge.set_index("customer")

#%%

psutil.virtual_memory()

gc.collect()
edge2 = pd.read_csv("C:/Users/10331/OneDrive/Desktop/Social Network Analytics/Slides/Project/SNA project/edge.csv")
tmp1 = edge2.target.values.tolist()
edge2 = pd.get_dummies(edge2.source)
edge2["customer"] = tmp1
tmp1 = sorted(set(tmp1))
gc.collect()

out = pd.DataFrame()
out2 = []
for i in tmp1:
    print(tmp1.index(i))
    c = edge2.loc[edge2.customer == i,:]
    if len(c) > 1:
        out2.append(i)
        c = c.groupby("customer").sum().reset_index()
        out = out.append(c)
        del c
        gc.collect()
cond = edge2["customer"].isin(out2)
cond = np.invert(cond)
sum(cond)
edge2 = edge2.loc[cond,:]
edge2 = edge2.append(out)
del out
del out2
del cond
del tmp1
gc.collect()

#%%

gc.collect()
edge = pd.concat([edge, edge2])
del edge2

edge = edge.fillna(0)

edge = sp.sparse.csr_matrix(edge.values)

edge2 = edge.transpose()

df = edge*edge2

del edge2
gc.collect()

#%%

from sklearn.metrics.pairwise import pairwise_distances

jac_sim = 1 - pairwise_distances(df.T, metric = "hamming")
# optionally convert it to a DataFrame
jac_sim = pd.DataFrame(jac_sim, index=df.columns, columns=df.columns)

#%%

from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist, jaccard

res = pdist(df[['category1','category2','category3']], 'jaccard')
squareform(res)
distance = pd.DataFrame(squareform(res), index=df.index, columns= df.index)

#%%

g = nx.from_pandas_edgelist(edge, edge_attr=True, create_using=nx.DiGraph())

l = nx.to_pandas_edgelist(g)

nx.draw(g)
plt.show()

m = nx.to_scipy_sparse_matrix(g)

