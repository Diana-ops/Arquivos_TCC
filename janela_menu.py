"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela principal
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import sys
import os

#Criando a janela do menu
janela_menu = tk.Tk()
janela_menu.title("Interface - Usuario - Menu")
janela_menu.configure(bg='white')
width=480
height=320
screen_width = janela_menu.winfo_screenwidth()
screen_height = janela_menu.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_menu.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_menu , width=480, height=320,bg="white")
canvas.pack()

def janela_instrucoes(): #Para comecar a configurar o dispositivo
    janela_menu.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_instrucoes.py')
    sys.exit()

def janela_testes():
    janela_menu.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_testes.py')
    sys.exit()
    
def janela_uso_automatico():
    janela_menu.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_uso_automatico.py')
    sys.exit()

def janela_uso_manual():
    janela_menu.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_uso_manual_v0.py')
    sys.exit()

"""
def janela_uso_braco():
    janela_menu.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_braco.py')
    sys.exit()
"""
    
x1 = 120
x2 = 0
x3 = x1+120
x4 = x3+120
y= 0

h = 120
v = 320
 
#Mostrando imagem bot_teste
pil_image0 = Image.open('menu/bot_teste.png')
image_0 = pil_image0.resize((h, v), Image.ANTIALIAS) #Tamanho da imagem
image_0.save('menu/bot_teste.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_menu )
botao0.config(image=tk_image0, compound="right", command=janela_testes, borderwidth=0,highlightbackground='white')
botao0.place(x=x1, y=y)

#Mostrando imagem bot_configuracao
pil_image1 = Image.open('menu/bot_config.png')
image_1 = pil_image1.resize((h, v), Image.ANTIALIAS) #Tamanho da imagem
image_1.save('menu/bot_config.png')
tk_image1 = ImageTk.PhotoImage(image_1)
botao1 = tk.Button(janela_menu)
botao1.config(image=tk_image1, compound="right", command=janela_instrucoes, borderwidth=0,highlightbackground='white')
botao1.place(x=x2, y=y)

#Mostrando imagem bot_uso_automatico
pil_image2 = Image.open('menu/bot_uso_automatico.png')
image_2 = pil_image2.resize((h, v), Image.ANTIALIAS) #Tamanho da imagem
image_2.save('menu/bot_uso_automatico.png')
tk_image2 = ImageTk.PhotoImage(image_2)
botao2 = tk.Button(janela_menu )
botao2.config(image=tk_image2, compound="right", command=janela_uso_automatico, borderwidth=0,highlightbackground='white')
botao2.place(x=x3, y=y)

#Mostrando imagem bot_uso_manual
pil_image3 = Image.open('menu/bot_uso_manual_padrao.png')
image_3 = pil_image3.resize((h, v), Image.ANTIALIAS) #Tamanho da imagem
image_3.save('menu/bot_uso_manual.png')
tk_image3 = ImageTk.PhotoImage(image_3)
botao3 = tk.Button(janela_menu)
botao3.config(image=tk_image3, compound="right", command=janela_uso_manual, borderwidth=0,highlightbackground='white')
botao3.place(x=x4, y=y)

"""
#Mostrando imagem bot_controle_braco
pil_image4 = Image.open('menu/bot_controle_braco.png')
image_4 = pil_image4.resize((120, 160), Image.ANTIALIAS) #Tamanho da imagem
image_4.save('menu/bot_controle_braco.png')
tk_image4 = ImageTk.PhotoImage(image_4)
botao4 = tk.Button(janela_menu)
botao4.config(image=tk_image4, compound="right", command=janela_uso_braco, borderwidth=0,highlightbackground='white')
botao4.place(x=x4, y=160)
"""
janela_menu.mainloop()
