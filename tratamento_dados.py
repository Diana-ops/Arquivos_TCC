"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Normalização e filtro dos dados para uma faixa de valores para a construção dos datasets
Separação dos dados de treinamento e teste
"""

import csv, os, shutil
from sklearn.model_selection import train_test_split

def iniciar_normalizacao(diretorio):

    print("Diretório: ", diretorio)
    #Caminho para armazenar os relatórios
    ca_g = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/relatorios_med_"+diretorio
    relatorio = open(ca_g+"/relatorio_dados_med_"+diretorio+".csv", "w")
    relatorio_testes = open(ca_g+"/relatorio_testes_med_"+diretorio+".csv", "w")

    #Saidas possíveis 
    saidas = ["frente", "tras", "esquerda","direita", "ligar", "parar","neutro"]
    saidas.sort()
    
    
    dic = [] #Armazenará somente o nome das saidas que existem no diretorio
    dic_valida = [] 
    index = [] #Armazenas qual valor correspondente ao movimento a RNA vai associar
    numeracao = [0]*7 #Armazena a maior numeração do arquivo de cada movimento

    #Abrindo diretório de dados brutos para treinamento e teste
    walk_past = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/brutos_med_"+diretorio+"/"
    pasta = os.listdir(walk_past)

    valida_brutos = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/valida_brutos_med_"+diretorio+"/"
    pasta_valida_brutos = os.listdir(valida_brutos)

    #Descobrindo a quantidade de saídas 
    for i in range(len(pasta)):
        for s in range(len(saidas)):
            if pasta[i].find(str(saidas[s])) == 0 and saidas[s].split("_")[0] not in dic:
                dic.append(str(saidas[s].split("_")[0]))
    print("Saidas Utilizadas: ", dic, "\n")

    #Descobrindo a quantidade de saídas que já estão no diretório de dados brutos para validação
    for i in range(len(pasta_valida_brutos)):
        for s in range(len(saidas)):
            if pasta_valida_brutos[i].find(str(saidas[s])) == 0 and saidas[s].split("_")[0] not in dic_valida:
                dic_valida.append(str(saidas[s].split("_")[0]))
    
    #Separando 1 amostra de cada entrada para validação
    if len(pasta_valida_brutos) < len(dic):
        dic = []
        for i in range(len(pasta)):
            for s in range(len(saidas)):
                if pasta[i].find(str(saidas[s])) == 0 and saidas[s].split("_")[0] not in dic_valida:
                    dic_valida.append(str(saidas[s].split("_")[0]))
                    os.link(walk_past+pasta[i], valida_brutos+pasta[i]) #Transferindo arquivo
                    os.remove(walk_past+pasta[i])
                
    dic = []
    
    #Buscando as saidas existentes no meu diretorio 
    for i in range(len(pasta)):
        for s in range(len(saidas)):
            numero = pasta[i].split("_")[1]
            numero= numero.split(".csv")[0]
            if (int(numero) > numeracao[s]) and  pasta[i].find(str(saidas[s])) == 0:
                numeracao[s] = int(numero)
            if pasta[i].find(str(saidas[s])) == 0 and saidas[s].split("_")[0] not in dic:
                dic.append(str(saidas[s].split("_")[0]))
                index.append(s)
                
    dic.sort()
    index.sort()
    relatorio.write("--------------- TRATAMENTO DOS DADOS ------------------\n")
    relatorio.write("Saidas: "+str(dic)+"\n")
    relatorio.write("Valor Index: "+str(index)+"\n")

    
    #Caminho dos diretórios 
    ca = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/treinamento_normalizados_med_"+diretorio
    ca_= "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/teste_normalizados_med_"+diretorio
    
    #Recebe dados normalizados para treinamento e teste 
    dados_normalizados = open(ca+"/entrada_normalizados.csv", 'w')
    saida_normalizados = open(ca+"/saida_normalizados.csv", 'w')

    
    maior = [0] * 11

    #Lista para os dados de treinamento e teste
    arq_entrada = []
    arq_saida = []
    
    #Abrindo os arquivos, convertendo para int e encontrando o maior valor
    #Abrindo diretório de dados brutos para treinamento e teste
    walk_past = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/brutos_med_"+diretorio+"/"
    pasta = os.listdir(walk_past)
                
    #O valor da saída é determinado pelo nome do arquivo
    for i in range(len(pasta)): #Para todos os arquivos no diretorio
        arq = open(walk_past+pasta[i]).readlines()
        if pasta[i].find(str(saidas[0])) == 0: #Mão Aberta
                saida_ = 0
        elif pasta[i].find(str(saidas[1])) == 0: #Mão Fechada
                saida_ = 1
        elif pasta[i].find(str(saidas[2])) == 0:
                saida_ = 2
        elif pasta[i].find(str(saidas[3])) == 0:
                saida_ = 3 
        elif pasta[i].find(str(saidas[4])) == 0: #Neutro
                saida_ = 4
        elif pasta[i].find(str(saidas[5])) == 0:
                saida_ = 5
        elif pasta[i].find(str(saidas[6])) == 0: 
                saida_ = 6
                
                
        #Abrindo todos os arquivos e encontrando o maior valor 
        for l in range(1, len(arq)): #Iguinorando a primeira linha de todos os arquivos
                linha = arq[l].split(";")
                for j in range(len(linha)): #Para cada linha
                        linha[j] = int(linha[j]) 
                        if linha[j] > maior[j]: 
                                maior[j] = linha[j]
                arq_entrada.append(linha) #Cada linha ficou como uma lista
                arq_saida.append(saida_)
                        
                    
    #Normalizando os dados para treinamento e teste
    for i in range(len(arq_entrada)): #Para cada linha do arquivo de entrada
            for j in range(3, len(arq_entrada[i])): #Seleciona apenas as ondas cerebrais
                arq_entrada[i][j] = (arq_entrada[i][j]/maior[j])*100 #Normaliza
                    
    #Gravando dados normalizados em um arquivo
    for i in range(len(arq_entrada)):
            saida_normalizados.write(str(arq_saida[i])+"\n")
            for j in range(3, len(arq_entrada[i])):
                if j < len(arq_entrada[i]) -1:
                        dados_normalizados.write(str(arq_entrada[i][j])+";")
                else:
                        dados_normalizados.write(str(arq_entrada[i][j]))
            dados_normalizados.write("\n")

    
    relatorio.write("\n")  
    relatorio.write("-"*40)
    relatorio.write("\nQuantidade de Dados Brutos/Normalizados para cada movimento: \n")
    [relatorio.write(str(saidas[i]).capitalize() + "--" + str(arq_saida.count(i)) + "\n") for i in index]
    relatorio.write("Total Brutos: "+str(len(arq_entrada))+"\n")
    relatorio.write("\n\n")
    relatorio.write("*"*40)
    
    for filtro_inferior in [0,10,20,30,40, 80]:
        for filtro_superior in [100]:
                """
                Sem controle de quantidade, este será feita pelo limite maximo possivel para cada filtro e o mim.
                que cada movimento pode oferecer para termos a mesma quantidade de saidas para a RNA
                """
                relatorio.write("*"*40)
                relatorio.write("\nFiltro Inferior: " + str(filtro_inferior) + " Filtro Superior: " +str(filtro_superior)+ "\n")
                
                #Recebe dados filtrados
                entrada_treino = open(ca+"/entrada_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv", 'w')
                saida_treino = open(ca+"/saida_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv", 'w')

                entrada_teste = open(ca_+"/entrada_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv", 'w')
                saida_teste = open(ca_+"/saida_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv", 'w')

                arq_entrada_filtrados = []
                arq_saida_filtrados = []
                quant_saida_T= [0]*len(saidas) #Armazena a quantidade de dados para cada saida (Treinamento)
                quant_saida_t= [0]*len(saidas)
                
                #A partir dos dados normalizados, será feito um filtro
                for linha in range(len(arq_entrada)):

                        if arq_saida[linha] != 4: #Se for movimento

                            #Se todos os dados da linha forem menores que o filtro superior
                            if all(arq_entrada[linha][coluna] <= filtro_superior for coluna in range(3, len(arq_entrada[linha]))): 
                                #Se algum dados da linha for maior que o filtro inferior
                                if any(arq_entrada[linha][coluna] >= filtro_inferior for coluna in range(3, len(arq_entrada[linha]))):
                                    arq_entrada_filtrados.append(arq_entrada[linha][3:len(arq_entrada[linha])])
                                    arq_saida_filtrados.append(arq_saida[linha])
                                    
                            #if all(arq_entrada[linha][coluna] <= filtro_inferior for coluna in range(3, len(arq_entrada[linha]))):
                              #     arq_entrada_filtrados.append(arq_entrada[linha][3:len(arq_entrada[linha])])
                                #   arq_saida_filtrados.append(4)
                                        
                        else: #Se for neutro
                            
                        #Se todos os dados da linha forem menores que o filtro superior
                            if all(arq_entrada[linha][coluna] <= filtro_inferior for coluna in range(3, len(arq_entrada[linha]))):
                                   arq_entrada_filtrados.append(arq_entrada[linha][3:len(arq_entrada[linha])])
                                   arq_saida_filtrados.append(arq_saida[linha])
                                   
                                    
                                    
                #Contabilizando saidas
                relatorio.write("*"*40)
                relatorio.write("\n\n")
                relatorio.write("Quantidade de Dados Filtrados para cada movimento: \n")
                [relatorio.write(str(saidas[i]).capitalize()+ "-- "+ str(arq_saida_filtrados.count(i)) + "|\n") for i in index]
                relatorio.write("Total Filtrados: " + str(len(arq_entrada_filtrados))+"\n")
                relatorio.write("-"*40)
                relatorio.write("\n\n")

                relatorio.write("Separando os dados de treinamento e teste\n")

                #Separando dados
                T_treino, t_teste, S_treino, s_teste = train_test_split(arq_entrada_filtrados,arq_saida_filtrados, random_state=42)

                
                relatorio.write("Entrada de treino: 75% "+ str(len(T_treino))+"\n")
                relatorio.write("Entrada de teste: 25% "+str(len(t_teste))+"\n")
                relatorio.write("-"*40)
                relatorio.write("\n\n")

                #Contabilizando saidas  
                #print("Quantidade de Saidas: \n")
                #print("-"*10, "Teste\n")
                #[print(str(saidas[i]).capitalize(), "--", s_teste.count(i), end = " ") for i in index]
                #print("-"*10, "Treinamento\n") 
                #[print(str(saidas[i]).capitalize(), "--", S_treino.count(i), end = " ") for i in index]

                #Armazena a menor quantidade de dados para uma saida, limitando quantidade do restante para o mesmo valor
                menor_teste = s_teste.count(index[0]) #Armazena a quantidade de uma saida 
                menor_treino = S_treino.count(index[0])

                for i in index: #Para todas as saidas 
                    if s_teste.count(i) < menor_teste: #Se alguma quantidade for menor 
                        menor_teste = s_teste.count(i) #Considerar a menor encontrada
                        
                        
                relatorio.write("Minimo Teste: "+str(menor_teste)+"\n")
                
                for i in index:
                    if S_treino.count(i) < menor_treino:
                        menor_treino = S_treino.count(i)
                    
                        
                relatorio.write("Minimo Treino: "+str(menor_treino)+"\n\n")

                def grava_dados(arq_ent, arq_saida, entrada, saida, minimo, quant_saida):

                    """
                    Parametros:
                           Arquivo de entrada e saida .csv
                           Lista de entrada e saida dos dados separados
                           Menor quantidade de dados de treino/saida
                           LIsta que armazena a quantidade de saidas para treino e teste
                    """
                    for i in index:
                        for linha in range(len(entrada)):
                            if quant_saida[i] < minimo and saida[linha] == i:
                                arq_saida.write(str(saida[linha])+"\n")
                                for coluna in range(len(entrada[linha])):
                                    if coluna < len(entrada[linha]) - 1:
                                        arq_ent.write(str((entrada[linha][coluna])/100)+";")
                                    else:
                                        arq_ent.write(str((entrada[linha][coluna])/100))
                                arq_ent.write("\n")
                                quant_saida[i] = quant_saida[i] +1
                            
                        
                #Gravando dados de treinamento 
                grava_dados(entrada_treino, saida_treino, T_treino, S_treino, menor_treino, quant_saida_T)

                #Gravando dados de teste 
                grava_dados(entrada_teste, saida_teste, t_teste, s_teste, menor_teste, quant_saida_t)

                #Contabilizando saidas - Verificando se a quantidade de saidas esta igualmente distribuida 
                #print("Quantidade de Saidas Distribuidas: \n")
                #print("-"*10, "Teste\n")
                #[print(str(saidas[i]).capitalize(), "--", quant_saida_t[i], end = " ") for i in index]
                #print("-"*10, "Treinamento\n") 
                #[print(str(saidas[i]).capitalize(), "--", quant_saida_T[i], end = " ") for i in index]
                    
    #Salvando o maior valor em um arquivo para ser usado para a normalização dos dados de teste
    maior_arq = open("/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/maior_arq_"+diretorio+".csv", 'w')
    for i in range(len(maior)-1):
          maior_arq.write(str(maior[i])+";")
    maior_arq.write(str(maior[len(maior)-1]))
    maior_arq.close()
    relatorio.write("\nMaiores valores no Dataset: "+str(maior)+"\n")
    relatorio.close()

    
    #Constroi o arquivo com dados de validacao
    from dados_valida import constroi_dados_valida
    constroi_dados_valida(diretorio)
        
    #Verifica se é necessário coletar mais dados. Se sim, para quais movimentos
    faltando_movimentos = []
    quantidades = []

    for i in range(len(saidas)):
        if i in index:
            quantidades.append(str(arq_saida.count(i)))
        else:
            quantidades.append(0)
            
    quantidades.append(str(len(arq_entrada)))
        #Se para cada movimento temos 300 leituras para o treinamento
    
    if all(quant_saida_T[i] >= 0 for i in index):
        
        return True, quantidades, numeracao
    else:
        for i in index:
            if quant_saida_T[i] < 0:
                faltando_movimentos.append(str(saidas[i])) #Armazena o movimento que precisa ser coletado
        return faltando_movimentos, quantidades, numeracao
