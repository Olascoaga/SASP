#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:18:51 2023

@author: samael
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import scikit_posthocs as sp
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(font="Arial")
sns.set_context("paper", font_scale=1.2)
sns.set_style("white")

# Leer el archivo CSV
df = pd.read_csv("sasp_mean_values.csv", index_col='Description')

# Reestructurar el DataFrame para la prueba de Dunn
data = []
for col in df.columns[0:]:
    data.append(pd.DataFrame({'Group': col, 'Value': df[col].values}))
data = pd.concat(data)

# Realizar la prueba de Kruskal-Wallis
kruskal_result = stats.kruskal(*[df[col] for col in df.columns[1:]])

# Imprimir los resultados de la prueba de Kruskal-Wallis
print("\nResultados de la prueba de Kruskal-Wallis:")
print(kruskal_result)

# Realizar la prueba post-hoc de Dunn
dunn_result = sp.posthoc_dunn(data, group_col='Group', val_col='Value', p_adjust='holm')

# Imprimir los resultados de la prueba de Dunn
print("\nResultados de la prueba de Dunn:")
print(dunn_result)

# Transformar los valores de p utilizando -log10 para manejar valores muy pequeños
log_p_values = -np.log10(dunn_result)

# Crear una máscara para el triángulo superior
mask = np.triu(np.ones_like(log_p_values, dtype=bool))

# Crear una paleta de colores divergente
cmap = sns.diverging_palette(250, 15, s=75, l=40, n=9, center="light", as_cmap=True)

# Dibujar el mapa de calor
sns.heatmap(log_p_values, mask=mask, cmap='coolwarm', 
            square=True, linewidths=.5, cbar_kws={"shrink": 1, "label": "-log10(adj_pval)"})

# Mostrar el gráfico
plt.tight_layout()
plt.savefig('pval.png', dpi=900)
plt.show()
