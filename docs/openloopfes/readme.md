
# **Uso de Eletroestimulador – (`openLoopFes.h`)**

Antes de iniciar a leitura deste documento, recomenda-se revisar a definição dos **comandos para o eletroestimulador**, utilizando o conceito de **Neurodevice** no link abaixo:

👉 **[https://github.com/isd-iin-els/Neurodevices/tree/main/docs/openloopfes](https://github.com/isd-iin-els/Neurodevices/tree/main/docs/openloopfes)**

Esse material explica como o **hardware** funciona e como enviar comandos corretamente para o eletroestimulador — conhecimento essencial antes de usar esta interface.

---

## **2. Interface**

A interface apresentada na página web
👉 [https://github.com/isd-iin-els/Neurodevices/blob/main/include/directStimulation_new.html](https://github.com/isd-iin-els/Neurodevices/blob/main/include/directStimulation_new.html)
permite interagir diretamente com o eletroestimulador. Ela é composta pelos seguintes elementos:

---

### **🔌 Server Address**

Campo destinado ao endereço do **servidor MQTT** (broker).
Atenção:

* Certifique-se de que o firewall não está bloqueando conexões.
* Verifique se o arquivo de configuração do broker libera:

  * Porta **1883 (TCP)** — microcontroladores
  * Porta **9001 (WebSocket)** — interface web
* Insira aqui o **IP ou domínio** do broker.

---

### **🔢 Port**

A porta pode ser configurada no broker.
Recomendação padrão:

* **9001** → interface web (WebSocket)
* **1883** → dispositivos físicos (ESP/MCUs)

Isso permite o correto *handshake* entre microcontrolador e página web.

---

### **🆔 Device Name**

Identificação única do dispositivo.
Para obtê-la:

1. Conecte o microcontrolador via **USB**.
2. Abra um terminal serial (115200 baud).
3. Reinicie o dispositivo.
4. O identificador (baseado no MAC) será exibido no log serial.

---

### **📏 Largura do Pulso (Pulse Width)**

Define e prepara o valor da largura de pulso que será enviado ao dispositivo.

---

### **⏱️ Período (Period)**

Define e prepara o valor do período de estimulação a ser enviado.

---

### **⚡ Canais de Estimulação**

Conjunto de *slide buttons* que define quais canais serão ativados.

* Cada slide representa um canal.
* Ao soltar o slide, **todos os comandos são enviados automaticamente**.

---

### **🔗 Connect Button**

A comunicação MQTT só inicia após clicar em **Connect**.
Use este botão depois de configurar:

* servidor
* porta
* dispositivo
* parâmetros de estimulação

---

### **📜 Logs**

A interface inclui caixas de log para facilitar o monitoramento:

* **Comandos enviados**
* **Streaming recebido**
* **Status do dispositivo**

Úteis para depuração e verificação da comunicação.

