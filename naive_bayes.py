import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def embaralhar(data_set):
    data_set = data_set.sample(frac=1).reset_index(drop=True)
    return data_set

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

def selecionar_json_melhor_classe(evento, data_set, nome_classe):
    #pega as diferentes classes
    diferentes_classes = data_set[nome_classe].unique()
    #pega o maior da probabilidade de todas as classes    
    probabilidade_por_classe = []
    for classe in diferentes_classes:
        probabilidade_por_classe.append({
            "classe": classe,
            "valor": calcular_probabildiade(data_set, classe, nome_classe, evento)
        })
    # pega o json que tem o maior valor
    return max(probabilidade_por_classe, key = lambda x: x['valor'])
    
def calcular_probabildiade(data_set, valor_classe, nome_classe, evento):
    data_set_filtrada = data_set.loc[data_set[nome_classe] == valor_classe]    
    qtd_classe = int(data_set_filtrada.groupby([nome_classe]).size())    
    frequencia_classe = qtd_classe / len(data_set)
    fqs = []
    for index,atrib in enumerate(evento):
        qtd_por_atributo = len(data_set_filtrada.loc[data_set_filtrada[data_set_filtrada.columns[index]].values == atrib])
        fqs.append(qtd_por_atributo/qtd_classe)
    return np.prod(fqs)


data_set = pd.read_csv('classific_naive_bayes.csv')
INCREMETO_TREINO_TESTE = 0.1

percent_treino_inicial = 0.9
percent_teste_inicial = 0.1
percent_treino = percent_treino_inicial
percent_teste = percent_teste_inicial

# só irá parar quando a quantidade de testes for igual a quantidade de treino inicial
while percent_teste != percent_treino_inicial:
    data_set_treino = selecionar_dados_treino(data_set, percent_treino)
    data_set_teste = selecionar_dados_teste(data_set, percent_treino)
    
    # pega linha por linha do teste para selecionar a melhor classe e verifica se acertou ou n
    num_erros = 0
    for index, linha in data_set_teste.iterrows():
        classe_teste = linha.Target
        #remove o target da linha que é a classe e não deve ser considerado
        del linha["Target"]
        classe_treino = selecionar_json_melhor_classe(linha, data_set_treino, "Target")["classe"]       
        if classe_teste != classe_treino:
            num_erros += 1
        
    percent_teste += INCREMETO_TREINO_TESTE 
    percent_treino += INCREMETO_TREINO_TESTE


    
    
