import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random as rd
import time

data_set = pd.read_csv('dermatologia.csv')
CONS_APRENDIZADO = 0.05
PESO_INICIAL = 1
BIAS = -1
Q = 6

def transformar_classes_em_bits(data_setl):
    diferentes_saidas = data_set["Target"].unique()
    mapa_classes_em_bits = {}
    for saida in diferentes_saidas:
        bits = ''
        for i in range(0, max(diferentes_saidas)):
            if i == saida:
                bits += '1'
            else:
                bits += '0'
        mapa_classes_em_bits[saida] = bits
    return mapa_classes_em_bits        

# def transformar_saida_em_bit(data_set, decimal):
#     diferentes_saidas = data_set["Target"].unique()
#     bits = ''
#     for i in range(0, max(saidas_decimal)):
#         if i == saidas_decimal[i]:
#             bits += '1'
#         else:
#             bits += '0'
#     return bits        

def funcao_ativacao(resultado_da_formula):    
    if resultado_da_formula <= 0:
        return 0
    elif:
        return 1        

# entrada -> linha do data set
def neuronio(entradas, pesos):
    # aplica a formula
    resultado = 0
    resultado = BIAS * pesos[0]
    for index, valor in enumerate(linha):
        resultado += valor * peso[index]    
    return funcao_ativacao(resultado)         

def atualizar_peso(pesos, entradas, erro):
    novos_pesos = []
    for index, peso in enumerate(pesos):
        novos_pesos.append(peso + erro * entradas[index])
    return novos_pesos

# SE ERRO FOR NEGATIVO, O PESO EU INCREMENTO, SE FOR POSITIVO DECREMENTO
pesos = []
json_classes_em_bit = transformar_classes_em_bits(data_set)

def treinar(data_set_treino):
    for i in len(data_set_treino.iloc[0] - 1):
        pesos.append(PESO_INICIAL)
    pesos = [1 for i in len(entradas)]
    for i,linha in data_set_treino.iterrows():                        
        # o último valor da linha é a saida desejada
        saida_desejada = entradas.pop(-1)
        saida_desejada_em_bits = json_classes_em_bit[saida_desejada]    
        neuronios = {}
        for indice_saida in range(Q):
            saida_neuronio = str(neuronio(linha, pesos))
            neuronios.append({
                'neuronio' : indice_saida,
                'saida': saida_neuronio
                'entrada' : linha,
                'pesos': pesos
            })
            # esse laço é para saber qual neurônio mudou
            for i, bit in enumerate(saida_desejada_em_bits):
                neuronio = neuronios.get(i)
                bit_saida_resultado = neuronio["saida"]
                if bit_desejado != bit_saida_resultado:
                    erro = bit_desejado - bit_saida_resultado
                    pesos = neuronio["pesos"]
                    pesos = atualizar_pesos(pesos, linha, erro)
    return neuronios

def testar(data_set_teste, neuronios):
    qtd_erros = 0
    for i,linha in data_set_teste.iterrows():                                
        saida_desejada = entradas.pop(-1)
        saida_desejada_em_bits = transformar_saida_em_bit(saida_desejada)            
        for indice_saida in range(QTD_CLASSES):
            saida_neuronio = str(neuronio(linha, peso))
            for i, bit in enumerate(saida_desejada_em_bits):
                bit_saida_resultado = neuronios.get(i)["saida"]
                if bit != bit_saida_resultado:
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
        
    dados_treino = { "tam_treino": percent_treino * len(data_set), "tam_teste": percent_teste * len(data_set) }

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



            
    
# for i,linha in data_set.iterrows():                        
#     resultado = 0
#     classe = linha.pop(-1)
#     resultado = BIAS * linha.iloc[0]
#     del linha[0]
#     for valor in linha:
#         resultado += valor * peso
#     resultado += resultado * CONS_APRENDIZADO
#     erro = classe - resultado
#     if abs(erro) > TAXA_ERRO and erro < 0:
#         peso += INCREMENTO_DECREMENTO_PESO    
#     elif abs(erro) > TAXA_ERRO and erro > 0:
#         peso -= INCREMENTO_DECREMENTO_PESO    
#     taxas_erros.append(erro)
    

# definir um valor para multiplicar por cada 
print(data_set)

