"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de classificações - Resultado do teste para o usuário
"""

from PIL import Image
import tkinter as tk
from PIL import ImageTk
import sys
import os
from tkinter import font

#Criando a janela do menu
cinza = '#d3d3d3'
roxo = '#606'
azul_escuro = '#084d6e'

janela_classifica = tk.Tk()
janela_classifica.title("Resultados - Classificações")
janela_classifica.configure(bg=cinza)
width=280
height=280
screen_width = janela_classifica.winfo_screenwidth()
screen_height = janela_classifica.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_classifica.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_classifica , width=280, height=280,bg=cinza)
canvas.pack()

trilha = "/home/diana/diana_testes/config_tela/"

font = font.Font(root=janela_classifica, size=10, family="Laksaman",weight="bold")

        
dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
for i in range(len(dados_melhor_treinamento)):
            resultados = dados_melhor_treinamento[i].split(";")

def voltar():
    janela_classifica.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_testes.py')
    sys.exit()
        

pil_image0 = Image.open(trilha+'resultados_RNA/sair.png')
image_0 = pil_image0.resize((30, 30), Image.ANTIALIAS) #Tamanho da imagem
image_0.save(trilha+'resultados_RNA/sair.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_classifica)
botao0.config(image=tk_image0, compound="right", command=voltar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=230, y= 10)

    

label1 = tk.Label(text="Resultados: ", fg=azul_escuro, bg=cinza, font=font)
label1.place(x=90, y=20)

label2 = tk.Label(text="Classificação de cada saída: ", fg=roxo, bg=cinza, font=font)
label2.place(x=45, y=50)
     
label3 = tk.Label(text="Frente: "+str(resultados[29]), fg="black", bg=cinza, font=font)
label3.place(x=90, y=100) #29 - posição no arquivo

label4 = tk.Label(text="Trás: "+str(resultados[33]), fg="black", bg=cinza, font=font)
label4.place(x=90, y=120) #33

label5 = tk.Label(text="Esquerda: "+str(resultados[28]), fg="black", bg=cinza, font=font)
label5.place(x=90, y=140) #28

label6 = tk.Label(text="Direita: "+str(resultados[27]), fg="black", bg=cinza, font=font)
label6.place(x=90, y=160) #27

label7 = tk.Label(text="Parar: "+str(resultados[32]), fg="black", bg=cinza, font=font)
label7.place(x=90, y=180) #32

label8 = tk.Label(text="Ligar: "+str(resultados[30]), fg="black", bg=cinza, font=font)
label8.place(x=90, y=200) #30

label9 = tk.Label(text="Neutro: "+str(resultados[31]), fg="black", bg=cinza, font=font)
label9.place(x=90, y=220) #31

janela_classifica.mainloop()

