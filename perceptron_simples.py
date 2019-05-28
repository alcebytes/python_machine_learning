
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random as rd
import time

#data_set = pd.read_csv('dermatologia.csv')
data_set = pd.read_csv('dermatology.dat', sep='\s+', header=None, skiprows=1)
CONS_APRENDIZADO = 0.05
PESO_INICIAL = 1
BIAS = -1
Q = 6

def transformar_classes_em_bits(data_set):
    # as classes serão sempre a última coluna
    diferentes_saidas = data_set[data_set.columns[-1]].unique()
    mapa_classes_em_bits = {}
    for saida in diferentes_saidas:
        bits = ''
        for i in range(1, max(diferentes_saidas) + 1):
            if i == saida:
                bits += '1'
            else:
                bits += '0'
            if '1' in bits:
                mapa_classes_em_bits[saida] = bits
    return mapa_classes_em_bits        

def funcao_ativacao(resultado_da_formula):    
    if resultado_da_formula <= 0:
        return 0
    else:
        return 1        

def calcular_saida_neuronio(entradas, pesos):
    # aplica a formula
    resultado = 0
    resultado = BIAS * pesos[0]
    for index, valor in enumerate(entradas):
        resultado += valor * pesos[index]    
    return funcao_ativacao(resultado)         

def atualizar_pesos(pesos, entradas, erro):
    novos_pesos = []
    for index, peso in enumerate(pesos):
        # aplicação da formula w(t+1) = w(t) + n * e(t) * x(t)                
        novos_pesos.append(peso + CONS_APRENDIZADO * erro * entradas[index])
    return novos_pesos

json_classes_em_bit = transformar_classes_em_bits(data_set)
qtd_entradas = len(data_set.iloc[0])

def treinar(data_set_treino):  
    pesos = [1 for i in range(0,qtd_entradas - 1)]
    for i,linha in data_set_treino.iterrows():          
        # o último valor da linha é a saida desejada   
        saida_desejada = linha.pop(len(linha) - 1)       
        saida_desejada_em_bits = json_classes_em_bit[saida_desejada]    
        neuronios = []
        for indice_saida in range(Q):
            saida_neuronio = calcular_saida_neuronio(linha, pesos)
            neuronios.append({
                'neuronio' : indice_saida,
                'saida': saida_neuronio,
                'entrada' : linha,
                'pesos': pesos
            })
            # esse laço é para saber qual neurônio errou (mudou)
        for i, bit_desejado in enumerate(saida_desejada_em_bits):                            
            neuronio = neuronios[i]                
            bit_saida_resultado = neuronio["saida"]            
            if int(bit_desejado) != int(bit_saida_resultado):                
                erro = int(bit_desejado) - int(bit_saida_resultado)
                pesos = neuronio["pesos"]
                pesos = atualizar_pesos(pesos, linha, erro)
    return neuronios

def testar(data_set_teste, neuronios):
    qtd_erros = 0
    for i,linha in data_set_teste.iterrows():                                
        saida_desejada = linha.pop(len(linha) - 1)
        saida_desejada_em_bits = json_classes_em_bit[saida_desejada]            
        for indice_saida in range(Q):
            saida_neuronio = calcular_saida_neuronio(linha, neuronios[indice_saida]["pesos"])
            for i, bit in enumerate(saida_desejada_em_bits):
                bit_saida_resultado = saida_neuronio
                if int(bit) != int(bit_saida_resultado):                
                    qtd_erros += 1
    return qtd_erros
            
QUANTIDADE_RODADAS = 30
incremento_treino_teste = 0.2
percent_treino_inicial = 0.8
percent_teste_inicial = 0.2
percent_treino = percent_treino_inicial
percent_teste = percent_teste_inicial

erros_totais = []
inicio = time.time()
# só irá parar quando a quantidade de testes for igual a quantidade de treino inicial
while percent_teste <= percent_treino_inicial:
        
    dados_treino = { "tam_treino": str(percent_treino * 100) + "%", "tam_teste": str(percent_teste * 100) + "%" }

    erros_por_rodada = []

    print('Inicio das ' + str(QUANTIDADE_RODADAS) + ' rodadas para o dataset com proporção: ' + str(percent_treino * 100) + '/' + str(percent_teste * 100) + " (%)")

    for i in range(0, QUANTIDADE_RODADAS):                

        data_set_treino = data_set.sample(frac=percent_treino, random_state=i*rd.randint(0,100)).reset_index(drop=True)

        data_set_teste = data_set.drop(data_set_treino.index)
        # pega linha por linha do teste para selecionar a melhor classe e verifica se acertou ou n
        num_erros = 0
        # treina os pesos para utilizar nos testes
        neuronios = treinar(data_set_treino)
        
        num_erros = testar(data_set_teste, neuronios)

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


tamanho_treino = [ dados["tam_treino"] for dados in reversed(erros_totais)]
media_erros =  [ dados["erro_media"] for dados in reversed(erros_totais)]

print('Proporção de treinamento: ' + str(tamanho_treino))
print('Média de erros para os treinos: ' + str(media_erros))

plt.scatter([ dados["tam_treino"] for dados in reversed(erros_totais)], media_erros)
plt.figure(1, figsize=(15,5))
plt.xlabel('Treino')
plt.ylabel('Média de erros')
plt.show()
