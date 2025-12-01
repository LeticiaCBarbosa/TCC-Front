
Neurodevice foi criado com o objetivo de dar suporte a comunicação entre microcontroladores ESP e outras aplicações em geral (atualmente representado por [SynapSys](https://github.com/isd-iin-els/SynapSys) ). A estrutura de comunicação segue os princípios de SynapSys em que todo dispositivo gravado com neurodevices se torna um bloco:

  - **Blocos físicos**: compreendem sensores e atuadores conectados ao sistema, com capacidade limitada de processamento, mas essenciais para a aquisição de dados e interação com o ambiente experimental.

Assim como todos os blocos assumem uma estrutura de mensagens baseadas no MQTT. Essa estrutura força que para se comunicar com os ESPs gravados os tópicos MQTT devem ser como os definidos a seguir: os atributos de blocos que são

  - **Tópicos MQTT**: No modelo *publish/subscribe*, os tópicos são os canais responsáveis pela organização e roteamento das mensagens. Cada bloco atua como *subscriber* em determinados tópicos e como *publisher* em outros. As principais convenções são:
  - `cmd/<service_id>`: tópico destinado ao recebimento de operações de comando que controlam o comportamento do bloco.
  - `status/<service_id>`: utilizado para publicação de mensagens com saída estruturada, geralmente em formato JSON, contendo informações detalhadas do processamento.
  - `stream/<service_id>`: destinado à publicação de dados literais ou contínuos, como inteiros, flutuantes ou strings, oriundos da função de aplicação.
  - `broadcast/get_active_services`: ao receber uma mensagem nesse tópico, todos os blocos conectados ao *broker* MQTT devem responder com suas identificações por meio do comando `who_am_i`, enviando uma mensagem para o tópico `newservice`.
  - `newservice`: tópico utilizado para receber as identificações dos blocos ativos no sistema.

Além da estrutura que obriga as mensagens e comunicação entre blocos o Neurodevice também determina um padrão de mensagens para comunicação como um microssersserviço sobre o MQTT. Esse padrão começa definindo funções básicas que podem ser acessadas via MQTT, Ex.:{"op":0}, json para chamar a função de who_am_i, no tópico `cmd/<service_id>`. É importante destacar que neste caso o fluxo da mensagem é de uma aplicação externa para o microcontrolador que processará como uma função e devolverá em status caso haja retorno. As operações já existentes como microsserviço são:

- **Operações de Comando**: Correspondem a instruções diretas enviadas a um bloco via o tópico `cmd/<service_id>`. Por padrão, cada bloco já é configurado com duas operações fundamentais:
  - `op 0 - who_am_i`: solicita que o bloco envie sua identificação detalhada para o tópico `newservice`.
  - `op 1 - subscribe`: instrui o bloco a se inscrever em um tópico MQTT específico.

  Além dessas, é possível estender o conjunto de operações de comando, permitindo que o desenvolvedor acrescente instruções adicionais conforme as necessidades do experimento. Isso deve acontecer sem sobrepor as operações que já existem. Além disso, é sugerido criar um arquivo com base no arquivo de [template](https://github.com/isd-iin-els/Neurodevices/blob/main/src/templateServico.h). Este arquivo tem a estrutura geral de como implementar um microsserviço sendo que ele guia os nomes que devem ser removidos, alterados e sobrescritos. Uma vez finalizado o microsserviço o arquivo deve ser inserido no arquivo de mais e adicionada a linha de código que terá a função a ser chamada.


Agora que o conteúdo sobre o funcionamento do sistema base (para permitir a programação), foi detalhado, ainda há um conjunto de recursos que são disponibilizados para além dos microsserviços. Uma vez construído o microserviço e gravado o microcontrolador, segue-se a partir do ítem 4.

## Procedimentos para conexão Neurodevices MQTT com ESP e aquisição de dados via _websocket_

1. Clonar repositório [Neurodevices](https://github.com/isd-iin-els/Neurodevices/tree/main)
2. Abrir projeto no VSCode
3. Conectar ESP à porta USB
4. Caso o projeto ainda não esteja gravado na memória _flash_ do ESP
   - Fazer upload do projeto Neurodevices para o ESP a partir do VSCode
   - Conectar (preferivelmente celular) à rede Wi-Fi devXXXX (XXXX é o número do dispositivo ESP. Ex.: dev3952)
   - Acessar o endereço 8.8.8.8 no _browser_ (chrome, firefox, etc...)
   - Preencher seguintes campos do formulário para configuração do ESP
     - WiFi SSID: CAMPUS
     - WiFi _Password_: IINELS_educacional
     - MQTT _Server Host Name_: endereço IP da máquina onde está instalado o servidor _broker_ MQTT (verificar IP conectado à rede Wi-Fi CAMPUS)
     - MQTT _Server port_: número da porta configurada para o _broker_ MQTT
       - Nesse caso, deve-se configurar a porta 1883, padrão do MQTT
     - _Submit_
   - Estando a máquina do _broker_ conectada à rede CAMPUS, abrir interface `directStimulation.html` no _browser_ e preencher as seguintes informações para coleta de dados com a palmilha:
     - _Server address_: endereço IP da máquina onde está instalado o servidor _broker_ MQTT (verificar IP conectado à rede Wi-Fi CAMPUS)
     - _Port_: número da porta configurada para o _broker_ MQTT
       - Caso o arquivo de configuração do _broker_ MQTT esteja configurado para conexão _websocket_ na porta 1887, configurar essa porta.
     - Tópico da palmilha: número do dispositivo ESP (Ex.: 3952)
     - Tempo de experimento: em segundos
   - Connect to MQTT
   - Começar experimento

Ou seja, além da arquitetura de microsserviços, o Neurodevices oferece um portal de configuração e uma função de teste na forma de uma pequena página web. Note que o broker MQTT deve ser instalado e as portas 1883 e ws 1887 habilitadas. Obs: É necessário desabilitar o firewall em aplicações windows.