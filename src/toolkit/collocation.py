from nltk import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures
import pandas as pd
from glob import glob as gb 
from unidecode import unidecode
import re

class Collocation():

    def __init__(self,data,text_column='',measure='pmi',window=5,freq_filter=50):

        """
        data (list): list of strings.
        measure (str): name of collocation metric, available in nltk.collocations.BigramAssocMeasures.
        window (int): window in which to look for collocates.
        freq_filter (int): lower frequency limit for words to be considered.
        """

        self.data = data 
        self.data = self.data[self.data.lemm_cleaned.str.split(' ').str.len() > 1]
        self.data = [[w for w in t.split(' ') if w not in [' ','','[s]']] for t in self.data[text_column]]
        self.window = window 
        self.freq_filter = freq_filter
        self.measure = eval(f"BigramAssocMeasures.{measure}")
        self.BigramCollocationFinder = BigramCollocationFinder

    def find_collocates(self):
        self.BigramCollocationFinder.default_ws = self.window
        self.finder = self.BigramCollocationFinder.from_documents(self.data)
        self.finder.apply_freq_filter(self.freq_filter)

    def score_collocates(self):
        self.collocation_data = dict(self.finder.score_ngrams(self.measure))

    def find_term(self,term='',direction='all'):
        if direction == 'left':
            return {k:v for k,v in self.collocation_data.items() if k[0] == term}
        elif direction == 'right':
            return {k:v for k,v in self.collocation_data.items() if k[1] == term}
        elif direction == 'all':
            return {k:v for k,v in self.collocation_data.items() if any(term in e for e in k)}
        else:
            pass