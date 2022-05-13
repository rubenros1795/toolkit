# Toolkit

This package contains tools for analysing text data in a tabular format. Toolkit provides a simple but effective way to parse text data, clean it and run several robust text analysis methods: frequency analysis, log likelihood distinctiveness and collocation analysis. 

A demonstration of the use of this toolkit can be found in ```demo.ipynb```.

For easy access to paths, edit the ```config.json``` file.

## Installation
Install toolkit by cloning the repo and using pip.

```
git clone https://github.com/rubenros1795/toolkit.git
cd toolkit/src/toolkit
pip -e install setup.py
```

## Requirements

- ```pandas```
- ```numpy```
- ```nltk```
- ```sklearn```
- ```tqdm```

## Documentation

**DataLoader(year_range=(1945,1964), text_column='lemm', data_path='', stopword_path='', pos_path='', load_text=True)**

| NAme          | Type    | Description                                                  |
| ------------- | ------- | ------------------------------------------------------------ |
| year_range    | tuple   | Start year and end year of the period to import. Make sure your text files have year names in them. |
| text_column   | str     | Name of the column with text data.                           |
| data_path     | str     | Path to the folder with the tabular files with text data.    |
| stopword_path | str     | Path to the ```.txt``` (or ```.csv/.tsv```) file with stopwords |
| pos_path      | str     | Path to the ```.json``` file with Part-of-Speech tags linked to individual words. |
| load_text     | boolean | Whether or not to load the text column.                      |

The ````DataLoader``` class provides easy access to data. Run ```DataLoader.load()``` to load the data, and ```DataLoader.clean()```. The data is stored in ```Dataloader.data```.

---

**Frequency(data,text_column,date_column,type_column=None,date_unit='year')**

| name        | type                    | description                                                  |
| ----------- | ----------------------- | ------------------------------------------------------------ |
| data        | pandas.DataFrame object | Dataframe with text data, imported with ```DataLoader.```    |
| text_column | str                     | Name of the column with text data.                           |
| date_column | str                     | Name of the date column                                      |
| type_column | str                     | Name of the column that is used for creating subgroups. In the case of parliamentary debate, this could be "party" or "name". |
| date_unit   | str                     | Type of temporal unit to use. Can be "year", "month", "day", "quarter" or "halfyear" |

The ```Frequency``` class can be used for counting words in tabular text data. Use ```Frequency.get_total_tokens()``` to get the tokens per ```date_unit``` for relative frequency. Count words with ```Frequency.count_words(word='example',relative=True)```. 

---

**Distinctiveness(data,type_column='',text_column='')**

| name        | type                    | description                                                  |
| ----------- | ----------------------- | ------------------------------------------------------------ |
| data        | pandas.DataFrame object | Dataframe with text data, imported with ```DataLoader.```    |
| text_column | str                     | Name of the column with text data.                           |
| type_column | str                     | Name of the column that is used for creating subgroups. In the case of parliamentary debate, this could be "party" or "name". |

The ```Distinctiveness``` class is used to get distinctive words per category. It uses the ```CountVectorizer``` from ```sklearn```. Run ```Distinctiveness.fit_vectorizer()``` to fit frequencies in a matrix. Then get the likelihood scores per word per category by running ```Distinctiveness.get_likelihoods()```.

---

**Collocation(data,text_column='',measure='pmi',window=5,freq_filter=50)**

| name        | type                    | description                                                  |
| ----------- | ----------------------- | ------------------------------------------------------------ |
| data        | pandas.DataFrame object | Dataframe with text data, imported with ```DataLoader.```    |
| text_column | str                     | Name of the column with text data.                           |
| measure     | str                     | Name of the collocation metric to use. Popular metrics are "pmi" and "likelihood_ratio". Others can be found in ```nltk.collocations.BigramAssocMeasures```. |
| window      | int                     | Size of the window in which to look for collocates.          |
| freq_filter | int                     | Co-occurrence frequency threshold, used for filtering out infrequent collocates. |

The ```Collocation``` class can be used to score word collocates. Run ```Collocation.find_collocates()``` to find collocates in the text column of the tabular data. Use ```Collocation.find_term(term='example',direction='all')``` to find collocates to the right, left or all sides of the target word.