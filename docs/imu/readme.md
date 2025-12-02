# **Uso de Sensor Inercial – GY80 (`sendIMUData.h`)**

Antes de iniciar a leitura deste documento, recomendo entender o conceito de **Neurodevices** neste link:
👉 [https://github.com/isd-iin-els/Neurodevices](https://github.com/isd-iin-els/Neurodevices)

Esse material explica como **tópicos e mensagens** funcionam nos serviços operados via **MQTT**, fundamental para utilizar os sensores inerciais corretamente.

---

## **Comando e Stream**

O funcionamento segue a mesma lógica de outros sensores e lembra o padrão **setup/loop do Arduino**:

* Uma função de **setup/init** é chamada via tópico `cmd/<service_id>`.
* Essa função inicializa o sensor e ativa o **loop contínuo**.
* O loop realiza a aquisição dos dados e publica no tópico:
  **`stream/<service_id>`**.

---

## **Padrão de Comando + Exemplo**

Para ativar o sensor inercial e receber os dados via MQTT, o comando deve conter os seguintes parâmetros:

* **op:** `2`
  Operação indicando que o sensor inercial será inicializado.
* **simulationTime:** *inteiro*
  Tempo (em segundos) durante o qual o streaming enviará dados.
* **frequence:** *inteiro*
  Frequência em Hz dos dados enviados (e da amostragem do sensor).

Após enviar o comando, **um programa externo deve se inscrever no tópico de streaming** para receber as mensagens.

---

### **📌 Exemplo**

**Objetivo:** sensor operando a **10 Hz** durante **300 s**.
**Comando JSON a enviar:**

```json
{
  "op": 2,
  "simulationTime": 300,
  "frequence": 10
}
```

---

### **Como receber os dados?**

1. Inscrever-se no tópico:
   **`stream/<service_id>`**
2. Aguardar as mensagens na função `onMessage` da linguagem utilizada.
