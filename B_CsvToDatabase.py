import csv
import sqlite3


'''
Python Code to read any csv file 
Note- The csv file should have the first row as the column names (as in example of FlyingFitness.csv)
If the column names are missing, another row should be manually added to the csv using editor

PROCESS-
1.Read in file normally and define some variables such as column length
2.Use SQL to dynamically create Columns in a table based on the previous count
3.Dynamically create placeholders to insert the values from the data(csv file)

'''

#Inputting data normally
dataOriginal = open('C:/Users/sahil/Documents/Business Analytics/Coursework - Fall Term/Data Science 2/Assignment1/Flying_Fitness.csv', 'r').readlines()
data = []
for line in dataOriginal:
	row = line.strip().split(',')
	data.append(row)

#Change list to tuple
#Because sql ONLY TAKES Tuple as a parameter
#This tuple has all the column names i.e the first row of any csv
tupcols=tuple(data[0])


#SQL CODE BEGINS
print('Database name is Project')
conn = sqlite3.connect('Project.db')
c = conn.cursor()

#TO delete the table if the table already exists
c.execute('DROP TABLE CSVTabular')

print('Table name is CSVTabular')
#Create table based on the columns names in the first row of csv file
c.execute('''CREATE TABLE CSVTabular {}'''.format(tuple(data[0])))

#Function to define place holders
#This will be required when we are inputting values in the SQL database
def place_holder(values):
    return '({})'.format(', '.join('?' * len(values)))
ph = place_holder(data[0])

#To input the actual values in the data from the csv
with open('C:/Users/sahil/Documents/Business Analytics/Coursework - Fall Term/Data Science 2/Assignment1/Flying_Fitness.csv', newline='\n') as f:
    csv_data = csv.reader(f, delimiter=',', quotechar='"')
    for row in csv_data:
        c.execute('INSERT INTO CSVTabular values {}'.format(ph), tuple(row))

#Print the values in the SQL Table
input("Press Enter to Print Table...")
c.execute('SELECT * from CSVTabular')
print(*c.fetchall(), sep='\n')

input("Press Enter to Exit (paradox eh! :p) ")

conn.commit()
conn.close()
