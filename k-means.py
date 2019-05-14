import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random as rd
import time

# Cada atributo desse data tem 12 atributos (caracteristicas)
data_set = pd.read_csv('agrup_centroides_Q1.csv')

# Não há presença de rótulos, ou seja, classes ou target. Para isso, nossa classe será desconhecida.
# como não temos, a classe será o indice da "linha"
DIMENSAO = 4

def obter_rodada(rodadas, tipo, valor):
    rodadas_rodada = []
    for r in rodadas:
        if r[tipo] == valor:
            rodadas_rodada.append(r)    
    return rodadas_rodada

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
        dist = distancia_euclidiana(linha, remove_primeira_coluna(centroide))
        distancias_do_centroide.append(dist)
    menor_distancia = distancias_do_centroide.index(min(distancias_do_centroide))
    return centroides.loc[menor_distancia]

def atualizar_centroides(rodadas, diferentes_clusters):
    novos_centroides = []
    for i in diferentes_clusters:
        rodadas_filtrando_cluster = obter_rodada(rodadas, "cluster", float(i))
        valores = []
        [valores.append(c["coordenada"]) for c in rodadas_filtrando_cluster]
        centroide_novo = []     
        sum_valores = 0
        for coluna in range(0, DIMENSAO):            
            for linha in range(0, len(valores)):
                sum_valores += valores[linha][coluna]
            centroide_novo.append(sum_valores/len(valores))            
            sum_valores = 0
        novos_centroides.append(centroide_novo) 
    return novos_centroides        

#def valida_houve_modificacao_rodadas(rodadas):

    


# rodadas onde é guardado o centroide, em qual rodada está e a classe 
rodadas = []

# começa com 3 centroides, as 3 primeiras linhas.
centroides = data_set.loc[0:2]

for i in range(0,100):
    for i,row in data_set.iterrows():    
        linha_sem_cluster = remove_primeira_coluna(row)    
        centroide = selecionar_centroide_mais_proximo(linha_sem_cluster, centroides)
        valores_centroide = list(centroide)
        cluster = valores_centroide.pop(0)
        rodadas.append({
            "coordenada" : linha_sem_cluster,
            "rodada": 1, 
            "cluster": cluster
        })
    centroides = atualizar_centroides(rodadas, [1,2,3])