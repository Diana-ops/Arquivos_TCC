"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Treinamento da RNA e calculo de desempenho
"""
from sklearn.neural_network import MLPClassifier
import numpy as np
import csv, os, pickle

os.chdir("/home/diana/diana_testes/config_tela")

def treinar_rede_dataseet(diretorio):
    melhores_resultados = [0,0,0,0,0] #Filtro - Limite - Div - Filtro Superior - Camadas - Saidas
    quantidades_resul  = [0,0,0]
    print("Iniciando treinamento \n")
    #Caminho para armazenar o relatório 
    ca_g = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/relatorios_med_"+diretorio
    relatorio = open(ca_g+"/relatorio_resultados_med_"+diretorio+".csv", "w")
    
    melhor = 0 #Minimo valor que a RNA deve conseguir classificar cada uma das saidas
    #  [0,10,20,30,40]
    for filtro_inferior in [0,10,20,30,40]: #Os filtros devem ser os mesmos, tanto para os dados de treinamento quanto para os de teste
            for filtro_superior in [100]:
                for div in [100]:

                    #Abrindo arquivos para treinar a RNA, testar e validar
                    ca = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/treinamento_normalizados_med_"+diretorio
                    ca_ = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/teste_normalizados_med_"+diretorio
                    cav = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/valida_normalizados_med_"+diretorio
                    
                    dados_entradas = open(ca+"/entrada_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv").readlines()
                    dados_saidas = open(ca+"/saida_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv").readlines()
                    
                    entrada_teste = open(ca_+"/entrada_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv").readlines()
                    saida_teste = open(ca_+"/saida_"+str(filtro_inferior)+"_"+str(filtro_superior)+".csv").readlines()

                    entrada_valida = open(cav+"/entrada_normalizados_valida.csv").readlines()
                    saida_valida =open(cav+"/saida_normalizados_valida.csv").readlines()

                    if len(dados_entradas) != 0 and len(entrada_teste) != 0:
                        #print(filtro_inferior, len(dados_entradas), len(entrada_teste))
                       #Saidas possíveis 
                        saidas = ["frente", "tras", "esquerda","direita", "ligar", "parar","neutro"]
                        saidas.sort()
                        
                        dire = [] #Armazenará somente o nome das saidas que existem no diretorio 
                        index = [] #Armazena os indices que serão testados, isto e, 0,1,2,3,4,5 ou 6
                        

                        walk_past = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/brutos_med_"+diretorio+"/" 
                        pasta = os.listdir(walk_past)
                        
                        #Buscando as saidas existentes no diretorio de arquivos de teste
                        for i in range(len(pasta)):
                            for s in range(len(saidas)):
                                if pasta[i].find(str(saidas[s])) == 0 and saidas[s].split("_")[0] not in dire:
                                        
                                        dire.append(str(saidas[s].split("_")[0]))
                                        index.append(s)

                        dire.sort() #Ordena as saidas encontradas para que a lista de dados de teste fique ordenada também 
                        index.sort()
                                        
                        #Separando os dados de treinamento 
                        entrada_RNA = list()
                        saida_RNA = list()

                        for i in range(len(dados_entradas)):
                                saida_RNA.append(int(dados_saidas[i]))
                                linha = dados_entradas[i].split(";")
                                linha = [float(linha[i]) for i in range(len(linha))]
                                entrada_RNA.append(linha)
                                                           
                        #Separando os dados de teste 
                        entrada_t = list()
                        saida_t = list()
                        
                        for i in range(len(entrada_teste)):
                                saida_t.append(int(saida_teste[i]))
                                linha = entrada_teste[i].split(";")
                                linha = [float(linha[i]) for i in range(len(linha))]
                                entrada_t.append(linha)

                        #Separando os dados de validação 
                        entrada_v = list()
                        saida_v = list()
                        
                        for i in range(len(entrada_valida)):
                                saida_v.append(int(saida_valida[i]))
                                linha = entrada_valida[i].split(";")
                                
                                linha = [float(linha[i]) for i in range(len(linha))]
                                entrada_v.append(linha)

                         
                        relatorio.write("---------------------------------------------------\n")
                        relatorio.write("Resultados: "+"Filtro: "+str(filtro_inferior)+" Div: "+str(div)+" Filtro Superior: "+str(filtro_superior)+"\n\n")
                        
                        for camadas in [28,25]:
                                relatorio.write("Número de camadas: "+str(camadas)+"\n\n")

                                #Definição das caracteristicas da rede
                                clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes = (camadas,len(dire)), random_state=1)
                                hidden_layer_sizes = (camadas,len(dire))
                                clf.fit(entrada_RNA,saida_RNA) #Treinando modelo
                                
                                resul_RNA = clf.predict(entrada_RNA) #Prediz os dados do próprio dataset
                                resul_TESTE = clf.predict(entrada_t) #Prediz os dados de teste
                                resul_valida = clf.predict(entrada_v) #Prediz novos dados 
                                
                                certo = [0,0,0] #Armazena os acertos para os dados de treino, teste e validação
                                errado = [0,0,0] #Armazena os erros para os dados de treino, teste e validação

                                # ---- Calculando Desempenho para os dados de treinamento, teste e validação ---- #

                                def calcula_desempenho(rede, saida_certa, posi):
                                    for i in range(len(rede)):
                                        rede[i]  = int(rede[i]) #Resultados preditos pela rede
                                        saida_certa[i] = int(saida_certa[i]) #Saídas corretas 
             
                                        if saida_certa[i] == 4:
                                            if rede[i]  == 4:
                                                certo[posi] = certo[posi] + 1
                                            else:
                                                errado[posi] = errado[posi] + 1
                                        else:
                                                for s in index:
                                                    if s!=4:
                                                        #Se a saida for um valor e a rede predizer o mesmo valor ou neutro
                                                        if saida_certa[i] == s: 
                                                            if rede[i]  == s or rede[i]  == 4:
                                                                certo[posi] = certo[posi] + 1
                                                            else:
                                                                #Se classificou outro movimento
                                                                errado[posi] = errado[posi] + 1
                                                                
                                calcula_desempenho(resul_RNA, saida_RNA, 0)
                                calcula_desempenho(resul_TESTE, saida_t, 1)
                                calcula_desempenho(resul_valida, saida_v, 2)

                                for i in [0,1,2]:
                                    certo[i] = (certo[i]/(certo[i]+errado[i]))*100
                                    errado[i] = (errado[i]/(certo[i]+errado[i]))*100
                                                            
                                relatorio.write("Acertos (Treinamento) \t"+ str(certo[0])+ "%""\nErrado (Treinamento)\t"+ str(errado[0])+ "%\n\n")
                                relatorio.write("Acertos (Teste) \t"+ str(certo[1])+"%"+"\nErrado (Teste)\t"+ str(errado[1])+ "%\n\n")
                                relatorio.write("Acertos (Validação) \t"+ str(certo[2])+"%"+"\nErrado (Validação)\t"+ str(errado[2])+ "%\n\n")
                                
                                #Mostra o desempenho dos dados de treinamento
                                resultado_rede = (clf.score(entrada_RNA, saida_RNA, sample_weight=None)*100)
                                relatorio.write("Treinamento: "+str(resultado_rede.round(2))+ " %\n")

                                #Mostra o desempenho dos dados de teste
                                resultado_teste = (clf.score(entrada_t, saida_t, sample_weight=None)*100)
                                relatorio.write("Teste: "+str(resultado_teste.round(2))+" %\n")

                                #Mostra o desempenho dos dados de validação
                                resultado_valida = (clf.score(entrada_v, saida_v, sample_weight=None)*100)
                                relatorio.write("Validação: "+str(resultado_valida.round(2))+" %\n\n")
                                
                                if certo[1] > melhor: #Quanto melhor for o resultado dos dados de validação 
                                    melhor = certo[1]

                                    #Registra as melhores caracteristicas do treinemento
                                    quantidades_resul = []
                                    melhores_resultados = [filtro_inferior, div, filtro_superior, camadas, len(dire)]
                                    
                                    #Salvando as quantidades 
                                    quantidades_resul.append(str(len(entrada_RNA))) 
                                    quantidades_resul.append(str(len(entrada_t)))
                                    quantidades_resul.append(str(len(entrada_v)))

                                    #Salvando o desempenho
                                    for d in [0,1,2]:
                                        certo[d] = round(certo[d],2)
                                        quantidades_resul.append(str(certo[d]))
                                        
                                    
                                    #Salva o melhor modelo de RNA encontrado
                                    if diretorio!="17":
                                        with open("salva_modelo.pkl", "wb") as f:pickle.dump(clf, f)
                                    else:
                                        with open("salva_modelo_joy.pkl", "wb") as f:pickle.dump(clf, f)
                                                                       
    print(melhores_resultados) #Devolve os dados do melhor treinamento
    relatorio.write("Melhores Resultados: "+str(melhores_resultados))
    relatorio.close()
    return melhores_resultados, quantidades_resul

