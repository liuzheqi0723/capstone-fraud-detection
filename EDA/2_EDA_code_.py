

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder

"""#Use dataframes from 1_Datasets_Understanding_&_Clean.py"""

#name dataframe
clean_train_id.name="clean_train_id"
clean_train_trans.name='clean_train_trans'

"""# Explore Pairwise Correlations"""

#Create correlation heatmaps showing the correlation between variables in the clean_train_id dataframe
#create a function "correlation_heatmap" that creates a correlation heatmap for the input dataframe
def correlation_heatmaps(df):
    plt.figure(figsize=(15,12))
    palette=sns.diverging_palette(20,220,n=256)
    corr=df.corr(method="kendall")
    sns.heatmap(corr, annot=True, fmt=".2f",cmap=palette, center=0,square=True,linewidth=0.5, cbar_kws={"shrink":.5})
    plt.title(df.name+" Correlation Matrix",size=15, weight="bold")
correlation_heatmaps(clean_train_id)

#find the highest 20 correlated variables in clean_train_trans
matr=clean_train_trans.corr().abs().unstack().sort_values(ascending=False).drop_duplicates()
round(matr[:20],20)

"""### C1_to_C14 correlation heatmap"""

#C1-C14: counting, such as how many addresses are found to be associated with the payment card, etc. The actual meaning is masked. 
#Pairwise Correlation heatmap for C1~C14
C1_to_C14_trans_train=clean_train_trans[['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14']]
C1_to_C14_trans_train.head()
C1_to_C14_trans_train.name="C1_to_C14_trans_train"

correlation_heatmaps(C1_to_C14_trans_train)

"""### D1_to_D15 correlation heatmap"""

#Create a correlation heatmap for D1-D15: timedelta, such as days between previous transaction, etc. 

D1_to_D15_trans_train=clean_train_trans[['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D15']]
D1_to_D15_trans_train.head()
D1_to_D15_trans_train.name="D1_to_D15_trans_train"
correlation_heatmaps(D1_to_D15_trans_train)

"""###healmap for Vxxx columns"""

#Create correlation heatmap for: Vxxx: Vesta engineered rich features, including ranking, counting, and other entity relations.
Vxxx_trans_train = clean_train_trans.filter(regex=("^V.*"))
Vxxx_trans_train
Vxxx_trans_train.name="Vxxx_trans_train"

"""###Highest Correlated variables in Vxxx columns"""

# pairs of vairables with the highest correlations in Vxxx columns
matr_v=Vxxx_trans_train.corr().abs().unstack().sort_values(ascending=False).drop_duplicates()
round(matr_v[:10],20)

"""#Further Data Exploration"""

#create a plot to visualize if data is imabalnced or not based on lable isFraud
clean_train_trans['isFraud'].value_counts().plot(kind='bar',figsize=(7, 6), rot=0)
plt.xlabel("isFraud")
plt.ylabel("Count")
plt.title("Count of fraudulent and non-fraudulent transactions")

"""##Transaction Amount Column"""

#transaction amount boxplot by isFraud
g = sns.boxplot(x="isFraud", y="TransactionAmt", data=clean_train_trans,palette="Set3")
sns.set(rc = {'figure.figsize':(10,15)})
plt.ylim(0, 7000)

#create a dataframe with Fraud transactions only and a dataframe with non-fraud transactions only
Fraud=clean_train_trans[clean_train_trans['isFraud']==1]
NonFraud=clean_train_trans[clean_train_trans['isFraud']==0]

#Quantiles of Fraud and No Fraud Transactions
pd.concat([Fraud['TransactionAmt'].quantile([.01, .1, .25, .5, .75, .9, .99]), 
                 NonFraud['TransactionAmt'].quantile([.01, .1, .25, .5, .75, .9, .99])],
                axis=1, keys=['Fraud Transaction Amount', "Non-Fraud Transaction Amount"])

"""###Transaction Amount Distribution"""

# create visualization for Transaction Amount distribution with four subplots
#create a subplot for the distribution of Transation Amount for Fraud transactions
plt.figure(figsize=(16,12))
plt.suptitle('Transaction Amount Distribution')
plt.subplot(221)
g = sns.distplot(Fraud['TransactionAmt'])
g.set_title("Fraud")
g.set_xlabel("Transaction Amount")
g.set_ylabel("Probability")
#create a subplot for the distribution of Transation Amount for Non-Fraud transactions
plt.subplot(222)
g = sns.distplot(NonFraud['TransactionAmt'])
g.set_title("Non-Fraud")
g.set_xlabel("Transaction Amount")
g.set_ylabel("Probability")
#create a subplot for the histogram of Transation Amount for Fraud transactions
plt.subplot(223)
g = sns.histplot(Fraud['TransactionAmt'])
g.set_title("Fraud")
g.set_xlabel("Transaction Amount")
g.set_ylabel("Count")
#create a subplot for the histogram of Transation Amount for Non-Fraud transactions
plt.subplot(224)
g = sns.histplot(NonFraud['TransactionAmt'])
g.set_title("Non-Fraud")
g.set_xlabel("Transaction Amount")
g.set_ylabel("Count")

"""##ProductCD: product code, the product for each transaction"""

# create visualization for ProductCD with four subplots
#Create a histogram for Transaction Amount by Product Code
plt.figure(figsize=(16,12))
plt.suptitle('ProductCD')
plt.subplot(221)
g = sns.countplot(x='ProductCD', data=clean_train_trans,palette="Set3")
g.set_title("ProductCD Distribution")
g.set_xlabel("ProductCD")
g.set_ylabel("Count")
g.set_ylim(0,500000)
# create a histogram of ProductCD by isFraud
plt.subplot(222)
g = sns.countplot(x='ProductCD', hue='isFraud', data=clean_train_trans,palette="Set3")
plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
g.set_title("Count of ProductCD by isFraud")
g.set_xlabel("ProductCD")
g.set_ylabel("Count")
#Create a graph for Transaction amount by product CD
plt.subplot(223)
g = sns.boxenplot(x='ProductCD', y='TransactionAmt', hue='isFraud',data=clean_train_trans,palette="Set3")
g.set_title("Transaction Amount Distribuition by ProductCD (all transactions)")
g.set_xlabel("ProductCD")
g.set_ylabel("Transaction Amount")
#Create a graph for filtered Transaction amount by product CD
plt.subplot(224)
g = sns.boxplot(x='ProductCD', y='TransactionAmt', hue='isFraud',data=clean_train_trans,palette="Set3")
g.set_title("Transaction Amount Distribuition by ProductCD (for transaction amount< 1000)")
g.set_xlabel("ProductCD")
g.set_ylabel("Transaction Amount")
plt.ylim([0, 1000])

#create tables for Transaction Amount by ProductCD with mean, std, and count
clean_train_trans[["TransactionAmt",'ProductCD']].groupby('ProductCD').agg({'TransactionAmt': ['mean', 'std','count']})

#create tables for Transaction Amount by ProductCD and isFraud with mean, std, and count
clean_train_trans[["TransactionAmt",'ProductCD','isFraud']].groupby(['ProductCD','isFraud']).agg({'TransactionAmt': ['mean', 'std','count']})

"""##card1 - card6 : payment card information, such as card type, card category, issue bank, country, etc."""

# create visualization for Card1 information with four subplots
plt.figure(figsize=(16,12))
plt.subplot(221)
g = sns.countplot(x='card4', hue='isFraud', data=clean_train_trans,palette="Set3")
plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
g.set_title("Number of Transactions by Card4 and isFraud")
g.set_xlabel("Card4 Category Names")
g.set_ylabel("Number of Transactions")

plt.subplot(222)
g = sns.countplot(x='card6', hue='isFraud', data=clean_train_trans,palette="Set3")
plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
g.set_title("Number of Transactions by Card6 and isFraud")
g.set_xlabel("Card6 Category Names")
g.set_ylabel("Number of Transactions")

plt.subplot(223)
g = sns.boxplot(x='card4', y='TransactionAmt', hue='isFraud', data=clean_train_trans,palette="Set3")
g.set_title("TransactionAmt by card4 (<1000)")
g.set_xlabel("Card4 Category Names")
g.set_ylabel("Transaction Amount")
plt.ylim([0, 1000])

plt.subplot(224)
g = sns.boxplot(x='card6', y='TransactionAmt', hue='isFraud', data=clean_train_trans,palette="Set3")
g.set_title("TransactionAmt by card6 (<1000)")
g.set_xlabel("Card6 Category Names")
g.set_ylabel("Transaction Amount")
plt.ylim([0, 1000])

#create a table for TransactionAmt by Card4 with mean, std and count
clean_train_trans[["TransactionAmt",'card4']].groupby('card4').agg({'TransactionAmt': ['mean', 'std','count']})

#create a table for TransactionAmt by Card4 and isFraud with mean, std and count
clean_train_trans[["TransactionAmt",'card4','isFraud']].groupby(['card4','isFraud']).agg({'TransactionAmt': ['mean', 'std','count']})

#create a table for TransactionAmt by Card6 with mean, std and count
clean_train_trans[["TransactionAmt",'card6']].groupby('card6').agg({'TransactionAmt': ['mean', 'std','count']})

#create a table for TransactionAmt by Card6 and isFraud with mean, std and count
clean_train_trans[["TransactionAmt",'card6','isFraud']].groupby(['card6','isFraud']).agg({'TransactionAmt': ['mean', 'std','count']})

"""##M1-M9: match, such as names on card and address, etc."""

#create graphs for number of transactions by M1-M9 respectively
for col in ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']: 
    g = sns.countplot(x=col, hue='isFraud', data=clean_train_trans,palette="Set3")
    plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
    g.set_title("Number of Transactions by "+ col+" and isFraud")
    g.set_xlabel("Category Names")
    g.set_ylabel("Number of Transactions")
    plt.show()

#create graphs for Transaction Amount by M1-M9 respectively
for col in ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']: 
   g = sns.boxplot(x=col, y='TransactionAmt', hue='isFraud', data=clean_train_trans,palette="Set3")
   g.set_title("TransactionAmt by " +col+ " (<1000)")
   g.set_xlabel(" Category Names")
   g.set_ylabel("Transaction Amount")
   plt.ylim([0, 1000])
   plt.show()

"""##P_emaildomain: purchaser email domain"""

#create visualization for number of transactions by P_emaildomain and isFraud
plt.figure(figsize=(34,12))
plt.subplot(221)
g = sns.countplot(x='P_emaildomain', hue='isFraud', data=clean_train_trans,palette="Set3")
plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
g.set_title("Number of Transactions by P_emaildomain and isFraud")
g.set_xlabel("P_emaildomain Category Names")
g.set_ylabel("Number of Transactions")
g.set_xticklabels(g.get_xticklabels(),rotation = 70)

#create visualization for number of Fraud and nonFraud Transactions by top 10 P_emaildomain
plt.figure(figsize=(18,12))
plt.subplot(211)
g = sns.countplot(x='P_emaildomain', order=pd.value_counts(Fraud['P_emaildomain']).iloc[:10].index, data=Fraud,palette="Set3")

g.set_title("Number of Fraud Transactions by Top 10 P_emaildomain")
g.set_xlabel("P_emaildomain  Category Names")
g.set_ylabel("Number of Transactions")

plt.subplot(212)
g = sns.countplot(x='P_emaildomain',  order=pd.value_counts(NonFraud['P_emaildomain']).iloc[:10].index,data=NonFraud,palette="Set3")

g.set_title("Number of Non Fraud Transactions by Top 10 P_emaildomain ")
g.set_xlabel("P_emaildomain  Category Names")
g.set_ylabel("Number of Transactions")

"""##R_emaildomain : recipient email domain"""

#create visualization for Number of Transactions by R_emaildomain and isFraud
plt.figure(figsize=(34,12))
plt.subplot(221)
g = sns.countplot(x='R_emaildomain', hue='isFraud', data=clean_train_trans,palette="Set3")
plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
g.set_title("Number of Transactions by R_emaildomain and isFraud")
g.set_xlabel("R_emaildomain Category Names")
g.set_ylabel("Number of Transactions")
g.set_xticklabels(g.get_xticklabels(),rotation = 70)

#create visualization for number of Fraud and nonFraud Transactions by top 10 R_emaildomain
plt.figure(figsize=(18,12))
plt.subplot(211)
g = sns.countplot(x='R_emaildomain', order=pd.value_counts(Fraud['R_emaildomain']).iloc[:10].index, data=Fraud,palette="Set3")
#plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
g.set_title("Number of Fraud Transactions by Top 10 R_emaildomain")
g.set_xlabel("R_emaildomain  Category Names")
g.set_ylabel("Number of Transactions")
#g.set_xticklabels(g.get_xticklabels(),rotation = 70)
plt.subplot(212)
g = sns.countplot(x='R_emaildomain',  order=pd.value_counts(NonFraud['R_emaildomain']).iloc[:10].index,data=NonFraud,palette="Set3")
#plt.legend(title='Fraud', loc='best', labels=['Non-Fraud', 'Fraud'])
g.set_title("Number of Non Fraud Transactions by Top 10 R_emaildomain ")
g.set_xlabel("R_emaildomain  Category Names")
g.set_ylabel("Number of Transactions")
#g.set_xticklabels(g.get_xticklabels(),rotation = 70)

"""##Device Type : type of device used for transaction """

#create a barplot for Device Type
plt.figure(figsize=(8,6))

g = sns.countplot(x='DeviceType', data=clean_train_id,palette="Set3")

g.set_title("Number of Transactions by DeviceType")
g.set_xlabel("DeviceType Category Names")
g.set_ylabel("Number of Transactions")
