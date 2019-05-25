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
    return centroides.loc[menor_distancia_index],cluster, min(distancias_do_centroide)

def atualizar_centroides(rodadas, diferentes_clusters, centroides):
    novos_centroides = []
    for i in diferentes_clusters:
        rodadas_filtrando_cluster = obter_rodada(rodadas, "cluster", float(i))
        valores = []
        [valores.append(c["coordenada"]) for c in rodadas_filtrando_cluster]
        centroide_novo = []     
        sum_valores = 0    
        if valores != []:
            for coluna in range(0, DIMENSAO):            
                for linha in range(0, len(valores)):
                    sum_valores += valores[linha][coluna]                            
                centroide_novo.append(sum_valores/len(valores))            
                sum_valores = 0
            novos_centroides.append(centroide_novo)                 
        else:
            [centroide_novo.append(c) for c in centroides.loc[i-1]]
            novos_centroides.append(centroide_novo)

    return pd.DataFrame(novos_centroides)        

  
# CRIAR MÉTODO PARA VALIDAR SE NA RODADA NOVA NÃO MUDOU NADA EM RELAÇÃO A ANTERIOR...  

def verifica_nova_rodada_mudou(numero_rodada_corrente, execucoes):
  if execucoes == [] or numero_rodada_corrente == 1:
      return True
  execucoes_da_ultima_rodada = [execucao for execucao in execucoes if execucao["rodada"] == numero_rodada_corrente - 1]
  execucoes_da_nova_rodada = [execucao for execucao in execucoes if execucao["rodada"] == numero_rodada_corrente]
  for i in range(1, DIMENSAO + 1):
    rodadas_filtrando_cluster_anterior = obter_rodada(execucoes_da_ultima_rodada, "cluster", float(i))
    rodadas_filtrando_cluster_nova = obter_rodada(execucoes_da_nova_rodada, "cluster", float(i))
    for j in range(len(rodadas_filtrando_cluster_anterior)):
      if rodadas_filtrando_cluster_anterior[j]["coordenada"].equals(rodadas_filtrando_cluster_nova[j]["coordenada"]) == False:
        return True      
  return False  
    
def obter_media_distancias(numero_rodada, execucoes, tam_data_set):
    execucoes_filtradas = [execucao for execucao in execucoes if execucao["rodada"] == numero_rodada]
    sum_distancias = 0
    for execu in execucoes_filtradas:
        sum_distancias += execu["distancia_do_centroide"]
    return sum_distancias/tam_data_set
    
    

# rodadas onde é guardado o centroide, em qual rodada está e a classe 
execucoes = []
data_set = pd.read_csv('agrupamento.dat', sep='\s+', header=None, skiprows=1)
todos_centroides = pd.read_csv('centroides.dat', sep='\s+', header=None, skiprows=1)
numero_rodada_corrente = 1
eibow = []

#começa com 2
centroides_iniciais = todos_centroides.loc[:1]

for indice_centroide in range(len(centroides_iniciais) - 1, len(todos_centroides)):
    
    if indice_centroide >= 2:
      centroides_iniciais = centroides_iniciais.append(todos_centroides.loc[indice_centroide])
      centroides = centroides_iniciais
    else:
      centroides = centroides_iniciais

    clusters = np.array(range(1, len(centroides) + 1))    
    
    print("executando com " + str(len(centroides)) + " centroides..")
    
    while True:
        for i,row in data_set.iterrows():                        
            centroide, cluster, distancia = selecionar_centroide_mais_proximo(row, centroides)        
            execucoes.append({
                "coordenada" : row,
                "distancia_do_centroide": distancia, 
                "rodada": numero_rodada_corrente, 
                "cluster": cluster
            })
        centroides = atualizar_centroides(execucoes, clusters, centroides)    
        # se não mudar mais nada, é pq deve parar o loop pois não há mais o que fazer..
        if verifica_nova_rodada_mudou(numero_rodada_corrente, execucoes) == False:
            print("execução com " + str(len(centroides)) + " centroides estabilizado na rodada " + str(numero_rodada_corrente) + "!")
            eibow.append({
                "media_distancias": obter_media_distancias(numero_rodada_corrente, execucoes, len(data_set)),               
                "quantidade_centroides": len(centroides)
            })
            execucoes = []
            numero_rodada_corrente = 1
            #print(eibow)
            break
        else:
            numero_rodada_corrente += 1

media = [ dados["media_distancias"] for dados in eibow]
qtd_centroides = [dados["quantidade_centroides"] for dados in eibow]
plt.scatter(media, qtd_centroides)
plt.figure(1, figsize=(15,5))
plt.xlabel('Variância')
plt.ylabel('Quantidade de centroides')
plt.show()
print(eibow)
#plot dos gráficos    