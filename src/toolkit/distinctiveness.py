# Code for calculating log likelihood distinctiveness. 
# Created by Ruben Ros, adopted from code by Jo Guldi.


import re
import numpy as np
import pandas as pd
from nltk import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures
from sklearn.feature_extraction.text import CountVectorizer

class Distinctiveness():
    """
    Class for calculating log likelihood distinctiveness for text data.
    """

    def __init__(self,data,type_column='',text_column=''):
        """
        data (pd.data): data with text data and metadata.
        type_column (str): column that indicates the group for which distinctive terms should be calculated.
        text_column (str): column with text.
        """
        self.type_column = type_column
        self.text_column = text_column

        if len(data[type_column]) != len(data[type_column].unique()):
            self.data = data[[type_column,text_column]].groupby([type_column]).agg({text_column: lambda x: " ".join(x)}).reset_index()
        else:
            self.data = data

    def fit_vectorizer(self,max_features=10000,ngram_range=(1,1)):
        """
        Create a CountVectorizer object.
        max_features (int): max. number of word features to use
        ngram_range (tuple): range of ngrams to use, default is (1,1), can be (1,2) and up.
        """
        print('\t > fitting word counts in CountVectorizer ...')

        self.vectorizer = CountVectorizer(
            max_features=max_features, 
            lowercase=True, 
            ngram_range=ngram_range
            )
        self.vectorized = self.vectorizer.fit_transform(self.data[self.text_column].tolist())
        self.all_words = np.array(self.vectorizer.get_feature_names())
        self.type_names = self.data[self.type_column].tolist()
        self.vecdf = pd.data(self.vectorized.todense(), # the matrix we saw above is turned into a data
                                 columns=self.all_words,
                                 index =self.type_names
                                 )  
        self.type_words_total = self.vecdf.sum(axis=1)
        self.word_total = self.vecdf.sum(axis=0) 
        self.total_corpus_words = sum(self.word_total)   

    def get_likelihoods(self):
        print('\t > calculating word-level log likelihood scores ...')
        lls = []

        for type_id,type_ in enumerate(self.type_names):
            loglikely = []
            for word_id in self.vectorized[type_id].indices:
                a = self.vecdf.iat[type_id, word_id] #  word in type
                b = self.word_total[word_id] - a  # # word in remaining types
                c = self.type_words_total[type_id] - a #  not word in type
                d = self.total_corpus_words - a - b - c # not word in remaining types
                E1 = (a + c) * (a + b) / self.total_corpus_words  
                E2 = (b + d) * (a + b) / self.total_corpus_words 
                LL = 2 * (a * np.log(a / E1)) # the log likelihood equation
                if (b > 0):
                    LL += 2 * b * np.log(b / E2)
                loglikely.append((LL, self.all_words[word_id])) # add the log likelihood score to the end of a new data

            loglikely = sorted(loglikely, reverse=True) # the loop hits this every time it cycles through all the words in one speaker. 
            lls.append(loglikely) # add on another speaker
        self.lls_df = pd.data()
        for c,i in enumerate(lls):
            i = pd.data(i)
            i['type'] = self.type_names[c]
            self.lls_df = self.lls_df.append(i)