import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random as rd
import time

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
        dist = distancia_euclidiana(linha, centroide)
        distancias_do_centroide.append(dist)
    menor_distancia_index = distancias_do_centroide.index(min(distancias_do_centroide))
    # mais 1 pois o cluster não pode ser zero
    cluster = (menor_distancia_index) + 1
    return centroides.loc[menor_distancia_index],cluster

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
    return pd.DataFrame(novos_centroides)        

  
# CRIAR MÉTODO PARA VALIDAR SE NA RODADA NOVA NÃO MUDOU NADA EM RELAÇÃO A ANTERIOR...  

def verifica_nova_rodada_mudou(numero_rodada_corrente, execucoes):
  if execucoes == [] or numero_rodada_corrente == 1:
      return True
  execucoes_da_ultima_rodada = [execucao for execucao in execucoes if execucao["rodada"] == numero_rodada_corrente - 1]
  execucoes_da_nova_rodada = [execucao for execucao in execucoes if execucao["rodada"] == numero_rodada_corrente]
  for i in range(DIMENSAO):
    rodadas_filtrando_cluster_anterior = obter_rodada(execucoes_da_ultima_rodada, "cluster", float(i))
    rodadas_filtrando_cluster_nova = obter_rodada(execucoes_da_nova_rodada, "cluster", float(i))
    del rodadas_filtrando_cluster_anterior["rodada"]
    del rodadas_filtrando_cluster_nova["rodada"]
    for i in range(rodadas_filtrando_cluster_anterior):
      if(rodadas_filtrando_cluster_anterior[i]["coordenada"] != rodadas_filtrando_cluster_anterior[i]["coordenada"]):
        return True      
  return False  
    
    
# rodadas onde é guardado o centroide, em qual rodada está e a classe 
execucoes = []

agrupamentos = pd.read_csv('agrupamento.dat', sep='\s+', header=None, skiprows=1)

centroides = pd.read_csv('centroides.dat', sep='\s+', header=None, skiprows=1)

data_set = pd.concat([centroides,agrupamentos])

clusters = np.array(range(1, len(centroides) + 1))

numero_rodada_corrente = 1

while True:
    for i,row in data_set.iterrows():            
        print('executando rodada...' + str(numero_rodada_corrente))
        centroide, cluster = selecionar_centroide_mais_proximo(row, centroides)
        execucoes.append({
            "coordenada" : row,
            "rodada": numero_rodada_corrente, 
            "cluster": cluster
        })
    centroides = atualizar_centroides(execucoes, clusters)    
    # se não mudar mais nada, é pq deve parar o loop pois não há mais o que fazer..
    if verifica_nova_rodada_mudou(numero_rodada_corrente, execucoes) == False:
        break
    else:
        numero_rodada_corrente += 1


#plot dos gráficos    