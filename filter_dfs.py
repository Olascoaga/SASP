#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 21:09:38 2023

@author: samael
"""

import pandas as pd

samples = pd.read_csv('SampleAttributes.csv')
with open("sample_exclusion.txt", "r") as exclusion_file:
    exclusion = exclusion_file.readlines()
    exclusion = list(map(lambda s: s.strip(), exclusion))

samples = samples[samples['SMTSD'].isin(exclusion)]
samples = samples[samples['GROUP'] == 'E']

df = pd.read_csv('brain.csv')

# Crear un diccionario con los SAMPID como llave y la región como valor
sampid_to_region = {row['SAMPID']: row['SMTSD'].replace('Brain - ', '') for _, row in samples.iterrows()}

# Filtrar las columnas en el dataframe df que correspondan a los SAMPID en samples
filtered_columns = [col for col in df.columns if col in sampid_to_region.keys()]

# Crear un dataframe solo con las columnas filtradas y la columna 'Description'
filtered_df = df[['Description'] + filtered_columns]

# Agrupar las columnas por región
region_to_columns = {}
for col in filtered_columns:
    region = sampid_to_region[col]
    if region in region_to_columns:
        region_to_columns[region].append(col)
    else:
        region_to_columns[region] = [col]

# Guardar las muestras que correspondan a la misma región en el mismo archivo TSV
for region, columns in region_to_columns.items():
    file_name = f"{region}.tsv"
    filtered_df[['Description'] + columns].to_csv(file_name, sep='\t', index=False)
