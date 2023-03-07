import Apriori
import pandas as pd
import sys
from itertools import chain
from mlxtend.frequent_patterns import association_rules

freqItemsets = None
attRange = chain(range(0,7), range(301, 131667))
id_range = range(0,301)
transaction_data = {}
item_data = []

try:
    print("\nReading in and splitting adult.csv...")
    attribute_data = pd.read_csv('anonymous-msweb.csv', skiprows=[i for i in attRange], header=None)
    identification_data = pd.read_csv('anonymous-msweb.csv', skiprows=[i for i in id_range], header=None)

    #organize identification data into transactions
    #structure of transaction_data: {transaction id:
    #               [
    #                list of attributes (ie items)
    #               ]
    i = 0
    while i in range(0, len(identification_data)): 
        char = identification_data[0][i]
        counter = 0
        if char == 'C':
            transaction_data[identification_data[1][i]] = set()    
            i += 1
            counter += 1
            char = 'V'  
            while (char == 'V') and (i < len(identification_data)):
                transaction = identification_data[1][i]
                transaction_data[identification_data[1][i-counter]].add(transaction)
                i += 1
                counter += 1   
                if i < len(identification_data):
                    char = identification_data[0][i]

    #pass in the item data (ie attributes)
    for data in attribute_data[1]:
        item_data.append(data)
    
    print("\nRunning Apriori Algorithm on it to return frequent itemsets:\n")

    ap = Apriori.AprioriAlg(item_data, transaction_data, 500)#init the algorithm class with the data
    if ap is not None:
        freqItemsets = ap.generate_Frequent_itemsets()#call the primary alg method
        print("Frequent itemsets:")
        print(freqItemsets,"\n")
        print("Associations:")
        ap.association_rules(freqItemsets, .7)
    else:
        print("\nError initializing class for algorithm.")
except FileNotFoundError as ex:
    print("\nFile not found, error:" + ex)
    sys.exit()

    