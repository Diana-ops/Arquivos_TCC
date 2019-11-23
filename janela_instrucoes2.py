"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de instruções (parte 2)
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import os, sys
from tkinter import font

cinza = '#d3d3d3'
janela_instrucoes2 = tk.Tk()
janela_instrucoes2.title("Instruções")
janela_instrucoes2.configure(bg=cinza)
width=480
height=320
screen_width = janela_instrucoes2.winfo_screenwidth()
screen_height = janela_instrucoes2.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_instrucoes2.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_instrucoes2 , width=480, height=320,bg=cinza)
canvas.pack()

def janela_coletas():
    janela_instrucoes2.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_coletas.py')
    sys.exit()

def janela_menu():
    janela_instrucoes2.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_menu.py')
    sys.exit()

def janela_instrucoes(): #Voltar para as instrucoes
    janela_instrucoes2.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_instrucoes.py')
    sys.exit()

#Mostrando imagem texto_1
trilha = "/home/diana/diana_testes/config_tela/"
pil_image0 = Image.open(trilha+'instrucoes/menu.png')
image_0 = pil_image0.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_0.save(trilha+'instrucoes/menu.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_instrucoes2)
botao0.config(image=tk_image0, compound="right", command=janela_menu, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=10, y=10)

pil_image1 = Image.open(trilha+'instrucoes/instrucoes2.png')
image_1 = pil_image1.resize((410, 240), Image.ANTIALIAS) #Tamanho da imagem
image_1.save(trilha+'instrucoes/instrucoes2.png')
tk_image1 = ImageTk.PhotoImage(image_1)
image = canvas.create_image(10, 10, anchor=tk.NW, image=tk_image1)
canvas.move(image,  10, 50)

#Mostrando imagem de confirmaçãao
pil_image2 = Image.open(trilha+'instrucoes/ir.png')
image_2 = pil_image2.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_2.save(trilha+'instrucoes/ir.png')
tk_image2 = ImageTk.PhotoImage(image_2)
botao0 = tk.Button(janela_instrucoes2)
botao0.config(image=tk_image2, compound="right", command=janela_coletas, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=430, y=240)

#Botao para ir para a janela de instrucoes
pil_image8 = Image.open(trilha+'coletas/voltar.png')
image_8 = pil_image8.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_8.save(trilha+'coletas/voltar.png')
tk_image8 = ImageTk.PhotoImage(image_8)
botao8 = tk.Button(janela_instrucoes2)
botao8.config(image=tk_image8, compound="right", command=janela_instrucoes, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao8.place(x=0, y=240)

font = font.Font(root=janela_instrucoes2, size=15, family="Laksaman",weight="bold")

label2 = tk.Label(text="Instruções para as ", fg='black', bg=cinza, font=font)
label2.place(x=105, y=10)

label3 = tk.Label(text="coletas", fg='#005580', bg=cinza, font=font)
label3.place(x=285, y=10)



janela_instrucoes2.mainloop()




