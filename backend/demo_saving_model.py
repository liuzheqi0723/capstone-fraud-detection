from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
n_neighbors = 5
knn = KNeighborsClassifier(n_neighbors=n_neighbors)
dump(knn, 'KNN.joblib')