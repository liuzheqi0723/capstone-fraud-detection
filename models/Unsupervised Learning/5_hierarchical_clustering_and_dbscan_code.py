
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy 
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import seaborn as sns

"""#Hierarchical Clustering"""

#create a dataframe for hierarchical clustering with only 15% of dataset
df_pca_kmeans_head=df_pca_kmeans.head(20225)
hierarchical_data=df_pca_kmeans_head.iloc[:,:-16]

#Create dendogram of original data to get an idea of number of clusters in data
model = scipy.cluster.hierarchy.linkage(hierarchical_data, method='ward')

fig=plt.figure(figsize=(10,10))
scipy.cluster.hierarchy.dendrogram(model)
plt.show()

#Do agglomerative clustering specifically for k=3 and evaluate its silhoutte socre and Davies Bouldin Score
cluster = AgglomerativeClustering(n_clusters=3,affinity='euclidean', linkage='ward')  
assigning_clusters = cluster.fit_predict(hierarchical_data)
result = cluster.labels_
plt.figure(figsize=(10, 7))  
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.scatter(df_pca_kmeans_head['component 1'], df_pca_kmeans_head['component 2'], c=result, cmap='rainbow') 
print("Silhouette Score for k = 3: " + str(silhouette_score(hierarchical_data, assigning_clusters)))
print("Davies Bouldin Score for k = 3: " + str(davies_bouldin_score(hierarchical_data, assigning_clusters)))

#add a column with the hierarchical labels
df_pca_kmeans_head['hier_Label'] = result

#compare hierarchical clustering for clusters for 2 to 9
#create 2d scatterplots for visualization and generate silhouette scorea and davies-bouldin score for each model
for num in range(2,10):
  cluster = AgglomerativeClustering(n_clusters=num,affinity='euclidean', linkage='ward')  
  assigning_clusters = cluster.fit_predict(hierarchical_data)
  plt.figure(figsize=(10, 7))  
  plt.scatter(df_pca_kmeans_head['component 1'], df_pca_kmeans_head['component 2'], c=result, cmap='rainbow') 
  plt.xlabel('Principal Component 1')
  plt.ylabel('Principal Component 2')
  print("Silhouette Score for num= " + str(num) + " " + str(silhouette_score(hierarchical_data, assigning_clusters)))
  print("Davies Bouldin Score for num = " + str(num) + " " + str(davies_bouldin_score(hierarchical_data, assigning_clusters)))

"""#DBSCAN"""

#filter a fraction of dataset`15% and create a dataframe for DBSCAN clustering
X_pca_head=X_pca.head(int(len(X_pca)*0.15))

#create visualization to find optimal epsilon level 
plt.figure(figsize=(10,5))
nn = NearestNeighbors(n_neighbors=5).fit(X_pca_head)
distances, idx = nn.kneighbors(X_pca_head)
distances = np.sort(distances, axis=0)
distances = distances[:,1]
plt.plot(distances)
plt.ylim([0, 30])
plt.show()

#Try DBSCAN clustering with epsilons between 2.5-5 and minimum samples as 30, plot, and generate scores
#create visualizations for clusters and generate silhouette score and davies bouldin indices
Silhouette =[]
davies_bouldin=[]

for eps in np.arange(2.5, 12, 0.5):
  db = DBSCAN(eps=eps, min_samples=30)
  db.fit_predict(X_pca_head)
  assigning_clusters = db.labels_
  plt.figure(figsize=(10, 7))  
  plt.scatter(X_pca_head['0'], X_pca_head['1'], c=db.labels_, cmap='rainbow') 
  plt.xlabel('Principal Component 1')
  plt.ylabel('Principal Component 2')
  #print(assigning_clusters)
  print("Silhouette Score for eps = " + str(eps) + " " + str(silhouette_score(X_pca_head, assigning_clusters)))
  print("Davies Bouldin Score for eps = " + str(eps) + " " + str(davies_bouldin_score(X_pca_head, assigning_clusters))) 
  Silhouette.append(silhouette_score(X_pca_head, assigning_clusters))
  davies_bouldin.append(davies_bouldin_score(X_pca_head, assigning_clusters))

#create visaulization for silhouette and davies-bouldin scores
lst=[2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5]
t_list = [lst,Silhouette, davies_bouldin]
df = pd.DataFrame({'eps': lst, 'Silhouette': Silhouette, 'davies_bouldin': davies_bouldin})
df.plot(x="eps", y=["Silhouette", "davies_bouldin"], kind="line", figsize=(9, 6))

#Try DBSCAN clustering with epsilons of 8.5 and minimum samples as 30, plot, and generate scores
db = DBSCAN(eps=8.5, min_samples=30).fit(X_pca_head)
labels = db.labels_
print("Silhouette Score for eps = " + str(8.5) + " " + str(silhouette_score(X_pca_head, labels)))
print("Davies Bouldin Score for eps = " + str(8.5) + " " + str(davies_bouldin_score(X_pca_head, labels)))

# Number of clusters in labels and number of noise points.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)
print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

#add a column with DBSCAN clustering labels 
X_pca_head['DBSCAN_cluster']=labels

#plot in a 3D scatter plot for 3 clusters
import plotly.express as px
fig = px.scatter_3d(X_pca_head, x='0', y='1', z='2', color='DBSCAN_cluster',                 
                    width=700,
                    height=700)                 
#fig.update_layout(showlegend=False)
fig.show()
