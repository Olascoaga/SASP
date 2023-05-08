# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 22:14:14 2023

@author: olask
"""

import pandas as pd

samples = pd.read_csv('SampleAttributes.csv')
with open("sample_exclusion.txt", "r") as exclusion_file:
    exclusion = exclusion_file.readlines()
    exclusion = list(map(lambda s: s.strip(), exclusion))

samples = samples[samples['SMTSD'].isin(exclusion)]
samples = samples[samples['GROUP'] == 'E']
use_samples = samples['SAMPID'].tolist()
use_samples.insert(0, 'Description')


df = pd.read_csv("GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.gct",
                 sep='\t',
                 skiprows=2,
                 usecols=use_samples)