
### import libraries ###
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_transformer
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

"""#Prepare data for PCA and unsupervised learning models"""

X_null = X.isnull().sum(axis=0).to_frame() # count Nans in every col.
X_null.rename(columns={0: '#_Nans'}, inplace=True) # rename cols.
# create dataframe that contains columns with more than 1 Nan
df_temp = X_null[X_null['#_Nans']>0]

#find columns that only have Nan and drop them
for c in df_temp.index.tolist():
    if len(X[c].unique())<=1:
          print(c )
X=X.drop(columns=['dist1', 'D11'], inplace=False)



"""## Create encoding for categorical vairables"""


categorical_columns = X.dtypes[X.dtypes == np.object].index.tolist() # list of columns with categorical variables

#create ordinal encoders for categorical variables
from sklearn.preprocessing import OrdinalEncoder
oe = OrdinalEncoder( dtype=int)
oe.fit(X[categorical_columns])
X[categorical_columns] = oe.transform(X[categorical_columns])



"""##fill Nan"""

### Step 1:
# filter out the cols with Nans.
X_null = X.isnull().sum(axis=0).to_frame() # count Nans in every col.
X_null.rename(columns={0: '#_Nans'}, inplace=True) # rename cols.
X_NanCols = X_null[X_null['#_Nans']>0].index # get a series contains all the names of cols with Nan.
X_fullCols = X_null[X_null['#_Nans']==0].index   # column names without NA

# make lists, indicating which stratage will be used in imputing the cols.
cols_fill_mean = []
cols_fill_freq = []

for col in X_NanCols:
  if str(col).startswith('C'): # cols C1-C1
    cols_fill_freq.append(col)
  elif str(col).startswith('D'): # cols D1-D15 and 'Device ...' which has been filled previously.
    cols_fill_freq.append(col)
  else:
    cols_fill_mean.append(col) # cols id_XX and cols has already been filled with other startages earlier.

# make all the cols still included in the following processing
cols_fill_freq.extend(X_fullCols.to_list())

# Step 2:
# instantiate the imputers, within a pipeline
# imputer imputes with the mean
imp_mean = Pipeline(steps=[('imputer', SimpleImputer(missing_values=np.nan, strategy='mean'))])


# imputer imputes with 'most_frequent'
imp_freq = Pipeline(steps=[('imputer',SimpleImputer(missing_values=np.nan, strategy='most_frequent'))])

# Step 3:
# put the features list and the transformers together by col transformer.
imp_preprocessor = ColumnTransformer(transformers=[('imp_mean', imp_mean, cols_fill_mean),\
                                                   ('imp_freq',imp_freq,cols_fill_freq)])#,remainder='passthrough' )

# Step 4:
# fit and trans the dataset with 'imp_preprocessor'.

imp_preprocessor.fit(X)
X_train = imp_preprocessor.transform(X)



"""##create a dataframe df_PCA that have Nan filled and encodings created for categorical variables"""

# create a dataframe to be used for PCA and unsupervised learning
df_PCA = pd.DataFrame(imp_preprocessor .fit_transform(X), columns=X.columns, index=X.index)

y_train=y


"""# k-means with PCA"""

#create a vairance ratio plot
#Create graph to see the relationship between number of principal components and explained variance. 
X_df = df_PCA
scalar = StandardScaler()
X_scaled = pd.DataFrame(scalar.fit_transform(X_df), columns=X_df.columns)

pca = PCA().fit(X_scaled)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of principal components')
plt.ylabel('Cumulative explained variance')

plt.xlim([0, 30])

pca15=PCA(n_components=15)

score_PCA=pca15.fit_transform(X_scaled)
X_pca=pd.DataFrame(score_PCA)


"""##K-means clustering into 2 clusters(fraud and nonfraud)  with PCA results"""

from sklearn.cluster import KMeans
kmeans_PCA=KMeans(n_clusters=2,init="k-means++",random_state=42)

#fit data after PCA with k-means model
kmeans_PCA.fit_predict(score_PCA)

#create a dataframe with PCA scores and assigned cluster
df_pca_kmeans=pd.concat([df_PCA.reset_index(drop=True),pd.DataFrame(score_PCA)],axis=1)
df_pca_kmeans.columns.values[-15:]=["component 1","component 2","component 3","component 4",
                                    "component 5","component 6","component 7","component 8",
                                    "component 9","component 10","component 11","component 12",
                                    "component 13","component 14","component 15"]

#add a column for the assigned cluster
df_pca_kmeans['pca_kmeans_cluster']=kmeans_PCA.labels_

"""##result of two clusters"""

df_pca_kmeans['pca_kmeans_cluster'].value_counts()

"""###Visualize 2 Clusters by Principle Components """

#create a dataframe with only the last 16 columns of df_pca_kmeans
PCA_columns  = df_pca_kmeans.iloc[: , -16:]

#df_pca_kmeans .to_csv('df_pca_kmeans.csv')
#!cp df_pca_kmeans.csv "drive/MyDrive/Capstone/Data/"

#visualize two clusters in 2D scatterplot
import seaborn as sns
x_axis=PCA_columns ["component 1"]
y_axis=PCA_columns ["component 2"]
plt.figure(figsize=(10,7))
sns.scatterplot(x_axis,y_axis,hue=PCA_columns ['pca_kmeans_cluster'])
plt.title("cluster by PCA and Kmeans")
plt.show

#plot in a 3D scatter plot
import plotly.express as px
fig = px.scatter_3d(PCA_columns, x='component 1', y='component 2', z='component 3', color='pca_kmeans_cluster',                 
                    width=700,
                    height=700)                 
fig.show()

"""## Conduct Elbow distortion method to find ideal number of clusters with PCA data"""

#Conduct Elbow distortion method to find ideal number of clusters with PCA data
model = KMeans()
visualizer = KElbowVisualizer(model, k=(1,11))
visualizer.fit(score_PCA)    
visualizer.show()

"""##Kmeans clustering into 3 clusters with PCA results"""

kmeans_PCA_3=KMeans(n_clusters=3,init="k-means++",random_state=42)
#fit data after PCA with k-means model
kmeans_PCA_3.fit_predict(score_PCA)

#create a dataframe with PCA scores and assigned cluster
df_pca_kmeans_3clus=pd.concat([df_PCA.reset_index(drop=True),pd.DataFrame(score_PCA)],axis=1)
df_pca_kmeans_3clus.columns.values[-15:]=["component 1","component 2","component 3","component 4",
                                    "component 5","component 6","component 7","component 8",
                                    "component 9","component 10","component 11","component 12",
                                    "component 13","component 14","component 15"]

#add a column for the assigned cluster
df_pca_kmeans_3clus['pca_kmeans_cluster']=kmeans_PCA_3.labels_

"""###result of 3 clusters"""

df_pca_kmeans_3clus['pca_kmeans_cluster'].value_counts()

"""###visualize 3 clusters"""

#create a dataframe with only the last 16 columns of df_pca_kmeans
PCA_columns_3clus  = df_pca_kmeans_3clus.iloc[: , -16:]

#visualize two clusters in 2D scatterplot
import seaborn as sns
x_axis=PCA_columns_3clus  ["component 1"]
y_axis=PCA_columns_3clus  ["component 2"]
plt.figure(figsize=(10,7))
sns.scatterplot(x_axis,y_axis,hue=PCA_columns_3clus ['pca_kmeans_cluster'])
plt.title("cluster by PCA and Kmeans")
plt.show

#plot in a 3D scatter plot
import plotly.express as px
fig = px.scatter_3d(PCA_columns_3clus , x='component 1', y='component 2', z='component 3', color='pca_kmeans_cluster',                 
                    width=800,
                    height=800)                 
#fig.update_layout(showlegend=False)
fig.show()


"""##Compare Silhouette score and Davies Bouldin Score for clusters of 2 and 3"""

for num in range(2,4):
    kmeans = KMeans(n_clusters=num)
    kmeans.fit_predict(score_PCA)
    assigning_clusters = kmeans.labels_    
    print("Silhouette Score for k = " + str(num) + " " + str(silhouette_score(score_PCA, assigning_clusters)))
    print("Davies Bouldin Score for k = " + str(num) + " " + str(davies_bouldin_score(score_PCA, assigning_clusters)))
