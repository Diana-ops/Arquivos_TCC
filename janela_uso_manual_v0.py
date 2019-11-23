"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de uso manual
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import paho.mqtt.client as mqtt
from threading import Thread
import sys
import os
from tkinter import font

cinza = '#d3d3d3'
#Configuracoes do mqtt

client = mqtt.Client()
Broker = "diana-desktop.local"
PortaBroker = 1883
KeepAliveBroker = 60
TimeoutConexao = 5 #em segundos
TopicoPublish = "Sara"  #substitua este topico por algum de sua escolha (de preferencia, algo "unico" pra voce)

########
#Eventos
########
def FinalizaPrograma():
    global client
 
    print("O programa esta sendo finalizado.")
    client.disconnect()
    janela_uso_manual.destroy()
    sys.exit()

mov_atual = " "
#Callback - conexao ao broker realizada
def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conectado ao Broker. Resultado de conexao: "+str(rc))
    return
 
#Callback - mensagem recebida do broker
def on_message(client, userdata, msg):
    MensagemRecebida = str(msg.payload)
    print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+MensagemRecebida)
    return

def EventoBotao1():
    global client, mov_atual
 
    print("[NodeMCU] Frente")
    client.publish(TopicoPublish,"BT1")
    mov_atual = "BT1"
    print(mov_atual)
    return
 
def EventoBotao2():
    global client, mov_atual
 
    print("[NodeMCU] Trás")
    client.publish(TopicoPublish,"BT2")
    mov_atual = "BT2"
    print(mov_atual)
    return
 
def EventoBotao3():
    global client, mov_atual
 
    print("[NodeMCU] Esquerda")
    client.publish(TopicoPublish,"BT3")
    print(mov_atual)

    #O carrinho se posiciona para a esquerda e segue realizando o movimento anterior
    if mov_atual != " ":
        client.publish(TopicoPublish, str(mov_atual))
    return
 
def EventoBotao4():
    global client, mov_atual
 
    print("[NodeMCU] Direita")
    client.publish(TopicoPublish,"BT4")
    print(mov_atual)

    #O carrinho se posiciona para a esquerda e segue realizando o movimento anterior
    if mov_atual != " ":
        client.publish(TopicoPublish, str(mov_atual))
    return
 
def EventoBotao5():
    global client, mov_atual
 
    print("[NodeMCU] Parar")
    client.publish(TopicoPublish,"BT5")
    
    mov_atual = " "
    print(mov_atual)
    return

 

print("[STATUS] Inicializando MQTT...")
print(client.on_connect)
print(client.on_message)
print(Broker)
print(PortaBroker)
print(KeepAliveBroker)
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, PortaBroker, KeepAliveBroker)

#inicializa thread de mqtt
ThMQTT = Thread(target=client.loop_forever)
ThMQTT.start()

janela_uso_manual = tk.Tk()
janela_uso_manual.title("Uso Manual")
janela_uso_manual.configure(bg=cinza)
width=480
height=320
screen_width = janela_uso_manual.winfo_screenwidth()
screen_height = janela_uso_manual.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_uso_manual.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_uso_manual , width=480, height=320,bg=cinza)
canvas.pack()

def janela_menu():
    janela_uso_manual.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_menu.py')
    sys.exit()

#Tamanho botão 
x=95
y=46

#Botao Frente
pil_image0 = Image.open('testes/frente.png')
image_0 = pil_image0.resize((x, y), Image.ANTIALIAS) #Tamanho da imagem
image_0.save('testes/frente.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_uso_manual)
botao0.config(image=tk_image0, command=EventoBotao1, compound="right", borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=70, y=100)

#Botao Tras
pil_image1 = Image.open('testes/tras.png')
image_1 = pil_image1.resize((x, y), Image.ANTIALIAS) #Tamanho da imagem
image_1.save('testes/tras.png')
tk_image1 = ImageTk.PhotoImage(image_1)
botao1 = tk.Button(janela_uso_manual)
botao1.config(image=tk_image1, command=EventoBotao2, compound="right",  borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao1.place(x=185, y=100)

#Botao Esquerda
pil_image2 = Image.open('testes/esquerda.png')
image_2 = pil_image2.resize((x, y), Image.ANTIALIAS) #Tamanho da imagem
image_2.save('testes/esquerda.png')
tk_image2 = ImageTk.PhotoImage(image_2)
botao2 = tk.Button(janela_uso_manual)
botao2.config(image=tk_image2, command=EventoBotao3, compound="right",  borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao2.place(x=300, y=100)

#Botao Direita
pil_image3 = Image.open('testes/direita.png')
image_3 = pil_image3.resize((x, y), Image.ANTIALIAS) #Tamanho da imagem
image_3.save('testes/direita.png')
tk_image3 = ImageTk.PhotoImage(image_3)
botao3 = tk.Button(janela_uso_manual)
botao3.config(image=tk_image3, command=EventoBotao4, compound="right", borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao3.place(x=130, y=160)

#Botao Parar
pil_image4 = Image.open('testes/parar.png')
image_4 = pil_image4.resize((x, y), Image.ANTIALIAS) #Tamanho da imagem
image_4.save('testes/parar.png')
tk_image4 = ImageTk.PhotoImage(image_4)
botao4 = tk.Button(janela_uso_manual)
botao4.config(image=tk_image4, command=EventoBotao5, compound="right", borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao4.place(x=245, y=160)


#Mostrando imagem bot_teste
pil_image5 = Image.open('uso_manual/menu.png')
image_5 = pil_image5.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_5.save('uso_manual/menu.png')
tk_image5 = ImageTk.PhotoImage(image_5)
botao5 = tk.Button(janela_uso_manual)
botao5.config(image=tk_image5, compound="right", command=janela_menu, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao5.place(x=10, y=10)

pil_image6 = Image.open('uso_manual/game.png')
image_6 = pil_image6.resize((30, 30), Image.ANTIALIAS) #Tamanho da imagem
image_6.save('uso_manual/game.png')
tk_image6 = ImageTk.PhotoImage(image_6)
image = canvas.create_image(10, 10, anchor=tk.NW, image=tk_image6)
canvas.move(image, 5, 250)

font = font.Font(root=janela_uso_manual, size=15, family="Laksaman",weight="bold")

label8 = tk.Label(text="Você escolheu controlar o carrinho manualmente,", fg='black', bg=cinza, font=("Laksaman", 10) )
label8.place(x=90, y=250)

label11 = tk.Label(text="por isso, não é necessário utilizar o capacete.", fg='black', bg=cinza, font=("Laksaman", 10)  )
label11.place(x=110, y=270)

label9 = tk.Label(text="Acione as saídas a partir da", fg='black', bg=cinza, font=font)
label9.place(x=70, y=20)

label10 = tk.Label(text="Interface", fg='orange', bg=cinza, font=font)
label10.place(x=340, y=20)

janela_uso_manual.protocol('WM_DELETE_WINDOW', FinalizaPrograma)

janela_uso_manual.mainloop()
