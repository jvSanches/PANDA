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

O download do executável encontra-se aqui: [PANDA Software](https://mega.nz/file/axgA1SaY#NMB4sDLCN5FtJLe6xaybOM77CXp7pwxL-bIBF7l-11k).



Como Usar
=================

### Pré-Requisitos

O único pré-requisito necessário para usar o software da PANDA é ter o sistema operacional Windows. Se esse não for o seu caso, será necessário que você tenha no seu sistema operacional algum ambiente que rode Python, de preferência usando Anaconda. Em seguida, baixe para seu computador os arquivos em Python da pasta 'Software'. Instale as bibliotecas wx, matplotlib, time, os, numpy e pyinstaller. Na linha de comando, no diretório dos arquivos que você baixou, digite a seguinte linha:
```bash
pyinstaller --onefile MainFrame.py --noconsole
```
Pronto! O executável gerado estará na pasta dist, ainda no diretório onde estão os arquivos que você baixou.

### Configurações

* Na janela de Configurações, você possui algumas opções. O primeiro botão de cima para baixo ativa/desativa o modo de Controle. Uma vez ativado, é possível escolher entre controle P, PD, PI ou PID;

* O segundo bloco é onde você pode selecionar os gráficos que quer gerar. Atenção: só é possível selecionar gráficos de Controle se ele estiver ativo. 'Gráficos dos Valores' refere-se aos valores selecionados mais para baixo;

* Em seguida, preencha a lacuna com o valor do ganho desejado para o amplificador. Pode ser inserido um valor de 1 a 1000; 

* No bloco 'Mostrar Valores', selecione de quais valores você quer que sejam gerados os dados e gráficos;

* Essa é a parte mais complicada. É necessário que você calcule a constante multiplicadora para cada valor desejado. O valor fornecido pela placa é o da tensão de saída da Ponte de Wheatstone, e para convertê-lo é necessário realizar algumas contas, que dependem de propriedades da sua aplicação.

Para o cálculo de Ks (constante de deformação): <img src="http://www.sciweavers.org/upload/Tex2Img_1605911981/render.png" width="100">, onde GF é o Gage Factor dos extensômetros, Vi é a tensão de entrada da ponte (o _default_ é 3.3V), Vo é a tensão de saída e ε é a deformação. As outras constantes vêm de fórmulas de Resistência dos Materiais. Dica: comece encontrando a tensão exercida na célula de carga (a tensão que gera a deformação). A partir daí, é possível encontrar o momento sendo exercido (torque) e a força. Tudo pode ser escrito em função da tensão de saída.

### Calibração

Uma vez que você tenha terminado as configurações, aqui basta informar qual o valor de deformação, força ou torque sendo exercido no momento da calibração. A placa tratará de realizar sua rotina de auto-calibração.

### Modo Controle

Ainda não está completamente implementado. Uma vez que você tenha selecionado sua opção de Controle nas configurações, ao apertar o botão na janela principal você poderá digitar o _setpoint_ que deseja para a sua aplicação. **Cuidado:** a responsabilidade é sua de informar um valor que sua aplicação seja capaz de realizar. Na janela do _setpoint_ aparecerão as constantes que serão enviadas. Ao clicar em 'Confirmar', observe o que acontece na sua aplicação.

### Gráficos e Dados

Uma vez que tenha selecionado quais gráficos deseja gerar, ao clicar no botão 'Mostrar Gráficos' na janela principal, eles serão abertos. Os _plots_ serão atualizados em tempo real. No menu da janela, você pode escolher salvar o gráfico como uma imagem (grava o gráfico no instante em que é clicada essa opção), salvar os dados adquiridos em um arquivo _.csv_, ou parar o gráfico (Ctrl-X), situação em que o programa para de gerar novos pontos. No caso da opção de parar, para voltar a ver novos _plots_ é necessário apertar novamente o botão dos gráficos. 

Aplicações Atuais
=================

### Deformação de Barras

Essa aplicação tem como foco auxiliar em aulas de Instrumentação. Como a PANDA capta dados vindos de extensômetros, ela pode medir a deformação ocorrida em uma barra e mostrar esse valor em tempo real em um gráfico. Se essa deformação ocorre devido a um peso, este pode ser calculado também. Dessa forma, é possível construir uma balança simples e os alunos podem consolidar diversos conceitos ligados a Instrumentação.

### Comunicação com Protocolos

Como já dito anteriormente, a PANDA serve como plataforma para comunicação entre diversos protocolos. Imagine que em um laboratório de pesquisa alguns equipamentos funcionem com protocolo CAN, enquanto outros funcionam com I2C. O funcionamento conjunto desses aparelhos pode ser facilitado através de nossa placa, já que ela consegue entender e enviar informações para ambos os protocolos, além de RS485 e USB.

Aplicações Futuras
=================

### Torque em Exoesqueletos

Talvez seja uma constatação óbvia, mas exoesqueletos devem ser precisos. Se você aplica um torque específico em um local equivalente ao joelho de um exoesqueleto, é necessário analisar se este torque exercido realmente é o desejado. Além disso, o monitoramento também é essencial se levar em consideração o uso desse equipamento para fisioterapia e reabilitação, situações onde um torque indesejado pode significar consequências graves para o usuário. Portanto, aplicando uma célula de carga nesse exoesqueleto e conectando extensômetros a ela, pode-se não só verificar em tempo real o torque, como também controlá-lo estabelecendo rotinas de Controle.

### Curva de Torque de Motores

Em projetos de equipamentos que exigem motores trifásicos, sobretudo para ferramentas relacionadas a processos de usinagem, uma análise necessária é a da curva de torque desses motores. Com a PANDA e seu software, basta selecionar a opção desse gráfico nas configurações, e uma vez que uma célula de carga esteja acoplada ao motor, essa curva pode ser gerada para a interpretação do projetista.

### Caracterização de Motores

No âmbito da Robótica, o estudo de motores adequados para as aplicações é de grande relevância. Aproveitamos para dar um alô para a [Equipe ThundeRatz de Robótica](https://thunderatz.org/)! Em grupos de extensão como esse, fazer a caracterização de motores é importante para verificar informações deles que podem não estar disponíveis tão facilmente. Também é interessante o seu uso para a verificação de motores que foram revitalizados. 

### Leitura de Termistores

Para a área de Térmicas a PANDA também possui função! Em aplicações utilizando motores a vapor, além de checar informações sobre o motor em si, também é preciso manter controle da temperatura do sistema. Assim, nossa placa também consegue realizar a leitura de termistores.

### Controle de Módulo Motorizado

Nas matérias relacionadas com Controle, muitas vezes pode ser difícil enxergar como um sistema de equações pode fazer um sistema motorizado funcionar da forma que queremos. Assim, a PANDA também pode auxiliar nesses Laboratórios, controlando alguns módulos. É possível escolher dentre 4 tipos de controle, além de poder gerar gráficos de pólos e zeros e respostas a degraus e rampas.

### Interface com Arduino

Por fim <s>por enquanto</s>, a última aplicação é mais geral, mas que também abre portas para muitas oportunidades. A PANDA pode se comunicar com Arduinos! Dessa forma, essa placa que é tanto utilizada mundo afora pode construir projetos que incluam também a nossa placa. Pense nas possibilidades de modularização e escalabilidade!


      
      
