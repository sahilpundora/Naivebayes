import matplotlib.pyplot as plt
import csv
import sqlite3

''' 
Data is imported from CSV File 
Data is stored in Database as a Table
Data is extracted from the database
Naive bayes classifier to determine whether a pilot is fit to fly a plane
ROC is Plotted
'''

# Function to calculate NavieBayes
def NaiveBayesClassifier(data):
    print('Classifying the data based on Naive Bayes theorem\n', 'TestRes/Var1 is the Target Variable\n',
          'Var 2-to-6 are Independent Variables (Features of the dataset)')
    global tyes
    global tno
    tyes=0
    tno=0
    for i in range(0, len(data)):
        if data[i][1]==1:
            tyes+=1
        else:
            tno+=1

    dicCounts = {}
    for i in range(0,len(data[0])):
        dicCounts[i]=[0,0,0,0]

    countedNumbers = [0,1,2,3]

    dicCondCount = {}
    for j in range(0,len(data[i])):
        if j not in dicCondCount.keys():
            dicCondCount[j]=[0, 0, 0, 0]

    for i in range(0, len(data)):
        for j in range(0,len(data[i])):
            for k in range(0, len(countedNumbers)):
                if data[i][j]== countedNumbers[k] and data[i][1]==1:
                    dicCondCount[j][countedNumbers[k]]+=1
    dicCond = {}
    for j in range(0,len(data[i])):
        dicCond[j]=[0, 0, 0, 0]

    for i in range(0, len(dicCondCount)):
        for j in range(0, len(dicCondCount[i])):
            dicCond[i][j] = dicCondCount[i][j] / float(tyes)

    global naiveScoreList
    naiveScoreList = [0 for y in range(0, len(data))]
    for i in range(0, len(data)):
        for j in range(2, len(data[i])):
            if naiveScoreList[i] == 0:
                naiveScoreList[i] = dicCond[j][int(data[i][j])]
            else:
                naiveScoreList[i] = naiveScoreList[i] * dicCond[j][int(data[i][j])]
        naiveScoreList[i] = naiveScoreList[i]*dicCond[1][1]*float(tyes/(tyes+tno))

#Function to plot the ROC
def ROC(list):
    # Create a list with observation number, target value and predicted score
    scoreAndTarget = []
    for i in range(0, len(data)):
        scoreAndTarget.append([data[i][0], data[i][1], list[i]])
    print('CLASSIFICATION RESULTS\n[Instance No., Target, Score]')
    print(scoreAndTarget)
    sortedScore = sorted(scoreAndTarget, key=lambda x: x[2])

    tprAndFpr = []
    for i in range(0, len(sortedScore)):
        tp = 0
        fp = 0
        for j in range(0, len(sortedScore)):
            if sortedScore[j][2] > sortedScore[i][2]:
                prediction = 1
            else:
                prediction = 0
            if prediction and sortedScore[j][1] == 1:
                tp += 1
            if prediction == 1 and sortedScore[j][1] == 0:
                fp += 1
        tprAndFpr.append([sortedScore[i][2], tp / tyes, fp / tno])

    tpr = []
    fpr = []
    tprFpr = []
    for row in tprAndFpr:
        tpr.append(row[1])
        fpr.append(row[2])
        tprFpr.append(row[1:])

    # Plot roc curve
    plt.plot(tpr, fpr, color='r')
    plt.title('ROC Curve for Naive Bayesian Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    x = [0, .5, 1]
    plt.plot(x, x, color='b')

    print('Plotting ROC Curve.......')
    input("Press Enter to continue...")
    plt.show()

def main():

    NaiveBayesClassifier(data)
    ROC(naiveScoreList)

print ('WELCOME TO NAIVE BAYES CLASSIFIER')
print ('Inputting data from CSV.......')

# READ CSV FILE AND REMOVE
dataOriginal = open('C:/Users/sahil/Documents/Business Analytics/Coursework - Fall Term/Data Science 2/Assignment1/Flying_Fitness.csv', 'r').readlines()
data = []
for line in dataOriginal:
	row = line.strip().split(',')
	data.append(row)



print('Creating Table and storing in the DataBase.....')
#SQL CODE BEGINS
conn = sqlite3.connect('Project.db')
c = conn.cursor()

#TO delete the table if the table already exists
# c.execute('DROP TABLE CSVTabular')

c.execute('''CREATE TABLE CSVTabular {}'''.format(tuple(data[0])))

tupcols=tuple(data[0])
def place_holder(values):
    return '({})'.format(', '.join('?' * len(values)))
ph = place_holder(data[0])

# To input the actual values in the data from the csv
with open('C:/Users/sahil/Documents/Business Analytics/Coursework - Fall Term/Data Science 2/Assignment1/Flying_Fitness.csv', newline='\n') as f:
    csv_data = csv.reader(f, delimiter=',', quotechar='"')
    for row in csv_data:
        c.execute('INSERT INTO CSVTabular values {}'.format(ph), tuple(row))

c.execute('SELECT * from CSVTabular')
datacsv=c.fetchall()
datacsv = [list(i) for i in datacsv]

conn.commit()
conn.close()

# store col names in cnames
cnames= datacsv[0]

# remove the first line from data i.e. column headers
datacsv = datacsv[1:]

#convert string of data to integers
for i in range(len(datacsv)):
    for j in range(0, len(datacsv[i])):
        datacsv[i][j] = int(datacsv[i][j])
data=datacsv

print('Following is the data- \n',cnames, data)
input("Press Enter to continue...")

#Call Main
main()

print("!End of Program!")
input("Press Enter to Exit (paradox eh! :p) ")


