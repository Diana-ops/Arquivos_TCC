"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de uso automático para o joystick e capacete mindflex
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import sys
import os
import paho.mqtt.client as mqtt
from threading import Thread


client = mqtt.Client()
Broker = "diana-desktop.local"
PortaBroker = 1883
KeepAliveBroker = 60
TimeoutConexao = 5 #em segundos
TopicoPublish = "Sara"  #substitua este topico por algum de sua escolha (de preferencia, algo "unico" pra voce)
#Criando a janela do menu
cinza = '#d3d3d3'
janela_uso_automatico = tk.Tk()
janela_uso_automatico.title("Uso Automatico")
janela_uso_automatico.configure(bg=cinza)
width=480
height=320
screen_width = janela_uso_automatico.winfo_screenwidth()
screen_height = janela_uso_automatico.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_uso_automatico.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_uso_automatico , width=480, height=320,bg=cinza)
canvas.pack()

def janela_menu():
    janela_uso_automatico.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_menu.py')
    sys.exit()

def janela_testes():
    janela_uso_automatico.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_testes.py')
    sys.exit()

def iniciar_uso():
    os.system('sudo python3 /home/diana/diana_testes/config_tela/teste_automa.py &')

        #---------------- Abre o arquivo com os dados do melhor treinamento  ----------------------#
    quant_elementos = 33
    dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
    for i in range(len(dados_melhor_treinamento)):
            coluna = dados_melhor_treinamento[i].split(";")

    coluna[0] = int(coluna[0])
    
    dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
    [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
    dados_melhor_treinamento.write(str(coluna[quant_elementos]))
    dados_melhor_treinamento.close()

def iniciar_joy():

    #---------------- Abre o arquivo com os dados do melhor treinamento  ----------------------#
    quant_elementos = 33
    dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
    for i in range(len(dados_melhor_treinamento)):
            coluna = dados_melhor_treinamento[i].split(";")

    coluna[0] = 17
    
    dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
    [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
    dados_melhor_treinamento.write(str(coluna[quant_elementos]))
    dados_melhor_treinamento.close()
    
    os.system('sudo python3 /home/diana/diana_testes/config_tela/teste_automa.py &')

    

def parar():
    global client
    
    client.publish(TopicoPublish, "BT5")
    print("Parando carrinho - Game Over")
    os.system('sudo bash matar_processo.sh')
    return

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

print("[STATUS] Inicializando MQTT...")
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, PortaBroker, KeepAliveBroker)
#inicializa thread de mqtt
ThMQTT = Thread(target=client.loop_forever)
ThMQTT.start()

#Mostrando imagem bot_teste
pil_image0 = Image.open('uso_automaticao/iniciar.png')
image_0 = pil_image0.resize((135, 116), Image.ANTIALIAS) #Tamanho da imagem
image_0.save('uso_automaticao/iniciar.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_uso_automatico)
botao0.config(image=tk_image0, compound="right", command=iniciar_uso, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=80, y= 100)

pil_image4 = Image.open('uso_automaticao/joy.png')
image_4 = pil_image4.resize((155, 76), Image.ANTIALIAS) #Tamanho da imagem
image_4.save('uso_automaticao/joy.png')
tk_image4 = ImageTk.PhotoImage(image_4)
botao4 = tk.Button(janela_uso_automatico)
botao4.config(image=tk_image4, compound="right", command=iniciar_joy, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao4.place(x=230, y= 130)


pil_image2 = Image.open('uso_automaticao/menu.png')
image_2 = pil_image2.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_2.save('uso_automaticao/menu.png')
tk_image2 = ImageTk.PhotoImage(image_2)
botao2 = tk.Button(janela_uso_automatico)
botao2.config(image=tk_image2, compound="right", command=janela_menu, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao2.place(x=10, y= 10)

pil_image3 = Image.open('uso_automaticao/voltar.png')
image_3 = pil_image3.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_3.save('uso_automaticao/voltar.png')
tk_image3 = ImageTk.PhotoImage(image_3)
botao3 = tk.Button(janela_uso_automatico)
botao3.config(image=tk_image3, compound="right", command=janela_testes, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao3.place(x=10, y= 250)

label2 = tk.Label(text="Controle do dispositivo com ", fg='black', bg=cinza, font=("Helvetica 20 bold",15) )
label2.place(x=95, y=20)

label3 = tk.Label(text="Ondas Cerebrais", fg='#005580', bg=cinza, font=("Helvetica 20 bold",15) )
label3.place(x=160, y=50)

pil_image7 = Image.open('uso_automaticao/parar_capacete.png')
image_7 = pil_image7.resize((45, 45), Image.ANTIALIAS) #Tamanho da imagem
image_7.save('uso_automaticao/parar_capacete.png')
tk_image7 = ImageTk.PhotoImage(image_7)
botao7 = tk.Button(janela_uso_automatico)
botao7.config(image=tk_image7, compound="right", command=parar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao7.place(x=150, y= 200)

pil_image8 = Image.open('uso_automaticao/parar_joy.png')
image_8 = pil_image8.resize((45, 45), Image.ANTIALIAS) #Tamanho da imagem
image_8.save('uso_automaticao/parar_joy.png')
tk_image8 = ImageTk.PhotoImage(image_8)
botao8 = tk.Button(janela_uso_automatico)
botao8.config(image=tk_image8, compound="right", command=parar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao8.place(x=270, y= 200)

janela_uso_automatico.mainloop()
