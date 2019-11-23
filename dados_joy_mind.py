"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Tratamento dos dados para testar a capacidade de classificação da RNA
"""

import csv,os
import random as rd

diretorio = "17"
pasta = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/brutos_med_"+diretorio+"/"
pastas = os.listdir(pasta)
nomes = ["sinal","med", "aten", "direita", "esquerda", "frente","ligar", "neutro", "parar","tras"]

for i in range(len(pastas)):
    for p in range(len(nomes)):
        if pastas[i].find(nomes[p]) == 0:
            arq  = open(pasta+pastas[i]).readlines()
            arq_  = open(pasta+pastas[i], "w")
            
            valor = 1000000*p
            for j in range(1,len(arq)):
                linha = arq[j].split(";")
                for k in range(3, len(linha)):
                     linha[k] = int(linha[k])
                     linha[k] = 100
                linha[p] = 100*p
                
                """
                linha[3] = rd.randint(1000,9000000)
                linha[4] = rd.randint(1000,9000000)
                linha[5] = rd.randint(1000,9000000)
                linha[6] = rd.randint(1000,9000000)
                linha[7] = rd.randint(1000,9000000)
                linha[8] = rd.randint(1000,9000000)
                linha[9] = rd.randint(1000,9000000)
                """
                
                [arq_.write(str(linha[l])+";") for l in range(0,10)]
                arq_.write(str(linha[10])+"\n")
            arq_.close()

