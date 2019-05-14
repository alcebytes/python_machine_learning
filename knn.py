import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random as rd
import time

data_set = pd.read_csv('iris_data_set.csv')

def distancia_euclidiana(l1, l2):
    ed = 0
    for t1, t2 in zip(l1, l2):
        ed += (t1-t2) ** 2
    return np.sqrt(ed)

def selecionar_dados_treino(data_set, qtd_treino):
     if qtd_treino > 1:
        print("So eh possivel percentual")
        return
     return data_set[0:int(qtd_treino*len(data_set))].reset_index(drop=True)

def selecionar_dados_teste(data_set, qtd_treino):
    if qtd_treino > 1:
        print("So eh possivel percentual")
        return     
    # de teste é todo o restante do de treino
    return data_set[int(qtd_treino*len(data_set)):len(data_set)].reset_index(drop=True)

def selecionar_melhor_classe(data_set, linha_teste):
    distancias = []
    for i,row in enumerate(data_set.values):
        distancias.append(distancia_euclidiana(linha_teste, tuple(row)))    
    menor_distancia_index = distancias.index(min(distancias))
    return data_set.loc[menor_distancia_index]
    
    
QUANTIDADE_RODADAS = 30
incremento_treino_teste = 0.1
percent_treino_inicial = 0.9
percent_teste_inicial = 0.1
percent_treino = percent_treino_inicial
percent_teste = percent_teste_inicial

erros_totais = []
inicio = time.time()
# só irá parar quando a quantidade de testes for igual a quantidade de treino inicial
while percent_teste <= percent_treino_inicial:
        
    dados_treino = { "tam_treino": percent_treino * len(data_set), "tam_teste": percent_teste * len(data_set) }

    erros_por_rodada = []

    print('Inicio das ' + str(QUANTIDADE_RODADAS) + ' rodadas para o dataset com proporção: ' + str(percent_treino * 100) + '/' + str(percent_teste * 100) + " (%)")

    for i in range(0, QUANTIDADE_RODADAS):                
        data_set_treino = data_set.sample(frac=percent_treino, random_state=i*rd.randint(0,100)).reset_index(drop=True)
        data_set_teste = data_set.drop(data_set_treino.index)
        # pega linha por linha do teste para selecionar a melhor classe e verifica se acertou ou n
        num_erros = 0
        for index, linha in data_set_teste.iterrows():                        
            classe_teste = linha.species

            linha_teste = list(linha)
        # remove o valor da species, pois não é necessário para calcular a distância euclidiana
            linha_teste.pop()
            classe_treino = selecionar_melhor_classe(data_set_treino, tuple(linha_teste))["species"]       
            if classe_teste != classe_treino:
                num_erros += 1
        erros_por_rodada.append(num_erros)

    dados_treino["erro_media"] = round(np.mean(erros_por_rodada), 3)
    dados_treino["erro_max"] = np.max(erros_por_rodada)
    dados_treino["erro_min"] = np.min(erros_por_rodada)
    
    erros_totais.append(dados_treino)

    percent_teste += incremento_treino_teste
    percent_teste = round(percent_teste, 2)
    percent_treino -= incremento_treino_teste
    percent_treino = round(percent_treino, 2)   

fim = time.time()

tempo_execucao_minutos = round(((fim - inicio) / 60), 1)
print("Tempo de execução: " + str(tempo_execucao_minutos) + " minutos")
print('Abaixo o JSON que contempla as proporções e média de erros para cada.')
print(erros_totais)


tamanho_treino = [ str(np.round(dados,1) * 100) + "%" for dados in np.arange(0.1,1, 0.1)]
media_erros =  [ dados["erro_media"] for dados in reversed(erros_totais)]

print('Proporções treino/teste do conjunto de dados: ' + str(tamanho_treino))
print('Média de erros para os treinos: ' + str(media_erros))
plt.scatter(tamanho_treino, media_erros)
plt.figure(1, figsize=(15,5))
plt.xlabel('Tamanho do treino em %')
plt.ylabel('Média de erros')
plt.show()