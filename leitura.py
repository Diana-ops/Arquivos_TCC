"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Leitura e gravamento dos dados coletados em arquivo .csv
"""
import serial, os, csv, sys 
from time import sleep
        
def iniciar_leitura(escolha_mov, n_coleta, new_dir):
        
        ser = serial.Serial("/dev/ttyUSB0", 9600)
        print("Diretorio: ", new_dir)
        leitura_UNO = ser.readline() #Leitura da porta serial do Arduino 
        coluna = leitura_UNO.decode('utf-8').split(",")

        if len(coluna) == 11: #Se a leitura estiver completa 
        
                #Determina o nome do arquivo
                mov = escolha_mov
                num = ""
                data = n_coleta
                coleta = mov+num+"_"+data+".csv"
                
                

                #Cria e abre o arquivo para armazenar as coletas
                arq_coleta = open(coleta, "w")
                arq_coleta.write("Quali;Med;Aten;Delta;Theta;Alpha Baixo;Alpha Alto;Beta Baixo;Beta Alto;Gama Baixo;Gama Alto\n")
                os.link(coleta,"/home/diana/diana_testes/rede_coletas/med_"+str(new_dir)+"/brutos_med_"+str(new_dir)+"/"+coleta)
                os.remove(coleta)

                leituras = 0 
                filtro = 1000 #Estabelece um filtro para desconsiderar dados quando há falha na leitura  
                
                if len(coluna) == 11: #Se a leitura estiver completa
                        print("Movimento: " + escolha_mov)
                        try: 
                                while leituras <=120:
                                        
                                        ler_ard = ser.readline()
                                        coluna = ler_ard.decode('utf-8').split(",")
                                        sinal_veri = int(coluna[0])
                                        
                                        if (len(coluna) == 11): #Verifica se a leitura da coluna está completa
                                                        if all(int(coluna[i]) >= filtro for i in range(3,11)): 
                                                        #Passando a leitura para o arquivo de coleta
                                                                [arq_coleta.write(str(coluna[col])+";") for col in range(0,10)]
                                                                arq_coleta.write(str(coluna[10]))
                                                                leituras = leituras + 1
                                                                print("Leituras Feitas: ", leituras)
                                                                print(coluna)

                        except KeyboardInterrupt:
                                       print("----------------------------------Fim da Coleta--------------------------------------------------------")
                                       arq_coleta.close()
                                       sys.exit() #Fecha o código de leitura
        
