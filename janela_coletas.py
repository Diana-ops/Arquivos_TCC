"""
Instituição: Fatec Santo André - Mecatronica Industrial 
TCC: Sistema Automático para Coleta e Classificação de Ondas Cerebrais 
Autor: Diana Regina da Silva 
Descrição: Contrução da janela de coletas
"""
from PIL import Image
import tkinter as tk
from PIL import ImageTk
import sys, os, shutil

#---------------- Construção Base da Interface ----------------------#
cinza = '#d3d3d3'
janela_coletas = tk.Tk()
janela_coletas.title("Coletas")
janela_coletas.configure(bg=cinza)
width=480
height=320
screen_width = janela_coletas.winfo_screenwidth()
screen_height = janela_coletas.winfo_screenheight()
xCentro = (screen_width/2) - (width/2)
yCentro = (screen_height/2) - (height/2)
janela_coletas.geometry('%dx%d+%d+%d' % (width, height, xCentro, yCentro))
canvas = tk.Canvas(janela_coletas , width=480, height=320,bg=cinza)
canvas.pack()

#---------------- Direcionamento do usuário para outras janelas ----------------------#
def janela_menu(): #Ir para o menu
        janela_coletas.destroy()
        os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_menu.py')
        sys.exit()
    
def janela_instrucoes2(): #Voltar para as instrucoes
            janela_coletas.destroy()
            os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_instrucoes2.py')
            sys.exit()

def janela_resultados(): #Ir para o menu
        janela_coletas.destroy()
        os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_resultados.py')
        sys.exit()

"""
Variavel usada para confirmar se a RNA foi treinada com os dados coletados,
permitindo que o usuário tenha acesso a janela de testes
"""
def janela_testes(): #Seguir para os testes
        if int(coluna[21]) >= 12: #Se houve quant. minima para o treinamento, a RNA foi treinada
            janela_coletas.destroy()
            os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_testes.py')
            sys.exit()
        else:
                label5 = tk.Label(text="A RNA ainda não foi treinada.", fg='red', bg=cinza, font=("Helvetica",10))
                label5.place(x=150, y=280)
                
#---------------- Exclui todos os arquivos com os dados normalizados  ----------------------#    
def reiniciar(): 
        diretorio = coluna[0]
        caminho  = "/home/diana/diana_testes/rede_coletas/med_"+diretorio
        
        walk_norm = caminho+"/treinamento_normalizados_med_"+diretorio+"/"
        walk_norm_teste = caminho+"/teste_normalizados_med_"+diretorio+"/"
        
        pasta_norm = os.listdir(walk_norm)
        pasta_norm_teste = os.listdir(walk_norm_teste)

        #Excluindo os dados normalizados 
        [os.remove(walk_norm+pasta_norm[i]) for i in range(len(pasta_norm))]
        [os.remove(walk_norm_teste+pasta_norm_teste[i]) for i in range(len(pasta_norm_teste))]

#---------------- Exclui todos os gráficos de teste e treinamento  ----------------------#    
def excluir_graficos(): 
        diretorio = coluna[0]
        caminho  = "/home/diana/diana_testes/rede_coletas/med_"+diretorio+"/relatorios_med_"+diretorio+"/graficos_med_"+diretorio
        
        walk_treino = caminho+"/treinamento_med_"+diretorio+"/"
        walk_teste = caminho+"/testes_med_"+diretorio+"/"
        walk_puros = caminho+"/dados_puros_med_"+diretorio+"/"
        
        pasta_treino = os.listdir(walk_treino)
        pasta_teste = os.listdir(walk_teste)
        pasta_puros = os.listdir(walk_puros)

        #Excluindo gráficos 
        [os.remove(walk_treino+pasta_treino[i]) for i in range(len(pasta_treino))]
        [os.remove(walk_teste+pasta_teste[i]) for i in range(len(pasta_teste))]
        [os.remove(walk_puros+pasta_puros[i]) for i in range(len(pasta_puros))] 

#---------------- Normalizando os dados  ----------------------#
def DEMO_joystick():
        import dados_joy_mind
        
        #Chamando o código para normalizar os dados 
        from tratamento_dados import iniciar_normalizacao
        resultado = iniciar_normalizacao("17")

        #Iniciar o treinamento
        from treinamento_RNA_analise import treinar_rede_dataseet
        re = treinar_rede_dataseet("17")
        print(re[1])
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")

        for i in range(len(re[0])):
                coluna[i+1] = re[0][i]

                #Gravando a numeração dos arquivos 
        for i in range(len(resultado[2])):
                coluna[6+i]  = resultado[2][i]
                        
        #Gravando a quantidade de dados brutos
        for i in range(len(resultado[1])):
                coluna[13+i]  = resultado[1][i]

                #Gravando a quantidade de dados usados pela rede e desempenho
        for p in range(len(re[1])):
                coluna[21+p]  = re[1][p]
                                
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()
        janela_coletas.destroy()

        
                        
        #Abre os resultados da RNA independete do desempenho
        os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_resultados.py')
        sys.exit()

def normaliza():
        #Chamando o código para normalizar os dados 
        from tratamento_dados import iniciar_normalizacao
        
        resultado = iniciar_normalizacao(coluna[0]) #Diretório dos dados
        # Resultado [0] - Confirmação, [1] - lista com a quantidade de dados brutos
        print("Terminei de normalizar os dados!")

        #Se não foi possivel obter a quantidade necessaria de dados tratados 
        if resultado[0] != True:                
                if 'frente' in resultado[0]:
                        label2 = tk.Label(text="Colete mais dados", fg='red', bg=cinza, font=("Helvetica",8) )
                        label2.place(x=33, y=130)
                else:
                        label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8))
                        label2.place(x=53, y=130)
                if 'tras' in resultado[0]:
                        label2 = tk.Label(text="Colete mais dados", fg='red', bg=cinza, font=("Helvetica",8) )
                        label2.place(x=143, y=130)
                else:
                        label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8))
                        label2.place(x=163, y=130)
                if 'esquerda' in resultado[0]:
                        label2 = tk.Label(text="Colete mais dados", fg='red', bg=cinza, font=("Helvetica",8) )
                        label2.place(x=253, y=130)
                else:
                        label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8))
                        label2.place(x=273, y=130)
                if 'direita' in resultado[0]:
                        label2 = tk.Label(text="Colete mais dados", fg='red', bg=cinza, font=("Helvetica",8) )
                        label2.place(x=363, y=130)
                else:
                        label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8))
                        label2.place(x=383, y=130)
                if 'parar' in resultado[0]:
                        label2 = tk.Label(text="Colete mais dados", fg='red', bg=cinza, font=("Helvetica",8) )
                        label2.place(x=83, y=210)
                else:
                        label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8))
                        label2.place(x=103, y=210)
                if 'ligar' in resultado[0]:
                        label2 = tk.Label(text="Colete mais dados", fg='red', bg=cinza, font=("Helvetica",8) )
                        label2.place(x=203, y=210)
                else:
                        label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8))
                        label2.place(x=223, y=210)
                if 'neutro' in resultado[0]:
                        label2 = tk.Label(text="Colete mais dados", fg='red', bg=cinza, font=("Helvetica",8) )
                        label2.place(x=323, y=210)
                else:
                        label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8))
                        label2.place(x=343, y=210)

        else: #Se todos os dados foram normalizados para fazer todos os testes 
                label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8)) #Frente
                label2.place(x=53, y=130)
                label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8)) #Tras
                label2.place(x=163, y=130)
                label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8)) #Esquerda
                label2.place(x=273, y=130)
                label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8)) #Direita
                label2.place(x=383, y=130)
                label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8)) #Parar
                label2.place(x=93, y=210)
                label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8)) #Ligar
                label2.place(x=213, y=210)
                label2 = tk.Label(text="Concluido", fg='green', bg=cinza, font=("Helvetica",8)) #Neutro
                label2.place(x=343, y=210)

                #Iniciar o treinamento
                from treinamento_RNA_analise import treinar_rede_dataseet
                re = treinar_rede_dataseet(coluna[0]) #Retorna os dados do melhor treinamento da RNA e a quantidade de dados filtrados
                
                dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
                print(re[1])
                for i in range(len(re[0])):
                        coluna[i+1] = re[0][i]

                #Gravando a numeração dos arquivos 
                for i in range(len(resultado[2])):
                        coluna[6+i]  = resultado[2][i]
                        
                #Gravando a quantidade de dados brutos
                for i in range(len(resultado[1])):
                        coluna[13+i]  = resultado[1][i]

                #Gravando a quantidade de dados usados pela rede e desempenho
                for p in range(len(re[1])):
                         coluna[21+p]  = re[1][p]
                                
                [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
                dados_melhor_treinamento.write(str(coluna[quant_elementos]))
                dados_melhor_treinamento.close()
                janela_coletas.destroy()
                        
                #Abre os resultados da RNA independete do desempenho
                os.system('sudo python3 /home/diana/diana_testes/config_tela/janela_resultados.py')
                sys.exit()
                        

                    
#---------------- Abre o arquivo com os dados do melhor treinamento  ----------------------#
quant_elementos = 33
dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv").readlines()
for i in range(len(dados_melhor_treinamento)):
        coluna = dados_melhor_treinamento[i].split(";")
                
#---------------- Funções que chamam a coleta dos dados  ----------------------# 
def coleta_dados_frente():
        label3.place(x=63, y=120)

        #Chamando a leitura
        from leitura import iniciar_leitura

        """
        Leva como parametro:
        1. Nome do movimento
        2. O numero atual da coleta
        3. Diretório
        """
        
        iniciar_leitura("frente", str(coluna[6]), int(coluna[0])) 

        #Conta mais um no numero do arquivo e re-armazena no arquivo
        coluna[6] = int(coluna[6]) + 1
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()
       

def coleta_dados_tras():
        label3.place(x=173, y=120)
        from leitura import iniciar_leitura
        iniciar_leitura("tras", str(coluna[7]), int(coluna[0]))
        coluna[7] = int(coluna[7]) + 1
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()
        

def coleta_dados_esquerda():
        label3.place(x=283, y=120)
        from leitura import iniciar_leitura
        iniciar_leitura("esquerda", str(coluna[8]), int(coluna[0]))
        coluna[8] = int(coluna[8]) + 1
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()


def coleta_dados_direita():
        label3.place(x=393, y=120)
        from leitura import iniciar_leitura
        iniciar_leitura("direita", str(coluna[9]), int(coluna[0]))
        coluna[9] = int(coluna[9]) + 1
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()

def coleta_dados_parar():
        label3.place(x=113, y=200)
        from leitura import iniciar_leitura
        iniciar_leitura("parar", str(coluna[10]), int(coluna[0]))
        coluna[10] = int(coluna[10]) + 1
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()

def coleta_dados_ligar():
        label3.place(x=233, y=200)
        from leitura import iniciar_leitura
        iniciar_leitura("ligar", str(coluna[11]), int(coluna[0]))
        coluna[11] = int(coluna[11]) + 1
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()

def coleta_dados_neutro():
        label3.place(x=360, y=200)
        from leitura import iniciar_leitura
        iniciar_leitura("neutro", str(coluna[12]), int(coluna[0]))
        coluna[12] = int(coluna[12]) + 1
        dados_melhor_treinamento = open("/home/diana/diana_testes/rede_coletas/dados_melhor_treinamento.csv", "w")
        [dados_melhor_treinamento.write(str(coluna[i])+";") for i in range(0,quant_elementos)]
        dados_melhor_treinamento.write(str(coluna[quant_elementos]))
        dados_melhor_treinamento.close()

trilha = "/home/diana/diana_testes/config_tela/"

#---------------- Construção da Interface  ----------------------# 
#Botao para leitura frente
pil_image0 = Image.open(trilha+'coletas/frente.png')
image_0 = pil_image0.resize((95, 46), Image.ANTIALIAS) #Tamanho da imagem
image_0.save(trilha+'coletas/frente.png')
tk_image0 = ImageTk.PhotoImage(image_0)
botao0 = tk.Button(janela_coletas)
botao0.config(image=tk_image0,command=coleta_dados_frente, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao0.place(x=30, y=80)

#Botao para leitura tras
pil_image1 = Image.open(trilha+'coletas/tras.png')
image_1 = pil_image1.resize((95, 46), Image.ANTIALIAS) #Tamanho da imagem
image_1.save(trilha+'coletas/tras.png')
tk_image1 = ImageTk.PhotoImage(image_1)
botao1 = tk.Button(janela_coletas)
botao1.config(image=tk_image1,activebackground=cinza, command=coleta_dados_tras, borderwidth=0,highlightbackground=cinza,background=cinza)
botao1.place(x=140, y=80)

#Botao para leitura esquerda
pil_image2 = Image.open(trilha+'coletas/esquerda.png')
image_2 = pil_image2.resize((95, 46), Image.ANTIALIAS) #Tamanho da imagem
image_2.save(trilha+'coletas/esquerda.png')
tk_image2 = ImageTk.PhotoImage(image_2)
botao2 = tk.Button(janela_coletas)
botao2.config(image=tk_image2, compound="right", command=coleta_dados_esquerda, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao2.place(x=250, y=79)

#Botao para leitura direita
pil_image3 = Image.open(trilha+'coletas/direita.png')
image_3 = pil_image3.resize((95, 46), Image.ANTIALIAS) #Tamanho da imagem
image_3.save(trilha+'coletas/direita.png')
tk_image3 = ImageTk.PhotoImage(image_3)
botao3 = tk.Button(janela_coletas)
botao3.config(image=tk_image3, compound="right", command=coleta_dados_direita, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao3.place(x=360, y=79)

#Botao para leitura parar
pil_image4 = Image.open(trilha+'coletas/parar.png')
image_4 = pil_image4.resize((95, 46), Image.ANTIALIAS) #Tamanho da imagem
image_4.save(trilha+'coletas/parar.png')
tk_image4 = ImageTk.PhotoImage(image_4)
botao4 = tk.Button(janela_coletas)
botao4.config(image=tk_image4, compound="right", command=coleta_dados_parar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao4.place(x=80, y=159)

#Botao para leitura ligar
pil_image5 = Image.open(trilha+'coletas/ligar.png')
image_5 = pil_image5.resize((95, 46), Image.ANTIALIAS) #Tamanho da imagem
image_5.save(trilha+'coletas/ligar.png')
tk_image5 = ImageTk.PhotoImage(image_5)
botao5 = tk.Button(janela_coletas)
botao5.config(image=tk_image5, compound="right", command=coleta_dados_ligar, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao5.place(x=200, y=159)

#Botao para leitura neutro
pil_image6 = Image.open(trilha+'coletas/neutro.png')
image_6 = pil_image6.resize((95, 46), Image.ANTIALIAS) #Tamanho da imagem
image_6.save(trilha+'coletas/neutro.png')
tk_image6 = ImageTk.PhotoImage(image_6)
botao6 = tk.Button(janela_coletas)
botao6.config(image=tk_image6, compound="right", command=coleta_dados_neutro, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao6.place(x=320, y=159)

#Botao para ir para a janela de testes
pil_image7 = Image.open(trilha+'coletas/ir.png')
image_7 = pil_image7.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_7.save(trilha+'coletas/ir.png')
tk_image7 = ImageTk.PhotoImage(image_7)
botao7 = tk.Button(janela_coletas)
botao7.config(image=tk_image7, compound="right", command=janela_testes, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao7.place(x=400, y=240)

#Botao para ir para a janela de instrucoes
pil_image8 = Image.open(trilha+'coletas/voltar.png')
image_8 = pil_image8.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_8.save(trilha+'coletas/voltar.png')
tk_image8 = ImageTk.PhotoImage(image_8)
botao8 = tk.Button(janela_coletas)
botao8.config(image=tk_image8, compound="right", command=janela_instrucoes2, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao8.place(x=20, y=240)

#Botao para ir para o menu
pil_image9 = Image.open(trilha+'coletas/menu.png')
image_9 = pil_image9.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_9.save(trilha+'coletas/menu.png')
tk_image9 = ImageTk.PhotoImage(image_9)
botao9 = tk.Button(janela_coletas)
botao9.config(image=tk_image9, compound="right", command=janela_menu, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao9.place(x=10, y=10)

#Botao para ir para o menu
pil_image15 = Image.open(trilha+'testes/demo.png')
image_15 = pil_image15.resize((100, 60), Image.ANTIALIAS) #Tamanho da imagem
image_15.save(trilha+'testes/demo.png')
tk_image15 = ImageTk.PhotoImage(image_15)
botao15 = tk.Button(janela_coletas)
botao15.config(image=tk_image15, compound="right", command=DEMO_joystick, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao15.place(x=270, y=245)

#Botao para ir para o menu
pil_image16 = Image.open(trilha+'coletas/relatorio.png')
image_16 = pil_image16.resize((40, 40), Image.ANTIALIAS) #Tamanho da imagem
image_16.save(trilha+'coletas/relatorio.png')
tk_image16 = ImageTk.PhotoImage(image_16)
botao16 = tk.Button(janela_coletas)
botao16.config(image=tk_image16, compound="right", command=janela_resultados, borderwidth=0,highlightbackground=cinza,activebackground=cinza,background=cinza)
botao16.place(x=420, y=10)


#Titulos
botao11 = tk.Button(janela_coletas, text='Treinar RNA', font=("Helvetica 30 bold",10), fg = 'white', background = 'black', height=1, width=15, command = normaliza)
botao11.place(x=100, y= 265)

label4 = tk.Label(text="Coletas com o capacete", fg='black', bg=cinza, font=("Helvetica 20 bold",15) )
label4.place(x=70, y=20)

label5 = tk.Label(text="MindFlex", fg='#005580', bg=cinza, font=("Helvetica 20 bold",15) )
label5.place(x=313, y=20)

label3 = tk.Label(text=" ... ", fg='red', bg=cinza, font=("Helvetica",15)) #Indica qual foi a ultima coleta

janela_coletas.mainloop()
