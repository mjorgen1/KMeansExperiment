import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#new python file for setting up the data and functions


#sets up the data from the excel sheet
def compile():
    df = pd.read_excel("/home/mackenzie/PycharmProjects/Practice/ARB Startle FINAL PP1-260 Cleaned_02.10.2017.xlsx", parse_cols= 'A, H, U, AG, AH') #parse_cols= 'C,E,H'
    subjects = np.array(df['Subject_ID'])
    stLat = np.array(df['Startle_Latency']) #takes in the latency data and transforms it into an array
    stLatUpd = [] #creates a blank list for updating with all good data
    stLatMeans = []  #creates a blank list for putting in each subject's latency mean
    stLatDevs = [] #creates a blank list for putting in each subject's latency st dev
    stAmp = np.array(df['Startle_Amp']) #takes in the amplitude data and transforms it into an array
    stAmpUpd = [] #creates a blank list for updating with all good data
    stAmpMeans = [] #creates a blank list for putting in each subject's amplitude mean
    stAmpDevs = [] #creates a blank list for putting in each subject's amplitude st dev
    preFilter = np.array(df['PreStartleFilter'])
    postFilter = np.array(df['PostStartleFilter'])
    trialCount = 0
    for x in range(0, 6208): #filters through all of the tasks/rows
        trialCount += 1
        #checks to make sure data is good and if not moves onto next subject
        if preFilter[x] == 1 & postFilter[x] == 1 & ~np.isnan(stAmp[x]): #checks to see if the data is good
            stAmpUpd.append(stAmp[x])
        else:
            trialCount == 24
        if preFilter[x] == 1 & postFilter[x] == 1 & ~np.isnan(stLat[x]):
            stLatUpd.append(stLat[x])
        else:
            trialCount == 24
        if trialCount== 24: #if this is the last task for a subject then we need to make conclusions
            if not np.isnan(np.mean(stLatUpd)):
                stLatMeans.append(np.mean(stLatUpd))
            if not np.isnan(np.std(stLatUpd)):
                stLatDevs.append(np.std(stLatUpd))
            if not np.isnan(np.mean(stAmpUpd)):
                stAmpMeans.append(np.mean(stAmpUpd))
            if not np.isnan(np.std(stAmpUpd)):
                stAmpDevs.append(np.std(stAmpUpd))
            stLatUpd = [] #empties the list so the next subject will fill them up
            stAmpUpd = []
            trialCount = 0
    return stLatMeans, stLatDevs, stAmpMeans, stAmpDevs

#sum of the squared error
def SSE(centroids, array, labels):
    sse = 0
    for i in range(centroids.shape[0]):  # starts at 0
        for j in range(array.shape[1]):
            if labels[j] == i:
                sse = sse + (centroids[i, 0] - array[0, j]) ** 2 + (centroids[i, 1] - array[1, j]) ** 2
    return sse

#clustering kmeans
def kmeans(data, k,): #will I need to send the datalocation
    dataN = np.array(data)
    clf = KMeans(n_clusters=k)
    clf.fit(dataN.T)
    labels_pr_ = clf.predict(dataN.T)
    centroids = clf.cluster_centers_
    labels = clf.labels_
    return dataN, centroids, labels, labels_pr_

#plotsclusters
def plotClusters(title, data, labels, centroids):
    colors = ["g.", "r.", "c.", "y.", "m."]
    plt.figure()
    for i in range(data.shape[1]):
        plt.plot(data[0, i], data[1, i], colors[labels[i]], markersize=10)
    plt.title(title)
    plt.scatter(centroids[:, 0], centroids[:, 1], color='black', marker="x", s=150, linewidths=10, zorder=10)
    plt.show()

#plots the SSE data
def plotSSE(dataX, dataY, title):
    plt.figure()
    plt.scatter(dataX, dataY, color= 'b', marker= 'o')
    plt.title(title)
    plt.show()

def findBestK(SSEpoints):
    max = 0
    for i in range(19):
        if abs(SSEpoints[i+1]-SSEpoints[i]) > max:
            max = abs(SSEpoints[i+1]-SSEpoints[i])
            kbest = i+2 #think through this logic about k
    return kbest

