## Arquivos TCC: Sistema Automático para Coleta e Classficação de Ondas Cerebrais 
### Instituição: Fatec Santo André
### Curso: Mecatronica Industrial 
Aluno: Diana Regina da Silva

Orientador: Prof. Paulo Tetsuo Hoashi

Ano de Conclusão: 2019

----------------------------------------------------------------------------------------

Organização dos Diretórios:
Linguagem C:
- Coleta_Mindflex.ino: Coleta dos Dados do Capacete MindFlex
- JoysticTCC: Leitura e mapeamento das posições do joystick
- node-para-raspberry: Recebe as mensagens transmitidas do raspberry para o acionamento do carrinho

Linguagem Python - Raspberry:

Construção das Janelas:

- janela_menu: Contrução da janela principal
- janela_instrucoes: Contrução da janela de instruções (parte 1)
- janela_instrucoes2: Contrução da janela de instruções (parte 2)
- janela_coletas: Contrução da janela de coletas
- janela_resultados: Contrução da janela de resultados - Apresentação do melhor desempenho da RNA
- janela_testes: Contrução da janela de testes
- janela_classifica: Contrução da janela de classificações - Resultado do teste para o usuário
- janela_uso_automatico: Contrução da janela de uso automático para o joystick e capacete mindflex
- janela_uso_manual_v0: Contrução da janela de uso manual

Leitura - Tratamento - Treinamento da RNA - Aplicação
- dados_joy_mind: Tratamento dos dados para testar a capacidade de classificação da RNA
- leitura: Leitura e gravamento dos dados coletados em arquivo .csv
- tratamento_dados: Normalização e filtro dos dados para uma faixa de valores para a construção dos datasets
                    Separação dos dados de treinamento e teste
- treinamento_RNA_analise: Treinamento da RNA e calculo de desempenho
- modelo_RNA_testes_uso_joy: Recebe os dados do capacete para classificação da RNA e acionamento do carrinho
- teste_automa: Executa o script "modelo_RNA_testes_uso_joy" enquanto não for selecionado
                a opção de parar a simulação na janela de uso automático
