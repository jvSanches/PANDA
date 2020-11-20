<img src="https://img.shields.io/static/v1?label=PANDA&message=v1.0&color=ceccd6&style=for-the-badge&logo=python"/> 

<h1 align="center">PANDA :panda_face: </h1>
<p align="center">Placa de Aquisição e coNdicionamento de DAdos</p>
<p align="center">Escola Politécnica da USP - Engenharia Mecatrônica</p>
<img src="https://www.amigosdapoli.com.br/static/logo-de0ca5685bde306c6345b2805c4685c5.png" width="300" align="right">


Sobre
=================
Trabalho de Conclusão de Curso dos alunos Guilherme de Agrela Lopes e João Vitor Sanches, orientados pelo Prof. Dr. Rafael Traldi Moura, para a obtenção do diploma de Engenheiros Mecatrônicos da Escola Politécnica da USP.

O foco do projeto é a PANDA (Placa de Aquisição e Condicionamento de Dados), uma placa construída primeiramente com o objetivo de realizar a aquisição de sinais provenientes de extensômetros, para a medição de deformações, forças e torques em aplicações de robótica. Contudo, ela evoluiu para mais do que isso. Ela também é uma plataforma de comunicação para diversos protocolos: I2C, CAN, USB e RS-485, além de possuir entradas analógicas e portas digitais.

Seu propósito é auxiliar em aulas e laboratórios da Escola Politécnica, sobretudo nas áreas de Engenharia Mecatrônica e Mecânica, nas mais diversas aplicações aqui citadas, pretendendo-se no futuro expandir para outras aplicações em conjunto com outras Engenharias.

O projeto é apoiado e financiado pelo Fundo Patrimonial Amigos da Poli, fundo este criado com o propósito de desenvolver o potencial dos alunos da Poli, financiando projetos de politécnicos para politécnicos, auxiliando a Escola a crescer e se desenvolver cada vez mais. Este projeto não seria possível sem o seu apoio, e por isso somos muito gratos.




Tabela de conteúdos
=================
<!--ts-->
   * [Sobre](#sobre)
   * [Tabela de Conteúdos](#tabela-de-conteúdos)
   * [Download](#download)
   * [Como Usar](#como-usar)
      * [Pré-Requisitos](#pré-requisitos)
      * [Configurações](#configurações)
      * [Calibração](#calibração)
      * [Modo Controle](#modo-controle)
      * [Gráficos e Dados](#gráficos-e-dados)
   * [Aplicações Atuais](#aplicações-atuais)
      * [Deformação de Barras](#deformação-de-barras)
      * [Comunicação com Protocolos](#comunicação-com-protocolos)
   * [Aplicações Futuras](#aplicações-futuras)
      * [Torque em Exoesqueletos](#torque-em-exoesqueletos)
      * [Curva de Torque de Motores](#curva-de-torque-de-motores)
      * [Caracterização de Motores](#caracterização-de-motores)
      * [Leitura de Termistores](#leitura-de-termistores)
      * [Controle de Módulo Motorizado](#controle-de-módulo-motorizado)
      * [Interface com Arduino](#interface-com-arduino)
<!--te-->



<h4 align="center"> 
	🚧  Projeto em desenvolvimento para atender todas as aplicações! 🚧
</h4>



Download
=================

O download do executável encontra-se aqui: [PANDA Software](https://mega.nz/file/uoYHTCrZ#ABBqe71Tc6OB-UX57K_Z6Jc-_zFcgVjPxbuWSQznxSI).



Como Usar
=================

### Pré-Requisitos

O único pré-requisito necessário para usar o software da PANDA é ter o sistema operacional Windows. Se esse não for o seu caso, será necessário que você tenha no seu sistema operacional algum ambiente que rode Python, de preferência usando Anaconda. Em seguida, baixe para seu computador os arquivos em Python da pasta 'Software'. Instale as bibliotecas wx, matplotlib, time, os, numpy e pyinstaller. Na linha de comando, no diretório dos arquivos que você baixou, digite a seguinte linha:
```bash
pyinstaller --onefile MainFrame.py --noconsole
```
Pronto! O executável gerado estará na pasta dist, ainda no diretório onde estão os arquivos que você baixou.

### Configurações

Na janela de Configurações, o usuário possui algumas opções. O primeiro botão de cima para baixo ativa e desativa o modo de Controle. Uma vez ativado, é possível escolher entre controle P, PD, PI ou PID.
