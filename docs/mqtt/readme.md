# **Comunicação entre Neurodevice e Aplicações Externas**

O objetivo deste documento é esclarecer questões respectivas à comunicação entre o neurodevice e outras aplicações externas. Além disso, também serão apresentadas arquiteturas internas de forma concisa. Informações além da arquitetura — ou seja, relativas aos módulos e serviços — podem ser encontradas nos links abaixo:

👉 **[Sensor Inercial](https://github.com/isd-iin-els/Neurodevices/blob/main/docs/imu/readme.md)**
👉 **[Estimulador Elétrico](https://github.com/isd-iin-els/Neurodevices/blob/main/docs/openloopfes/readme.md)**

---

O **Neurodevice** é uma biblioteca para microcontroladores **ESP32/ESP32-S2/ESP32-C3**, criada para facilitar operações entre esses dispositivos e aplicações externas via **MQTT**.
A biblioteca possui diversos recursos de interação com Wi-Fi; porém, neste documento, trataremos apenas do modo **STA**.

A figura a seguir exemplifica a arquitetura e o fluxo de dados:

![Conceito de Comunicação](https://github.com/isd-iin-els/Neurodevices/blob/main/docs/mqtt/conceitoComunicacao.png?raw=true)

---

## **Visão Geral da Comunicação**

Como é possível visualizar, só é possível utilizar o sistema se existir um **Broker MQTT**, e é a partir dele que começamos.

À direita, temos um bloco representando o **Neurodevice**, responsável pela comunicação com o broker. Este bloco possui **três tópicos principais**:

* **Comando** – utilizado para solicitar serviços ao dispositivo.
* **Stream** – aparece somente quando solicitado via comando ou quando alguém realiza *subscribe*.
* **Status** – tópico genérico para respostas como *"porta está com erro"* ou *"saída não pode streamar dados"*.

Além disso, vemos os **serviços disponíveis** no Neurodevice, que podem ser utilizados através dos comandos apropriados (ver links acima).
Os exemplos apresentados nos links ajudam a entender como uma interface JavaScript pode controlar os dispositivos.

À direita também aparece o **retorno**, ou seja, funções que cadastram tópicos de streaming e devolvem dados ao broker. Por fim, o tópico de **status genérico** envia mensagens como *"todos os parâmetros foram inicializados"* ou outras respostas simples.

---

## **Aplicações Externas e Sequência de Comunicação**

Acima do broker, temos as aplicações externas. Independentemente da linguagem utilizada, uma aplicação precisa realizar um conjunto de ações sobre o MQTT para se comunicar com o Neurodevice (enviar comandos e receber *stream/status*).
A sequência é:

1. **Ter o dispositivo ligado**
   Só é possível identificar dispositivos que já estejam ativos.

2. **Subscribe no tópico `newService`**
   Este tópico recebe informações enviadas em *broadcast* pelos dispositivos.

3. **Publish em `broadcast/get_active_service`**
   Usado quando a aplicação não conhece os dispositivos existentes.
   A solicitação faz com que o dispositivo responda via `newService`, permitindo seu reconhecimento.

4. **Aguardar o `whoAmI` do dispositivo**
   O retorno costuma ser imediato e tratado via *callback*.

5. **Identificar e armazenar o `service_id`**
   O ID deve ser guardado (variável local ou EEPROM), pois é ele que permite controlar o dispositivo via MQTT.

6. **Operar o dispositivo enviando e recebendo dados**
   Uma vez em posse do ID e das funções (informadas no `whoAmI`), a aplicação pode executar os *publish* e *subscribe* necessários para acessar qualquer serviço.

---

## **Conclusão**

A arquitetura baseada em MQTT permite uma comunicação clara, modular e escalável entre aplicações externas e o Neurodevice.


