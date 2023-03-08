#algorithm to find frequent itemsets using level-wise approach
import array as arr
import pandas as pd
from itertools import chain
import itertools

class AprioriAlg:
    #take in initial data and create first itemset
    def __init__(self, item_data:list, transaction_data, min_sup:int):
        self.Item_data = item_data
        self.Item_data.sort()
        self.Transaction_data = transaction_data
        self.Minimum_support = min_sup
        if((self.Item_data == None) or (self.Transaction_data == None) or (self.Minimum_support == 0)):
            return None

    #primary algorithm that will generate the frequent itemsets. 
    def generate_Frequent_itemsets(self):
        freq_itemsets = []
        Item_data = self.Item_data
        Transaction_data = self.Transaction_data
        Minimum_support = self.Minimum_support
        freq_k_itemsets = []
        k = 1

        while True:
            freq_k_itemsets = []
            freq_itemsets = []
            #generate candidates C1, C2,..., CN
            candidate_itemsets = self.generate_candidates(Item_data, k)

            #count each candidate support and ensure it's above min support threshold
            candidate_support = self.count_support(Transaction_data, candidate_itemsets)
            for candidate in candidate_support:
                if candidate_support.get(candidate) >= Minimum_support:
                    freq_k_itemsets.append(candidate)

            if not freq_k_itemsets:#no frequent itemsets this iteration, so we're done
                break
            #add the new itemset to frequent itemsets and update the item data
            freq_itemsets.extend(freq_k_itemsets)
            Item_data = freq_itemsets

            #increment the k variable to create sets of new size k
            k += 1
        supportInfo = dict()
        supportInfo = self.count_support(Transaction_data, Item_data)
        return supportInfo
    
    def generate_candidates(self, item_ds, k):
        candidate_itemset = set()

        #join singleton sets
        if (k == 1):
            for item in item_ds:
                candidate_itemset.add(frozenset({item}))

        #join k > 1 sets
        else:
            for i in range(len(item_ds)):
                 for j in range(i+1, len(item_ds)):
                      if len(item_ds[i] | item_ds[j]) == k:
                           candidate_itemset.add(item_ds[i] | item_ds[j])
        return candidate_itemset
        
        #run through the transaction dataset and count the support of each candidate (ie see if the candidate
        #is a subset of a transaction)
    def count_support(self, transaction_ds, candidate_itemset):
        candidate_support = {}
        for itemset in candidate_itemset:
            support = 0
            for transaction in transaction_ds:
                tr = transaction_ds.get(transaction)
                if itemset.issubset(tr):
                    support += 1
            candidate_support[itemset] = support#keep count of support of each candidate in hashtable
        return candidate_support
    
    def count_support_individual(self, itemset):
        transaction_ds = self.Transaction_data
        support = 0
        for transaction in transaction_ds:
            tr = transaction_ds.get(transaction)
            if itemset.issubset(tr):
                support += 1
        return support    
    
    def association_rules(self, frequent_itemsets, confidence_threshold):
        returnString = []
        for itemset in frequent_itemsets.keys():
            itemsetSuppCnt = self.count_support_individual(itemset)            
            subsets = gen_subsets(itemset)
            for subset in subsets:
                antecedent = frozenset(subset)
                antecedentSuppCnt = self.count_support_individual(antecedent)
                consequent = itemset-antecedent
                confidence = itemsetSuppCnt/antecedentSuppCnt
                if (confidence >= confidence_threshold):
                    print("consequent: [", consequent,"] => Antecedent [",  antecedent, "]: ",int(itemsetSuppCnt/antecedentSuppCnt*100), "%")
       
def frozenset_sort(fset):
    return tuple(sorted(fset))

def gen_subsets(set):
    subsets = []
    for i in range(1, len(set)):
        subsets += itertools.combinations(set, i)
    return subsets

