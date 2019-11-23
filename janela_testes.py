"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de testes
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import sys, os

#Criando a janela do menu
cinza = '#d3d3d3'
janela_testes = tk.Tk()
janela_testes.title("Testes")
janela_testes.configure(bg=cinza)
width=480
height=320
screen_width = janela_testes.winfo_screenwidth()
screen_height = janela_testes.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_testes.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_testes , width=480, height=320,bg=cinza)
canvas.pack()

                        
def abrir_janela_menu():
    janela_testes.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_menu.py')
    sys.exit()

def iniciar_demo():
    from treinamento_RNA_testes_DEMO import treinar_melhor_rede
    re = treinar_melhor_rede(60)    
    
respostas_positivas = [] #Armazena os testes que deram certo
respostas_negativas = [] #Armazena os testes que deram errado
contar_res = [0] #Conta quantos testes o usuario fez
chance = [3] #Quantidade de testes possiveis

print(contar_res)

def abrir_janela_uso_automatico():
            #---------------- Abre o arquivo com os dados do melhor treinamento  ----------------------#
    quant_elementos = 33
    dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
    for i in range(len(dados_melhor_treinamento)):
            coluna = dados_melhor_treinamento[i].split(";")
    print(coluna[5])
    if contar_res[0] >= int(coluna[5]):  #Verificando se o usuario fez todos os testes foram executados com sucesso
        if len(respostas_positivas) >= int(coluna[5]):
            print("Testes que deram errado: ")
            print(respostas_negativas)
            print("Testes que deram certo: ")
            print(respostas_positivas)
            janela_testes.destroy()
            os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_uso_automatico.py')
            sys.exit()
            
        else:
            if chance[0] <= 3 and chance[0] >=1:
                print("Total de chances: " + str(chance[0]))
                label2 = tk.Label(text="Os testes não foram executados com sucesso, tente novamente.", fg='red', bg=cinza, font=("Helvetica",10))
                label3 = tk.Label(text="Total de chances: "+str(chance[0]), fg='red', bg=cinza, font=("Helvetica",10))
                label2.place(x=40, y=270)
                label3.place(x=175, y=290)
                label4 = tk.Label(text="Teste todos os movimentos antes de seguir para a proxima etapa.", fg=cinza, bg=cinza, font=("Helvetica",10))
                label4.place(x=320, y=490)
                #Novo teste
                chance[0] = chance[0] - 1
                del respostas_positivas[0:len(respostas_positivas)]
                del respostas_negativas[0:len(respostas_negativas)]
                contar_res[0] = 0
                print(respostas_positivas)
                print(respostas_negativas)
                
            else: #Caso ele tenha que coletar os dados novamente, um novo diretorio devera sera ser criado com as informacoes
                label5 = tk.Label(text="Os testes não foram executados com sucesso, inicie as coletas novamente.", fg='red', bg=cinza, font=("Helvetica",10))
                label5.place(x=50, y=270)
                label4 = tk.Label(text="Teste todos os movimentos antes de seguir para a proxima etapa.", fg=cinza, bg=cinza, font=("Helvetica",10))
                label4.place(x=40, y=270)
                print("A RNA nao foi treinada com sucesso, sendo necessario coletar novos dados")
                
                #Criando novos diretorios
                #Conta o numero do arquivo 
                nome_dir = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
                for i in range(len(nome_dir)):
                        coluna = nome_dir[i].split(";")

                diretorio = coluna[0]   
                
                #Criando novos diretorios
                os.chdir("/home/diana/diana_testes/rede_coletas")
                caminho  = "/home/diana/diana_testes/rede_coletas/med_"+diretorio
                shutil.rmtree(caminho)

                
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
                
    else:
        label4 = tk.Label(text="Teste todos os movimentos antes de seguir para a proxima etapa.", fg='red', bg=cinza, font=("Helvetica",10))
        label4.place(x=40, y=270)
        label2 = tk.Label(text="Total de chances: "+str(chance[0]), fg='red', bg=cinza, font=("Helvetica",10))
        label2.place(x=500, y=500)
        
        

def abrir_janela_testes():
    janela_testes.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_testes.py')
    sys.exit()

def abrir_janela_coletas():
    janela_testes.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_coletas.py')
    sys.exit()
    
#Testando os movimentos (eventos)
def testar():

        #---------------- Abre o arquivo com os dados do melhor treinamento  ----------------------#
    quant_elementos = 33
    dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
    for i in range(len(dados_melhor_treinamento)):
            coluna = dados_melhor_treinamento[i].split(";")
                
    from modelo_RNA_testes_uso_joy import aplicar_modelo
    re = aplicar_modelo(5) #Tempo de cada teste

    #Gravando a quantidade de classificações
    for p in range(len(re)):
                coluna[27+p]  = re[p]

    dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
    [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
    dados_melhor_treinamento.write(str(coluna[quant_elementos]))
    dados_melhor_treinamento.close()
                
    janela_testes.destroy()
    os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_classifica.py')
    sys.exit()


#Respostas do usuario apos o teste
def frente_sim():
    if ("frente" not in respostas_negativas) and ("frente" not in respostas_positivas): #Faz com o que o usuario possa salvar apenas a primeira resposta
        contar_res[0] =  contar_res[0] + 1
        respostas_positivas.append("frente")
        print(respostas_positivas)
        print(contar_res[0])
    
def frente_nao():
     if ("frente" not in respostas_positivas) and ("frente" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_negativas.append("frente")


def tras_sim():
     if ("tras" not in respostas_negativas) and ("tras" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_positivas.append("tras")
        print(respostas_positivas)
        print(contar_res[0])
    
def tras_nao():
     if ("tras" not in respostas_negativas) and ("tras" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_negativas.append("tras")
        
def esquerda_sim():
     if ("esquerda" not in respostas_negativas) and ("esquerda" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_positivas.append("esquerda")
        print(respostas_positivas)
        print(contar_res[0])
    
def esquerda_nao():
    if ("esquerda" not in respostas_negativas) and ("esquerda" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_negativas.append("esquerda")

def direita_sim():
    if ("direita" not in respostas_negativas) and ("direita" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_positivas.append("direita")
        print(respostas_positivas)
        print(contar_res[0])
    
def direita_nao():
    if ("direita" not in respostas_negativas) and ("direita" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_negativas.append("direita")

def parar_sim():
    if ("parar" not in respostas_negativas) and ("parar" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_positivas.append("parar")
        print(respostas_positivas)
        print(contar_res[0])
    
def parar_nao():
    if ("parar" not in respostas_negativas) and ("parar" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_negativas.append("parar")

def ligar_sim():
    if ("ligar" not in respostas_negativas) and ("ligar" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_positivas.append("ligar")
        print(respostas_positivas)
        print(contar_res[0])
    
def ligar_nao():
    if ("ligar" not in respostas_negativas) and ("ligar" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_negativas.append("ligar")

def neutro_sim():
    if ("neutro" not in respostas_negativas) and ("neutro" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_positivas.append("neutro")
        print(respostas_positivas)
        print(contar_res[0])
    
def neutro_nao():
    if ("neutro" not in respostas_negativas) and ("neutro" not in respostas_positivas):
        contar_res[0] = contar_res[0] + 1
        respostas_negativas.append("neutro")

    

os.chdir("/home/diana/diana_testes/config_tela/")
#Mostrando imagem bot_teste
pil_image0 = Image.open('testes/frente.png')
image_0 = pil_image0.resize((90, 40), Image.ANTIALIAS) #Tamanho da imagem
image_0.save('testes/frente.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_testes)
botao0.config(image=tk_image0, compound="right", command=testar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=30, y=80)


#Mostrando imagem bot_teste
pil_image1 = Image.open('testes/tras.png')
image_1 = pil_image1.resize((90, 40), Image.ANTIALIAS) #Tamanho da imagem
image_1.save('testes/tras.png')
tk_image1 = ImageTk.PhotoImage(image_1)
botao1 = tk.Button(janela_testes)
botao1.config(image=tk_image1, compound="right", command=testar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao1.place(x=140, y=80)

#Mostrando imagem bot_teste
pil_image2 = Image.open('testes/esquerda.png')
image_2 = pil_image2.resize((90, 41), Image.ANTIALIAS) #Tamanho da imagem
image_2.save('testes/esquerda.png')
tk_image2 = ImageTk.PhotoImage(image_2)
botao2 = tk.Button(janela_testes)
botao2.config(image=tk_image2, compound="right", command=testar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao2.place(x=250, y=79)

#Mostrando imagem bot_teste
pil_image3 = Image.open('testes/direita.png')
image_3 = pil_image3.resize((90, 41), Image.ANTIALIAS) #Tamanho da imagem
image_3.save('testes/direita.png')
tk_image3 = ImageTk.PhotoImage(image_3)
botao3 = tk.Button(janela_testes)
botao3.config(image=tk_image3, compound="right", command=testar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao3.place(x=360, y=79)

#Mostrando imagem bot_teste
pil_image4 = Image.open('testes/ligar.png')
image_4 = pil_image4.resize((90, 41), Image.ANTIALIAS) #Tamanho da imagem
image_4.save('testes/ligar.png')
tk_image4 = ImageTk.PhotoImage(image_4)
botao4 = tk.Button(janela_testes)
botao4.config(image=tk_image4, compound="right", command=testar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao4.place(x=80, y=179)

#Mostrando imagem bot_teste
pil_image5 = Image.open('testes/parar.png')
image_5 = pil_image5.resize((90, 41), Image.ANTIALIAS) #Tamanho da imagem
image_5.save('testes/parar.png')
tk_image5 = ImageTk.PhotoImage(image_5)
botao5 = tk.Button(janela_testes)
botao5.config(image=tk_image5, compound="right", command=testar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao5.place(x=200, y=179)

#Mostrando imagem bot_teste
pil_image6 = Image.open('testes/neutro.png')
image_6 = pil_image6.resize((90, 41), Image.ANTIALIAS) #Tamanho da imagem
image_6.save('testes/neutro.png')
tk_image6 = ImageTk.PhotoImage(image_6)
botao6 = tk.Button(janela_testes)
botao6.config(image=tk_image6, compound="right", command=testar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao6.place(x=320, y=179)

#Mostrando imagem bot_teste
pil_image7 = Image.open('testes/ir.png')
image_7 = pil_image7.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_7.save('testes/ir.png')
tk_image7 = ImageTk.PhotoImage(image_7)
botao7 = tk.Button(janela_testes)
botao7.config(image=tk_image7, compound="right", command=abrir_janela_uso_automatico, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao7.place(x=425, y=260)

#Mostrando imagem bot_teste
pil_image8 = Image.open('testes/voltar.png')
image_8 = pil_image8.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_8.save('testes/voltar.png')
tk_image8 = ImageTk.PhotoImage(image_8)
botao8 = tk.Button(janela_testes)
botao8.config(image=tk_image8, compound="right", command=abrir_janela_coletas, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao8.place(x=0, y=260)

#Mostrando imagem bot_teste
pil_image9 = Image.open('testes/menu.png')
image_9 = pil_image9.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_9.save('testes/menu.png')
tk_image9 = ImageTk.PhotoImage(image_9)
botao9 = tk.Button(janela_testes)
botao9.config(image=tk_image9, compound="right", command=abrir_janela_menu, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao9.place(x= 10, y=10)

#Chamando os botoes "sim" e "nao"
#SIM E NAO para o Neutro 
pil_image10 = Image.open('testes/sim.png')
image_10 = pil_image10.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_10.save('testes/sim.png')
tk_image10 = ImageTk.PhotoImage(image_10)
botao10 = tk.Button(janela_testes)
botao10.config(image=tk_image10, compound="right", command = neutro_sim, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao10.place(x=325, y= 225)

pil_image11 = Image.open('testes/nao.png')
image_11 = pil_image11.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_11.save('testes/nao.png')
tk_image11 = ImageTk.PhotoImage(image_11)
botao11 = tk.Button(janela_testes)
botao11.config(image=tk_image11, compound="right", command = neutro_nao, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao11.place(x=365, y= 225)

#SIM E NAO (ENTRADA 6)
pil_image12 = Image.open('testes/nao.png')
image_12 = pil_image12.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_12.save('testes/nao.png')
tk_image12 = ImageTk.PhotoImage(image_12)
botao12 = tk.Button(janela_testes)
botao12.config(image=tk_image12, compound="right", command = ligar_nao, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao12.place(x=245, y= 225)

pil_image13 = Image.open('testes/sim.png')
image_13 = pil_image13.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_13.save('testes/sim.png')
tk_image13 = ImageTk.PhotoImage(image_13)
botao13 = tk.Button(janela_testes)
botao13.config(image=tk_image13, compound="right", command = ligar_sim, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao13.place(x=205, y= 225)

#SIM E NAO (ENTRADA 5)
pil_image14 = Image.open('testes/nao.png')
image_14 = pil_image14.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_14.save('testes/nao.png')
tk_image14 = ImageTk.PhotoImage(image_14)
botao14 = tk.Button(janela_testes)
botao14.config(image=tk_image14, compound="right", command = parar_nao, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao14.place(x=125, y= 225)

pil_image15 = Image.open('testes/sim.png')
image_15 = pil_image15.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_15.save('testes/sim.png')
tk_image15 = ImageTk.PhotoImage(image_15)
botao15 = tk.Button(janela_testes)
botao15.config(image=tk_image15, compound="right", command = parar_sim, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao15.place(x=85, y= 225)

#SIM E NAO (ENTRADA 4)
pil_image16 = Image.open('testes/nao.png')
image_16 = pil_image16.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_16.save('testes/nao.png')
tk_image16 = ImageTk.PhotoImage(image_16)
botao16 = tk.Button(janela_testes)
botao16.config(image=tk_image16, compound="right", command = direita_nao, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao16.place(x=405, y= 125)

pil_image17 = Image.open('testes/sim.png')
image_17 = pil_image17.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_17.save('testes/sim.png')
tk_image17 = ImageTk.PhotoImage(image_17)
botao17 = tk.Button(janela_testes)
botao17.config(image=tk_image17, compound="right", command = direita_sim, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao17.place(x=365, y= 125)

#SIM E NAO (ENTRADA 3)
pil_image18 = Image.open('testes/nao.png')
image_18 = pil_image18.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_18.save('testes/nao.png')
tk_image18 = ImageTk.PhotoImage(image_18)
botao18 = tk.Button(janela_testes)
botao18.config(image=tk_image18, compound="right", command = esquerda_nao, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao18.place(x=295, y= 125)

pil_image19 = Image.open('testes/sim.png')
image_19 = pil_image19.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_19.save('testes/sim.png')
tk_image19 = ImageTk.PhotoImage(image_19)
botao19 = tk.Button(janela_testes)
botao19.config(image=tk_image19, compound="right", command = esquerda_sim, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao19.place(x=255, y= 125)

#SIM E NAO (ENTRADA 2)
pil_image20 = Image.open('testes/nao.png')
image_20= pil_image20.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_20.save('testes/nao.png')
tk_image20 = ImageTk.PhotoImage(image_20)
botao20 = tk.Button(janela_testes)
botao20.config(image=tk_image20, compound="right", command = tras_nao, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao20.place(x=185, y= 125)

pil_image21 = Image.open('testes/sim.png')
image_21= pil_image21.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_21.save('testes/sim.png')
tk_image21 = ImageTk.PhotoImage(image_21)
botao21 = tk.Button(janela_testes)
botao21.config(image=tk_image21, compound="right", command = tras_sim, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao21.place(x=145, y= 125)

#SIM E NAO (ENTRADA 1) 
pil_image22 = Image.open('testes/nao.png')
image_22= pil_image22.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_22.save('testes/nao.png')
tk_image22 = ImageTk.PhotoImage(image_22)
botao22 = tk.Button(janela_testes)
botao22.config(image=tk_image22, compound="right", command = frente_nao, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao22.place(x=75, y= 125)

pil_image23 = Image.open('testes/sim.png')
image_23= pil_image23.resize((40, 30), Image.ANTIALIAS) #Tamanho da imagem
image_23.save('testes/sim.png')
tk_image23 = ImageTk.PhotoImage(image_23)
botao23 = tk.Button(janela_testes)
botao23.config(image=tk_image23, compound="right", command = frente_sim, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao23.place(x=35, y= 125)

label1 = tk.Label(text="Teste a", fg='black', bg=cinza,  font=("Helvetica 20 bold",15)  )
label1.place(x=90, y=20)

label1 = tk.Label(text="RNA", fg='#7b68ee', bg=cinza,  font=("Helvetica 20 bold",15)  )
label1.place(x=170, y=20)

label2 = tk.Label(text="para os movimentos ", fg='black', bg=cinza, font=("Helvetica 20 bold",15) )
label2.place(x=220, y=20)

janela_testes.mainloop()
