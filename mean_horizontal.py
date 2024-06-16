#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:48:29 2023

@author: samael
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import shapiro

sns.set(font="Arial")
sns.set_context("paper", font_scale=1.5)
sns.set_style("white")

# Leer el archivo CSV
df = pd.read_csv("sasp_mean_values.csv", index_col='Description')

# Calcular el log10 de los valores
log10_df = df.iloc[:, 0:].applymap(lambda x: np.log10(x + 1))

# Realizar la prueba de Shapiro-Wilk para cada columna
normality_report = {}
for column in log10_df.columns:
    stat, p_value = shapiro(log10_df[column])
    normality_report[column] = {
        'p_value': p_value,
        'passed': p_value > 0.05  # Consideramos p > 0.05 como paso de la prueba de normalidad
    }

# Crear un DataFrame con el reporte de normalidad
normality_df = pd.DataFrame(normality_report).T

# Imprimir el reporte de normalidad
print("Normality Test Report (Shapiro-Wilk):")
print(normality_df)

# Calcular las medias y el error estándar de la media (SEM)
mean_df = log10_df.mean(axis=0)
sem_df = log10_df.sem(axis=0)

# Crear un DataFrame con las medias y el SEM
result_df = pd.DataFrame({'Mean': mean_df, 'SEM': sem_df})

# Dibujar el gráfico de dispersión con líneas verticales para el SEM
fig, ax = plt.subplots(figsize=(10, 8), dpi=900)

# Crear líneas verticales para el SEM
for i, (mean, sem) in enumerate(zip(result_df["Mean"], result_df["SEM"])):
    ax.vlines(x=i, ymin=mean - sem, ymax=mean + sem, color='grey', lw=1.5)
    ax.plot([i-0.1, i+0.1], [mean - sem]*2, color='grey', lw=1.5)  # Agregar barras de error inferior
    ax.plot([i-0.1, i+0.1], [mean + sem]*2, color='grey', lw=1.5)  # Agregar barras de error superior

# Dibujar círculos para las medias
colors = cm.rainbow(np.linspace(0, 1, len(result_df)))
for i in range(len(result_df)):
    ax.scatter(i, result_df['Mean'].iloc[i], color='gray', s=100)

# Ajustes al eje X
plt.xticks(rotation=90)
plt.xticks([i for i in range(len(result_df.index))], [name.replace('.tsv', '') for name in result_df.index])
plt.ylabel('log10(TPM + 1)')
plt.title("SASP mean expression")

# Ajustar los márgenes para evitar que las etiquetas se corten
plt.tight_layout()

# Guardar la figura
plt.savefig('mean_expression.png', dpi=900)
plt.show()
