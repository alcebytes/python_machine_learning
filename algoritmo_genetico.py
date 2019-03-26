import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import random as rd
import matplotlib.animation as animation

coordinates_x = np.array(open("coordenadasx.dat").read().split("\n"), dtype=int)
coordinates_y = np.array(open("coordenadasy.dat").read().split("\n"), dtype=int) 
qtd_cidades = len(coordinates_x)

all_coordinates_table = pd.DataFrame()

for row in range(0, len(coordinates_x)): 
    all_coordinates_row = pd.DataFrame({'x': coordinates_x[row], 'y': coordinates_y[row]}, index = [row])
    all_coordinates_table = all_coordinates_table.append(all_coordinates_row)

# Criação das colunas do tamanho das coordenadas
dists = pd.DataFrame(columns=range(0, len(coordinates_x)))

# Data frame das distâncias calculando de todas as cidades
for i in range(0,  len(coordinates_x)):
    for j in range(0,  len(coordinates_y)):
        dists.loc[i, j] = math.sqrt(pow(all_coordinates_table.loc[i, 'x'] - all_coordinates_table.loc[j, 'x'], 2) +
                                    pow(all_coordinates_table.loc[i, 'y'] - all_coordinates_table.loc[j, 'y'], 2))


#OK
def selecionar_individuo_aleatorio(tamanho_total):
    return rd.sample(range(0, tamanho_total), tamanho_total)    

#OK
def formar_pares_aleatorios(populacao):
    pares_1 = []
    pares_2 = []
    qtdPares = int(len(populacao) / 2)
    for i in range(qtdPares):
        indice_par_2 = rd.randint(i + 1, len(populacao) - 1)                
        if indice_par_2 == i:
            continue    
        pares_1.append(populacao[i])
        pares_2.append(populacao[indice_par_2])        
    return pares_1, pares_2        
    
#OK    
def order_operator(par1, par2):
    
    tamanho_individuo = len(par1)
    metade = int(tamanho_individuo/2)
    # escolhe os pontos de cortes
    ponto_corte_1, ponto_corte_2 = rd.randint(0, metade), rd.randint(metade ,tamanho_individuo - 1)    

    entre_os_cortes = par1[ponto_corte_1:ponto_corte_2]
        
    novo_par = []
    indice_novo_par = 0
        
    for i in range(tamanho_individuo): 
        if par2[i] not in entre_os_cortes:
            novo_par.insert(indice_novo_par, par2[i])
            indice_novo_par += 1

    for i in range(len(entre_os_cortes)):
        index_par1 = par1.index(entre_os_cortes[i])
        novo_par.insert(index_par1, par1[index_par1])

    return novo_par  

#OK
def cross_over(machos,femeas):
  
  populacao = []

  # CROSSOVER
  for i in range(len(machos)):
    macho = machos[i]
    femea = femeas[i]
    # faz a troca de material genetico 
    populacao.append(order_operator(macho, femea))
    populacao.append(order_operator(femea, macho))

  return populacao


#OK
def calcular_distancia(individuo):
    valorDistancia = 0
    for i in range(0, len(individuo)-1):
        individuoOrigem = individuo[i]
        individuoDestino = individuo[i + 1]
        valorDistancia += dists.loc[individuoOrigem, individuoDestino]
    return valorDistancia
#OK
def fit(populacao):
    distancias = []    
    for individuo in populacao:
        # coloca-se o inverso pois o maior é o menor..
        distancias.append(1/calcular_distancia(individuo))        
    maior_valor = max(distancias)
    total = sum(distancias)    
    frequencias_relativas = []

    for distancia in distancias:
        frequencias_relativas.append(distancia/total)

    roleta = pd.DataFrame(columns={"indice", "distancia", "frequencia_inicial", "frequencia_final"})           

    frequencias_relativas.sort()

    for i,distancia in enumerate(distancias):   

        frequencia_inicial = sum(frequencias_relativas[0:i])
        frequencia_final = sum(frequencias_relativas[0:i + 1])
            
        area_roleta = pd.DataFrame(
                     {   
                      "indice": i,
                      "distancia": distancia, 
                      "frequencia_inicial": frequencia_inicial, 
                      "frequencia_final": frequencia_final
                      }, index = [i])
        # criaçõ da roleta com a distância e os range das frequencias.
        roleta = roleta.append(area_roleta, ignore_index=True)

    #roda a roleta pra achar os valores     
    individuos_selecionados = [] 

    for i in range(0, len(populacao)):  
        numero_aleatorio_roleta = rd.random() * 1      
        area_roleta_selecionada = roleta.loc[(roleta["frequencia_inicial"] < numero_aleatorio_roleta) & (roleta["frequencia_final"] > numero_aleatorio_roleta)]
        individuos_selecionados.append((populacao[int(area_roleta_selecionada["indice"])]))

    return individuos_selecionados   

  
#OK
def mutacao(populacao, chance_sofrer_mutacao):
  for individuo in populacao:
     if rd.random() < chance_sofrer_mutacao:
        posicoes_sorteadas = rd.sample(range(0, len(individuo)), 2)
        # troca as posições sorteadas
        individuo[posicoes_sorteadas[0]], individuo[posicoes_sorteadas[1]] = individuo[posicoes_sorteadas[1]], individuo[posicoes_sorteadas[0]]
        
  return populacao        


#OK
def menor_distancia_populacao(populacao):  
    menor_distancia = [-1, pow(10,9)]
    for index, individuo in enumerate(populacao):
        distancia = calcular_distancia(individuo)
        if distancia < menor_distancia[1]:
            menor_distancia = [index, distancia]
    return menor_distancia

# INICIADO O ALGORITMO GENÉTICO
POPULACAO_TAM = 50
RAND_MUTACAO = 0.05
NUM_EXECUCOES = 100

populacao = []

for i in range(POPULACAO_TAM):
    populacao.append(selecionar_individuo_aleatorio(qtd_cidades))
    
menores_distancias_geracoes = []

for i in range(0, NUM_EXECUCOES):
    print("Geração: " + str(i))
    populacao = fit(populacao)
    machos,femeas = formar_pares_aleatorios(populacao)
    populacao = cross_over(machos,femeas)
    populacao = mutacao(populacao, RAND_MUTACAO)
    menores_distancias_geracoes.append(menor_distancia_populacao(populacao))    

menor_distancia_total = populacao[menores_distancias_geracoes[menores_distancias_geracoes == min([d[1] for d in menores_distancias_geracoes])][0]]

plot_distancias = []

for dist in menores_distancias_geracoes:
    plot_distancias.append(dist[1])
    print('distância mínima encontrada em {} gerações: {}'.format(NUM_EXECUCOES, min([d[1] for d in menores_distancias_geracoes])))
plt.plot(plot_distancias)
plt.title("Plot das distâncias de cada geração")
plt.show()

def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

fig1 = plt.figure(figsize=(12,6))
route_coords = np.array([[coordinates_x[x] for x in menor_distancia_total], [coordinates_y[y] for y in min_route]])
plotcities, plotroute = plt.plot(coordinates_x, coordinates_y, 'bx', [], [], 'r-')

plt.title('Plot da menor distância encontrada..')
ani = animation.FuncAnimation(fig1, update_line, 100, fargs=(route_coords, plotroute), interval=100, blit=True)

plt.show()