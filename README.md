### Arquivos TCC: Sistema Automático para Coleta e Classficação de Ondas Cerebrais 
Instituição: Fatec Santo André

Curso: Mecatronica Industrial 

Aluno: Diana Regina da Silva

Orientador: Prof. Paulo Tetsuo Hoashi

Ano de Conclusão: 2019

### Resumo do Projeto 
 >O projeto “Sistema Automático de Coleta e Classificação de Ondas Cerebrais” tem como objetivo desenvolver uma interface gráfica automatizada que permita a coleta de sinais cerebrais através do capacete MindFlex (da empresa Neurosky), para acionamento dos movimentos de um carrinho a partir da diferença de comportamento desses sinais, que serão utilizados como entrada para uma Rede Neural Artificial (RNA), destinada a aprender a classificá-las em uma saída. O aprendizado é feito em um algoritmo de treinamento no Raspberry Pi3, um microprocessador com boa velocidade de processamento para fazer a RNA receber a leitura do capacete, interpretar e emitir uma saída que acionará um carrinho para a direção escolhida. 

----------------------------------------------------------------------------------------

### Organização dos Diretórios de Scripts: 
__Linguagem C:__
- Coleta_Mindflex.ino: Coleta dos Dados do Capacete MindFlex
- JoysticTCC: Leitura e mapeamento das posições do joystick
- node-para-raspberry: Recebe as mensagens transmitidas do raspberry para o acionamento do carrinho

__Linguagem Python - Raspberry:__

_Construção das Janelas:_

- janela_menu: Contrução da janela principal
- janela_instrucoes: Contrução da janela de instruções (parte 1)
- janela_instrucoes2: Contrução da janela de instruções (parte 2)
- janela_coletas: Contrução da janela de coletas
- janela_resultados: Contrução da janela de resultados - Apresentação do melhor desempenho da RNA
- janela_testes: Contrução da janela de testes
- janela_classifica: Contrução da janela de classificações - Resultado do teste para o usuário
- janela_uso_automatico: Contrução da janela de uso automático para o joystick e capacete mindflex
- janela_uso_manual_v0: Contrução da janela de uso manual

_Leitura - Tratamento - Treinamento da RNA - Aplicação_
- dados_joy_mind: Tratamento dos dados para testar a capacidade de classificação da RNA
- leitura: Leitura e gravamento dos dados coletados em arquivo .csv
- tratamento_dados: Normalização e filtro dos dados para uma faixa de valores para a construção dos datasets
                    Separação dos dados de treinamento e teste
- treinamento_RNA_analise: Treinamento da RNA e calculo de desempenho
- modelo_RNA_testes_uso_joy: Recebe os dados do capacete para classificação da RNA e acionamento do carrinho
- teste_automa: Executa o script "modelo_RNA_testes_uso_joy" enquanto não for selecionado
                a opção de parar a simulação na janela de uso automático


### Organização dos Diretórios de Dados:
__Dados Coletados com Mindfex:__
- Movimentos: Dados coletados durante a execução de um movimento com o braço direito e com a perna direita 
- Palavras: Dados coletados pensando em palavras que remetessem cada um dos movimentos 
- Musicas: Dados coletados ao ouvir musicas com 2 estilos diferentes (Rock e Sons da Natureza)

__Testes Joystick:__
- Teste 3 - Validação com Joystick: Dados tratados de maneira que apenas uma coluna diferenciasse os movimentos pela amplitude 
- Teste 9 - Validação com Joystick: Dados tratados de maneira que cada coluna representasse o acionamento de um movimento 
