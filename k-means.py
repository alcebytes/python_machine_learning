import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random as rd
import time

def obter_rodada(rodadas, tipo, valor):
    return [ r for r in rodadas if r[tipo] == valor ]

def remove_primeira_coluna(linha):
    linha = list(linha)
    linha.pop(0)
    return linha
        
def distancia_euclidiana(l1, l2):
    ed = 0
    for t1, t2 in zip(l1, l2):
        ed += (t1-t2) ** 2
    return np.sqrt(ed)

def selecionar_centroide_mais_proximo(linha, centroides):
    distancias_do_centroide = []
    for i,centroide in centroides.iterrows():
        dist = distancia_euclidiana(remove_primeira_coluna(linha), remove_primeira_coluna(centroide))
        distancias_do_centroide.append(dist)
    menor_distancia = distancias_do_centroide.index(min(distancias_do_centroide))
    return centroides.loc[menor_distancia]


# Cada atributo desse data tem 12 atributos (caracteristicas)
data_set = pd.read_csv('agrup_centroides_Q1.csv')

# rodadas onde é guardado o centroide, em qual rodada está e a classe 
rodadas = []

# Não há presença de rótulos, ou seja, classes ou target. Para isso, nossa classe será desconhecida.
# como não temos, a classe será o indice da "linha"
# começa com 3 centroides, as 3 primeiras linhas.
centroides = data_set.loc[0:2]

for i,row in data_set.iterrows():        
    centroide = selecionar_centroide_mais_proximo(remove_primeira_coluna(row), centroides)
    valores_centroide = list(centroide)
    classe = valores_centroide.pop(0)
    rodadas.append({
        "centroide" : valores_centroide,
        "rodada": 1, 
        "classe": classe
    })

   
print(rodadas)
 






