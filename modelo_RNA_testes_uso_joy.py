"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Recebe os dados do capacete para classificação da RNA e acionamento do carrinho
"""
from sklearn.neural_network import MLPClassifier
import csv, os, serial, pickle
import numpy as np
from time import sleep
import paho.mqtt.client as mqtt
from threading import Thread
import random as rd

#Abre arquivo com os dados do melhor treinamento 
nome_dir = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
coluna = nome_dir[len(nome_dir)-1].split(";") #Considerando as informacoes da ultima linha

#Extraindo as informacoes do melhor treinamento
diretorio, filtro, div, filtro_superior, camadas, saidas = coluna[0], coluna[1], int(coluna[2]), coluna[3], int(coluna[4]), int(coluna[5])

if diretorio == "17":
    ser = serial.Serial("/dev/ttyACM0", 9600) #Conecta no Arduino ligado ao JOYSTICK
    print("Abrindo modelo para o Joystick...")
    with open("salva_modelo_joy.pkl", "rb") as f:clf = pickle.load(f) #Abre o modelo salvo
    print("Aberto!")
    
else:
    ser = serial.Serial("/dev/ttyUSB0", 9600) #Conecta no Arduino ligado ao Capacete 
    print("Abrindo modelo para a classificação de ondas cerebrais ...")
    with open("salva_modelo.pkl", "rb") as f:clf = pickle.load(f) #Abre o modelo salvo
    print("Aberto!")

print("Diretorio:", diretorio)
    
os.chdir("/home/diana/diana_testes/config_tela")
#-------------------------------Configuracoes do mqtt -------------------------#

client = mqtt.Client()
Broker = "diana-desktop.local"
PortaBroker = 1883
KeepAliveBroker = 60
TimeoutConexao = 5 #em segundos
TopicoPublish = "Sara"  #substitua este topico por algum de sua escolha (de preferencia, algo "unico" pra voce)


def FinalizaPrograma():
    global client
 
    print("O programa esta sendo finalizado.")
    client.disconnect()
    janela_uso_manual.destroy()
    sys.exit()
    
#Callback - conexao ao broker realizada
def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conectado ao Broker. Resultado de conexao: "+str(rc))
    return
 
#Callback - mensagem recebida do broker
def on_message(client, userdata, msg):
    MensagemRecebida = str(msg.payload)
    print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+MensagemRecebida)
    return

def EventoBotao1(movimento):
    global client
    
    client.publish(TopicoPublish, str(movimento))

    return


print("[STATUS] Inicializando MQTT...")
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, PortaBroker, KeepAliveBroker)
#inicializa thread de mqtt
ThMQTT = Thread(target=client.loop_forever)
ThMQTT.start()


#------------------------ Funcionamento da RNA -----------------------#
def aplicar_modelo(tempo):

            #Conta e armazenas quantas classificações foram feitas para cada saida
            resultados = [0,0,0,0,0,0,0] 

            #Abre arquivo do relatório de testes
            ca_g = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/relatorios_med_"+diretorio
            relatorio_testes = open(ca_g+"/relatorio_testes_med_"+diretorio+".csv", 'r')
            conteudo = relatorio_testes.readlines()

            nomes = ["direita", "esquerda", "frente","ligar", "neutro", "parar","tras"]
            nomes.sort()

            msg_mcu = ["direita", "esquerda", "frente","ligar", "neutro", "parar","tras"]

            entrada_RNA = list()
            leituras = 0
        
            if diretorio == "17":
                while leituras < tempo:
                    leitura_joy = ser.readline()
                    #print(leitura_joy)
                    
                    for i in range(len(nomes)):
                                                        leitura = [0,0,0]
                                                        if leitura_joy.decode('utf-8').split("\n")[0].find(nomes[i]) == 0: #Detectando a posição do joystick
                                                                for dado in range(3,11):
                                                                        leitura.append(100)
                                                                leitura[i+3] = 100*(i+3)
                                                                #print(leitura)

                                                                #print(nomes[i])
                                                                
                                                                #Abrindo os maiores valores do Dataset
                                                                max_norma = open("/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/maior_arq_"+diretorio+".csv").readlines()

                                                                #Convertendo para inteiro
                                                                for i in range(len(max_norma)):
                                                                        linha_max = max_norma[i].split(";")
                                                                        [int(linha_max[i]) for i in range(len(linha_max))]
                                                                
                                                                leituras = leituras + 1
                                                                #print(leituras)
                                                                if all(int(leitura[i]) <= int(linha_max[i])  for i in range(3,11)):
                                                                            
                                                                            [entrada_RNA.append(((float(leitura[i])/float(linha_max[i])))) for i in range(3,11)]
                                                                            valor = (clf.predict([entrada_RNA]))
                                                                            #print(entrada_RNA)
                                                                            valor = int(valor)
                                                                            print("[RNA] " + nomes[valor])
                                                                            entrada_RNA = []
                                                                            
                                                                            

                                                                            for i in range(0,len(nomes)):
                                                                                if valor == 0: #Direita 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[0] = resultados[0] + 1
                                                                                        EventoBotao1("BT4")
                                                                                        
                                                                                elif valor == 1: #Esquerda 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[1] = resultados[1] + 1
                                                                                        EventoBotao1("BT3")
                                                                                        
                                                                                elif valor == 2: #Frente 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[2] = resultados[2] + 1
                                                                                        EventoBotao1("BT1")
                                                                                        
                                                                                elif valor == 5: #Parar 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[5] = resultados[5] + 1
                                                                                        EventoBotao1("BT5")
                                                                                        
                                                                                elif valor == 6: #Tras 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[6] = resultados[6] + 1
                                                                                        EventoBotao1("BT2")
                                                                                
                                                                                        
                                                                                        
                
                else:
                                                                     [conteudo.append((str(nomes[i])+": "+str(resultados[i])+"\n")) for i in range(len(nomes))]
                                                                     EventoBotao1("BT5")
                                                                     print("Finalizando SImulação")
                                                                     print(resultados)
                                                                     #client.disconnect()
                                                                     relatorio_testes = open(ca_g+"/relatorio_testes_med_"+diretorio+".csv", 'w')
                                                                     [relatorio_testes.write(str(conteudo[i])) for i in range(len(conteudo))]
                                                                     relatorio_testes.close()
                                                                     return resultados
            if diretorio != "17":
                    while leituras < tempo:
                                    leitura_mindflex = ser.readline()
                                    v = leitura_mindflex.decode('utf-8').split(",")
                                    
                                    if len(v) == 11:
                                        entrada_RNA = []
                                
                                        #Abrindo os maiores valores do Dataset
                                        max_norma = open("/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/maior_arq_"+diretorio+".csv").readlines()

                                        #Convertendo para inteiro
                                        for i in range(len(max_norma)):
                                                    linha_max = max_norma[i].split(";")
                                                    [int(linha_max[i]) for i in range(len(linha_max))]
                                                                    
                                        leituras = leituras + 1
                                        #print(leituras)
                                        if all(int(v[i]) <= int(linha_max[i])  for i in range(3,11)):
                                                                                
                                            [entrada_RNA.append(((float(v[i])/float(linha_max[i])))) for i in range(3,11)]
                                            #print(entrada_RNA)
                                            valor = (clf.predict([entrada_RNA]))
                                            valor = int(valor)
                                            print("[RNA] " + nomes[valor])
                                            
                                            
                                            for i in range(0,len(nomes)):
                                                     if valor == 0: #Direita 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[0] = resultados[0] + 1
                                                                                        EventoBotao1("BT4")
                                                                                        
                                                     elif valor == 1: #Esquerda 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[1] = resultados[1] + 1
                                                                                        EventoBotao1("BT3")
                                                                                        
                                                     elif valor == 2: #Frente 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[2] = resultados[2] + 1
                                                                                        EventoBotao1("BT1")
                                                                                        
                                                     elif valor == 3: #Ligar 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[3] = resultados[3] + 1
                                                     elif valor == 4: #Ligar 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[4] = resultados[4] + 1
                                                                                        
                                                     elif valor == 5: #Parar 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[5] = resultados[5] + 1
                                                                                        EventoBotao1("BT5")
                                                                                        
                                                     elif valor == 6: #Tras 
                                                                                        #print("[RNA] " + nomes[i])
                                                                                        resultados[6] = resultados[6] + 1
                                                                                        EventoBotao1("BT2")
                    
                    
                    for i in range(len(resultados)):
                       resultados[i] = int(resultados[i]/7)
                                                                                             
                    [conteudo.append((str(nomes[i])+": "+str(resultados[i])+"\n")) for i in range(len(nomes))]
                    EventoBotao1("BT5")
                                                                                             #client.disconnect()
                    relatorio_testes = open(ca_g+"/relatorio_testes_med_"+diretorio+".csv", 'w')
                    [relatorio_testes.write(str(conteudo[i])) for i in range(len(conteudo))]
                    relatorio_testes.close()
                    return resultados
EventoBotao1("BT5")                                                                 
        
