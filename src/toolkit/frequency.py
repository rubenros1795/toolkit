from collections import Counter 
import pandas as pd

class Frequency():
    """
    Frequency class for aggregating and n-gram frequencies.
    """

    def __init__(self,dataframe,text_column,date_column,type_column=None,date_unit='year'):
        """
        dataframe (pd.Dataframe): dataframe with text data
        text_column (str): name of text column
        date_column (str): name of date column
        type_column (Nonetype or str): metadata column used for creating distributions over groups (for example 'party-ref')
        date_unit = (str): 'year','month','day','quarter','halfyear'
        """
        self.dataframe = dataframe
        self.text_column = text_column
        self.date_column = date_column
        self.type_column = type_column
        self.date_unit = date_unit

        self.dataframe[date_column] = pd.to_datetime(self.dataframe[date_column],infer_datetime_format=True)
        if self.date_unit == 'year':
            self.dataframe[date_column] = self.dataframe[date_column].dt.strftime('%Y')
        if self.date_unit == 'month':
            self.dataframe[date_column] = self.dataframe[date_column].dt.strftime('%Y-%m')
        if self.date_unit == 'day':
            self.dataframe[date_column] = self.dataframe[date_column].dt.strftime('%Y-%m-%d')
        if self.date_unit == 'quarter':
            self.dataframe[date_column] = self.dataframe[date_column].dt.strftime('%Y-%q')
        if self.date_unit == 'halfyear':
            self.dataframe[date_column] = [f'{x.year}-{1 if x.quarter < 3 else 2}' for x in self.dataframe[date_column]]

        columns = [self.text_column,self.date_column] if self.type_column == None else [self.text_column,self.date_column,self.type_column]

        self.dataframe = (self.dataframe.groupby([c for c in columns if c != self.text_column]) 
                                       .agg({self.text_column: lambda x: " ".join(x)})
                                       .reset_index())
    def get_total_tokens(self):
        self.dataframe['total_tokens'] = self.dataframe[self.text_column].str.split(' ').str.len()

    def count_word(self,word,relative=True):
        self.dataframe[f'n_{word}'] = self.dataframe[self.text_column].str.count(f' {word} ')
        if relative == True:
            assert 'total_tokens' in self.dataframe.columns
            self.dataframe[f'n_{word}'] = self.dataframe[f'n_{word}'] / self.dataframe['total_tokens']