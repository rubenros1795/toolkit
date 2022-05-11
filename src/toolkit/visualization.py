import matplotlib.pyplot as plt
import seaborn as sns

class Style():
    def __init__(self):
        pass

    def set_default(self):
        sns.set_style('white')
        sns.set_style({'font.family':'Inter'})
        sns.set_palette('tab20b')
