import numpy as np
import matplotlib.pyplot as plt

# Naive bayes classifier to determine whether a pilot is fit to fly a plane

'''
SOURCES-
https://youtu.be/CPqOCI0ahss
https://www.saedsayad.com/naive_bayesian.htm
https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
https://www.python-course.eu/naive_bayes_classifier_introduction.php
https://github.com/kbennatti/Look-I-can-python/blob/master/naive_bayesian_classifier.py
https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
'''

# Function to calculate NavieBayes
def NaiveBayesClassifier(data):
    print('Classifying the data based on Naive Bayes theorem\n', 'TestRes/Var1 is the Target Variable\n',
          'Var 2-to-6 are Independent Variables (Features of the dataset)')
    input("Press Enter to continue...")
    # Count the number of target
    # Count number of Yes's and No's
    global tyes
    global tno
    tyes=0
    tno=0
    for i in range(0, len(data)):
        if data[i][1]==1:
            tyes+=1
        else:
            tno+=1
    # print('Target Yes', tyes, 'Target No', tno)

    # Count number of 1s in target (proportion fit to fly)
    # Counting total digits in each column and assigning to diction corresponding to the digit
    # For 2nd column (target) it has 20 0's 20 1's 0 2's 0 3's, so the key in dictionary will have values 20 20 0 0
    # Similarly 3rd column has 9 0's 28 1's 3 2's 0 3's so key in dictionary will have values 9 28 3 0
    # Len(data[0]) is used to specify number of columns that is '6'

    dicCounts = {}
    # Create dictionary of zeroes
    for i in range(0,len(data[0])):
        dicCounts[i]=[0,0,0,0]
    # print (dicCounts)

    countedNumbers = [0,1,2,3]
    for i in range(0, len(data)): #for all rows
        for j in range(0,len(data[i])): #from 0 to 7 for all variables
            for k in range(0, len(countedNumbers)): #for 0 1 2 3 values in each cell
                if data[i][j]==countedNumbers[k]:
                    dicCounts[j][countedNumbers[k]] += 1 #add to dictionary the total counts: key could be from 0-6, for values 0-3
    # print (dicCounts)


    # Calculate the probability of each predictor variable occurring
    # For each column calculate probability of each value from 0 1 2 3
    # Probability will be numberof 0s/40 or numberof1s/40 or numberof2s/40
    dicPredictorProb = {}
    #create dictionary of zeros
    for i in range(0,len(data[i])):
        dicPredictorProb[i]=[0, 0, 0, 0]

    for i in range(0, len(dicCounts)): #from 0-6
        for j in range(0, len(dicCounts[i])): #from 0-3
            dicPredictorProb[i][j]= dicCounts[i][j] / float(len(data)) #len(data) is 40
    # print (dicPredictorProb)


    # Count of predictor variables co-occurring with 1s in the target variable
    # For each value count it for column2 == 1(fit to fly)
    # For fly(==1), count number of each value (0,1,2,3) in each col(var2-6 total 5)
    dicCondCount = {}
    for j in range(0,len(data[i])):
        if j not in dicCondCount.keys():
            dicCondCount[j]=[0, 0, 0, 0]

    for i in range(0, len(data)):
        for j in range(0,len(data[i])):
            for k in range(0, len(countedNumbers)):
                if data[i][j]== countedNumbers[k] and data[i][1]==1:
                    dicCondCount[j][countedNumbers[k]]+=1
    # print (dicCondCount)

    # Calculate the probability of each predictor variable occurring for Target = Yes/1
    # Probability will be 0's/noofyes, 1's/noofyes, ... 3's/noofyes
    dicCond = {}
    # Create dictionary of zeros
    for j in range(0,len(data[i])):
        dicCond[j]=[0, 0, 0, 0]

    for i in range(0, len(dicCondCount)):
        for j in range(0, len(dicCondCount[i])):
            dicCond[i][j] = dicCondCount[i][j] / float(tyes)
    # print (dicCond)

    # Score each observation using the naive bayes classifier

    global naiveScoreList
    naiveScoreList = [0 for y in range(0, len(data))] #(create 40 observation = 0 in an array)
    for i in range(0, len(data)):
        for j in range(2, len(data[i])):
            if naiveScoreList[i] == 0:
                naiveScoreList[i] = dicCond[j][int(data[i][j])]
                # print ('i is', i, 'j is', j, 'and current score is', naiveScoreList[i])
            else:
                naiveScoreList[i] = naiveScoreList[i] * dicCond[j][int(data[i][j])]
                #                 # print ('j is', j, 'and current score is', naiveScoreList[i])
                # print ('predictor', naiveScoreList[i])
        naiveScoreList[i] = naiveScoreList[i]*dicCond[1][1]*float(tyes/(tyes+tno))
    # print (naiveScoreList)

#Function to plot the ROC
def ROC(list):
    # Create a list with observation number, target value and predicted score
    scoreAndTarget = []
    for i in range(0, len(data)):
        scoreAndTarget.append([data[i][0], data[i][1], list[i]])
    print('CLASSIFICATION RESULTS\n[Instance No., Target, Score]')
    print (scoreAndTarget)
    sortedScore = sorted(scoreAndTarget, key=lambda x: x[2])
    # print (sortedScore)
    # threshold, tpr, fpr
    tprAndFpr = []

    for i in range(0, len(sortedScore)):
        tp = 0
        fp = 0
        for j in range(0, len(sortedScore)):
            # compare with each point above threshold
            if sortedScore[j][2] > sortedScore[i][2]:
                prediction = 1
                # print (i,'threshold is ', sortedScore[i][2], 'score is ', sortedScore[j][2], 'pred is', prediction)
            else:
                prediction = 0
                # print (i, 'threshold is ', sortedScore[i][2], 'score is ', sortedScore[j][2], 'pred is', prediction)
            if prediction and sortedScore[j][1] == 1:
                tp += 1
                # print tp
            if prediction == 1 and sortedScore[j][1] == 0:
                fp += 1
                # print fp
        tprAndFpr.append([sortedScore[i][2], tp / tyes, fp / tno])

    # split up tpr and fpr to plot them
    tpr = []
    fpr = []
    tprFpr = []
    for row in tprAndFpr:
        tpr.append(row[1])
        fpr.append(row[2])
        tprFpr.append(row[1:])

    # Plot roc curve
    # TPR vs FPR
    plt.plot(tpr, fpr, color='r')
    plt.title('ROC Curve for Naive Bayesian Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    # Add another line x=y
    # This is to show random predictibility with 50-50 chance
    x = [0, .5, 1]
    plt.plot(x, x, color='b')

    print('Plotting ROC Curve.......')
    input("Press Enter to continue...")
    plt.show()

def main():

    # Call the Classifier
    # Passing the 'data' in the function as argument
    # Data is nothing but the table/csv file
    NaiveBayesClassifier(data)

    # Call the ROC Curve plot
    ROC(naiveScoreList)

print ('WELCOME TO NAIVE BAYES CLASSIFIER')
print ('Inputting data from CSV.......')

# READ CSV FILE AND REMOVE
dataOriginal = open('C:/Users/sahil/Documents/Business Analytics/Coursework - Fall Term/Data Science 2/Assignment1/Flying_Fitness.csv', 'r').readlines()
data = []
for line in dataOriginal:
	row = line.strip().split(',')
	data.append(row)
# print(data)

# Save column names in a variable
cnames= data[0]
# print (cnames)

# Remove headers by starting from row 1
data = data[1:]
# print (data)

# Convert the strings into FLOAT
datanew = [[0 for x in range(0, len(data[0]))] for y in
           range(0, len(data))]  # Create empty table equal to original data table
for i in range(0, len(data)):
    for j in range(0, len(data[0])):
        datanew[i][j] = float(data[i][j])
data = datanew

print('Following is the data- \n',cnames, data)
input("Press Enter to continue...")

main()

print("!End of Program!")
input("Press Enter to Exit (paradox eh! :p) ")