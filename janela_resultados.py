"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de resultados - Apresentação do melhor desempenho da RNA
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import sys, os, shutil
from tkinter import font
import os.path

#---------------- Construção Base da Interface ----------------------#
aumento = 70
cinza = '#ededed'
roxo = '#606'
azul_escuro = '#084d6e'

janela_resultados = tk.Tk()
janela_resultados.title("Resultados RNA")
janela_resultados.configure(bg=cinza)
width=480+aumento
height=320+aumento
screen_width = janela_resultados.winfo_screenwidth()
screen_height = janela_resultados.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_resultados.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_resultados , width=480+aumento, height=380+aumento,bg=cinza)
canvas.pack()
trilha = "/home/diana/diana_testes/config_tela/"
    
dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
for i in range(len(dados_melhor_treinamento)):
        coluna = dados_melhor_treinamento[i].split(";")

quant_elementos = 33
dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
[dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
dados_melhor_treinamento.write(str(coluna[quant_elementos]))
dados_melhor_treinamento.close()

diretorio = coluna[0]

# ------------------ FUNÇÕES ------------------ #
        
def excluir_ultima_coletas():
        caminho  = "/home/diana/diana_testes/rede_coletas/med_"+diretorio
        
        walk_brutos = caminho+"/treinamento_normalizados_med_"+diretorio+"/"
        
        pasta_brutos = os.listdir(walk_brutos)
        
        #Saidas possíveis 
        saidas = ["frente", "tras", "esquerda","direita", "ligar", "parar","neutro"]
        saidas.sort()
            
        dic = [] #Armazenará somente o nome das saidas que existem no diretorio

        #Abrindo diretório de dados brutos para treinamento e teste
        walk_past = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/brutos_med_"+diretorio+"/"
        pasta = os.listdir(walk_past)

        #Buscando as saidas existentes no meu diretorio 
        for i in range(len(pasta)):
                for s in range(len(saidas)):
                    if pasta[i].find(str(saidas[s])) == 0 and saidas[s].split("_")[0] not in dic:
                        dic.append(str(saidas[s].split("_")[0]))
                        if os.path.exists(walk_past+str(saidas[s])+"_"+str(coluna[6+s])+".csv"):
                                os.remove(walk_past+str(saidas[s])+"_"+str(coluna[6+s])+".csv")
                

        
def descartar_coletas():

        #Criando novos diretorios
        os.chdir("/home/diana/diana_testes/rede_coletas")
        #caminho  = "/home/diana/diana_testes/rede_coletas/med_"+diretorio
        #shutil.rmtree(caminho)
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
        for i in range(len(dados_melhor_treinamento)):
                coluna = dados_melhor_treinamento[i].split(";")

        coluna[0] = int(coluna[0]) + 1
        os.mkdir("med_"+str(coluna[0])) #Cria novo diretorio
        os.chdir("med_"+str(coluna[0])) #Entra neste diretório

        os.mkdir("brutos_med_"+str(coluna[0])) #Diretorio dos dados brutos (treinamento e teste)
        os.mkdir("valida_brutos_med_"+str(coluna[0])) #Diretorio dos dados brutos (validação)
                        
        os.mkdir("teste_normalizados_med_"+str(coluna[0])) #Diretorio dos dados normalizados (treinamento)
        os.mkdir("treinamento_normalizados_med_"+str(coluna[0])) #Diretorio dos dados normalizados (teste)
        os.mkdir("valida_normalizados_med_"+str(coluna[0])) #Diretorio dos dados normalizados (validação)
        os.mkdir("relatorios_med_"+str(coluna[0])) #Diretorio dos relatórios

        os.chdir("relatorios_med_"+str(coluna[0])) #Entra neste diretório
        os.mkdir("graficos_med_"+str(coluna[0])) #Diretorio dos gráficos
        
        os.chdir("graficos_med_"+str(coluna[0])) #Entra neste diretório
        os.mkdir("graf_norm") #Graficos normalizados
        os.mkdir("graf_filtrados") #Graficos filtrados

        quant_elementos = 33
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()
        
def voltar():
    janela_resultados.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_coletas.py')
    sys.exit()
        
# -------------------------------------------------- #

        
font = font.Font(root=janela_resultados, size=10, family="Laksaman",weight="bold")

distancia_linha = 10
pula = 30
# --------------------------------------------------------------------------- #

label0 = tk.Label(text="Quantidade de dados coletados:", fg=azul_escuro, bg=cinza, font=font)
label0.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label1 = tk.Label(text="Frente:  "+str(coluna[15])+"\tDireita:  "+str(coluna[13]), fg='black', bg=cinza, font=font)
label1.place(x=10, y=distancia_linha)
# Direita - 13, Esquerda - 14, Frente - 15, Ligar - 16, Neutro - 17, Parar - 18, Tras - 19

distancia_linha = distancia_linha + pula

label2 = tk.Label(text="Trás:  "+str(coluna[19])+"\tLigar: "+str(coluna[16]), fg='black', bg=cinza, font=font)
label2.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label3 = tk.Label(text="Esquerda:  "+str(coluna[14])+"\tParar: "+str(coluna[18]), fg='black', bg=cinza, font=font)
label3.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label4 = tk.Label(text="Neutro:  "+str(coluna[17]), fg='black', bg=cinza, font=font)
label4.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label5 = tk.Label(text="Total:  "+str(coluna[20]), fg='black', bg=cinza, font=font)
label5.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + 40

# --------------------------------------------------------------------------- #
label6 = tk.Label(text="Quantidade de dados usados pela RNA:", fg=azul_escuro, bg=cinza, font=font )
label6.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label7 = tk.Label(text="Treinamento:  "+str(coluna[21]), fg='black', bg=cinza, font=font)
label7.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label8 = tk.Label(text="Teste:  "+str(coluna[22]), fg='black', bg=cinza, font=font)
label8.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label9 = tk.Label(text="Validação:  "+str(coluna[23]), fg='black', bg=cinza, font=font)
label9.place(x=10, y=distancia_linha)

distancia_linha = distancia_linha + pula

label20 = tk.Label(text="Quantidade de Saídas: "+str(coluna[5]), fg="black", bg=cinza, font=font)
label20.place(x=30, y=distancia_linha+20)

label17 = tk.Label(text="Para mais informações, consulte a", fg='black', bg=cinza, font=font)
label17.place(x=300, y=distancia_linha)

distancia_linha = distancia_linha + 27

label17 = tk.Label(text="documentação do projeto.", fg=azul_escuro, bg=cinza, font=font)
label17.place(x=320, y=distancia_linha)


distancia_linha = distancia_linha + pula
# --------------------------------------------------------------------------- #
x = 300
distancia_linha = 10

label11 = tk.Label(text="Melhor Desempenho da RNA", fg=roxo, bg=cinza, font=font )
label11.place(x=x, y=distancia_linha)

distancia_linha = distancia_linha + pula

label12 = tk.Label(text="Filtro dos Dados:  "+str(coluna[1]), fg='black', bg=cinza, font=font)
label12.place(x=x, y=distancia_linha)

distancia_linha = distancia_linha + pula

label13 = tk.Label(text="Número de Camadas:  "+str(coluna[4]), fg='black', bg=cinza, font=font)
label13.place(x=x, y=distancia_linha)

distancia_linha = distancia_linha + pula

label14 = tk.Label(text="Treinamento:  "+str(coluna[24]) + " %", fg='black', bg=cinza, font=font)
label14.place(x=x, y=distancia_linha)

distancia_linha = distancia_linha + pula

label15 = tk.Label(text="Teste:  "+str(coluna[25]) + " %", fg='black', bg=cinza, font=font)
label15.place(x=x, y=distancia_linha)

distancia_linha = distancia_linha + pula

label16 = tk.Label(text="Valida:  "+str(coluna[26]) + " %", fg='black', bg=cinza, font=font)
label16.place(x=x, y=distancia_linha)
# --------------------------------------------------------------------------- #
def janela_coletas():
        return
pil_image0 = Image.open(trilha+'resultados_RNA/sair.png')
image_0 = pil_image0.resize((30, 30), Image.ANTIALIAS) #Tamanho da imagem
image_0.save(trilha+'resultados_RNA/sair.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_resultados)
botao0.config(image=tk_image0, compound="right", command=voltar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=500, y= 10)

#Tamanho dos botões 
x = 130
y = 40

distancia_linha = distancia_linha + pula

pil_image1 = Image.open(trilha+'resultados_RNA/manter_dados.png')
image_1 = pil_image1.resize((x, y), Image.ANTIALIAS) #Tamanho da imagem
image_1.save(trilha+'resultados_RNA/manter_dados.png')
tk_image1 = ImageTk.PhotoImage(image_1)
botao1 = tk.Button(janela_resultados)
botao1.config(image=tk_image1, compound="right", command=janela_coletas, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao1.place(x=340, y=200)

pil_image3 = Image.open(trilha+'resultados_RNA/excluir_ultima_coleta.png')
image_3 = pil_image3.resize((x+20, y), Image.ANTIALIAS) #Tamanho da imagem
image_3.save(trilha+'resultados_RNA/excluir_ultima_coleta.png')
tk_image3 = ImageTk.PhotoImage(image_3)
botao3 = tk.Button(janela_resultados)
botao3.config(image=tk_image3, compound="right", command=excluir_ultima_coletas, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao3.place(x=330, y=240)

pil_image4 = Image.open(trilha+'resultados_RNA/descartar_coletas.png')
image_4 = pil_image4.resize((x+15, y), Image.ANTIALIAS) #Tamanho da imagem
image_4.save(trilha+'resultados_RNA/descartar_coleta.png')
tk_image4 = ImageTk.PhotoImage(image_4)
botao4 = tk.Button(janela_resultados)
botao4.config(image=tk_image4, compound="right", command=descartar_coletas, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao4.place(x=335, y=280)

janela_resultados.mainloop()
dados_melhor_treinamento.close()
