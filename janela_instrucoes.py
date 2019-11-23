"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de instruções (parte 1)
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import os, sys
from tkinter import font

cinza = '#d3d3d3'
janela_instrucoes = tk.Tk()
janela_instrucoes.title("Instruções")
janela_instrucoes.configure(bg=cinza)
width=480
height=320
screen_width = janela_instrucoes.winfo_screenwidth()
screen_height = janela_instrucoes.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_instrucoes.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_instrucoes , width=480, height=320,bg=cinza)
canvas.pack()

def janela_instrucoes2():
    janela_instrucoes.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_instrucoes2.py')
    sys.exit()

def janela_menu():
    janela_instrucoes.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_menu.py')
    sys.exit()

#Mostrando imagem texto_1
trilha = "/home/diana/diana_testes/config_tela/"
pil_image0 = Image.open(trilha+'instrucoes/menu.png')
image_0 = pil_image0.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_0.save(trilha+'instrucoes/menu.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_instrucoes)
botao0.config(image=tk_image0, compound="right", command=janela_menu, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=10, y=10)

pil_image1 = Image.open(trilha+'instrucoes/texto_instrucoes.png')
image_1 = pil_image1.resize((450, 280), Image.ANTIALIAS) #Tamanho da imagem
image_1.save(trilha+'instrucoes/texto_instrucoes.png')
tk_image1 = ImageTk.PhotoImage(image_1)
image = canvas.create_image(10, 10, anchor=tk.NW, image=tk_image1)
canvas.move(image, -10, 20)

#Mostrando imagem de confirmaçãao
pil_image2 = Image.open(trilha+'instrucoes/ir.png')
image_2 = pil_image2.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_2.save(trilha+'instrucoes/ir.png')
tk_image2 = ImageTk.PhotoImage(image_2)
botao0 = tk.Button(janela_instrucoes)
botao0.config(image=tk_image2, compound="right", command=janela_instrucoes2, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=410, y=250)

font = font.Font(root=janela_instrucoes, size=15, family="Laksaman",weight="bold")

label2 = tk.Label(text="Instruções para as ", fg='black', bg=cinza, font=font)
label2.place(x=105, y=10)

label3 = tk.Label(text="coletas", fg='#005580', bg=cinza, font=font)
label3.place(x=285, y=10)

"""
para_1 = "1. Coloque o capacete MindFlex"
para_2 = "como mostra a figura."

para_3 = "2. Ao selecionar uma opção,"
para_4 = "concentre-se em realizar um "
para_5 = "pensamento. "

para_6 = "3. Ao selecionar uma opção, se concentre em realizar um"
para_7 = "movimento ou pensar em seu nome."

para_8 = "      Depois de escolher outra opção, foque em algo"
para_9 = "diferente para que a RNA consiga diferenciar muito "
para_10 = "bem os comandos de acordo com o seu pensamento."


label4 = tk.Label(text=para_1 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label4.place(x=15, y=70)
label5 = tk.Label(text=para_2 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label5.place(x=15, y=90)

label6 = tk.Label(text=para_3 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label6.place(x=250, y=70)
label7 = tk.Label(text=para_4 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label7.place(x=250, y=90)
label8 = tk.Label(text=para_5 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label8.place(x=250, y=110)

label9 = tk.Label(text=para_6 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label9.place(x=15, y=200)
label10 = tk.Label(text=para_7 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label10.place(x=15, y=220)
label11 = tk.Label(text=para_8 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label11.place(x=15, y=245)
label12 = tk.Label(text=para_9 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label12.place(x=15, y=265)
label13 = tk.Label(text=para_10 , fg='black', bg=cinza, font=("Times 20 bold",10) )
label13.place(x=15, y=285)
"""

janela_instrucoes.mainloop()




