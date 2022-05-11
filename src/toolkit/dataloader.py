import re
import json
import numpy as np
import pandas as pd
from glob import glob as gb
from tqdm import tqdm

class DataLoader():
    """
    DataLoader class for loading tabular text data.
    """

    def __init__(self,year_range=(1945,1964),text_column='lemm',data_path='',stopword_path='',load_text=True):
        """
        Initialize class. 

        year_range (tuple): (1945,1989).
        text_column (str): name of the text column, often "pos", "lemm_cleaned" or "or_cleaned".
        data_path (str): path to folder with csv/tsv files containing references to years (e.g. "data-1945-cleaned.tsv").
        stopword_path (str): path to stopword file (.txt or .csv/.tsv).
        load_text (bool): True if text_column should be loaded, False if not.
        """
        self.year_range = year_range
        self.text_column = text_column
        self.data_path = data_path
        self.stopword_path = stopword_path
        self.load_text = load_text 
        self.stopwords = pd.read_csv(stopword_path,header=None).iloc[:,0].tolist()

    def load_pos(self,pos_path=''):
        """
        Load Part-of-Speech Tags
        pos_path (str): path to POS-tagged words in .json format.
        """
        with open(pos_path,'r') as f:
            self.pos_dict = json.load(f)
            self.pos_terms = set(self.pos_dict.keys())

    def load(self,metadata='default'):
        """
        Load data.
        metadata (str/list): 'default' or custom list of metadata columns
        """
        print('\t > loading data ...')
        metadata = ['speech_id','date','role','party-ref','member-ref','speaker'] if metadata == 'default' else metadata 
        columns = [self.text_column] + metadata if self.load_text == True else metadata

        list_files = sorted(gb(self.data_path +'/*'))
        list_files = [f for f in list_files if any(str(y) in f for y in range(self.year_range[0],self.year_range[-1]))]

        data = pd.concat([pd.read_csv(i,sep='\t',usecols=columns) for i in tqdm(list_files)])
        data = data[data[self.text_column].notna()]
        data[self.text_column] = data[self.text_column].astype(str)
        self.data = data

    def clean(self,remove_stopwords=True,pos_types='default'):
        """
        Clean data by removing stopwords and or subsetting parts of speech.
        remove_stopwords (bool): remove stopwords or not.
        pos_types (str/list): keeps all parts of speech when using 'default', or takes input list as basis for selection.
        """
        print('\t > cleaning data ...')
        self.data[self.text_column] = self.data[self.text_column].str.lower()

        if remove_stopwords == False and pos_types == 'all':
            self.data[self.text_column] = self.data[self.text_column]
        
        elif remove_stopwords == True and pos_types == 'all':
            self.data[self.text_column] = [' '.join([w for w in str(t).split(' ') if w not in self.stopwords]) for t in self.data[self.text_column]]
        
        elif remove_stopwords == True and type(pos_types) == list:
            self.data[self.text_column] = [[w for w in str(t).split(' ') if w not in self.stopwords and w in self.pos_terms] for t in self.data[self.text_column]]
            self.data[self.text_column] = [' '.join([w for w in t if self.pos_dict[w] in pos_types]) for t in self.data[self.text_column]]

        elif remove_stopwords == False and type(pos_types) == list:
            self.data[self.text_column] = [[w for w in str(t).split(' ') if w in self.pos_terms] for t in self.data[self.text_column]]
            self.data[self.text_column] = [' '.join([w for w in t if self.pos_dict[w] in pos_types]) for t in self.data[self.text_column]]
        
        elif remove_stopwords == True and pos_types == 'all':
            self.data[self.text_column] = [' '.join([w for w in str(t).split(' ') if w not in self.stopwords]) for t in self.data[self.text_column]]
        else:
            pass

