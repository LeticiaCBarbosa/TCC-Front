# Neurodevice – Estrutura, Comunicação e Procedimentos

O **Neurodevice** foi criado para dar suporte à comunicação entre microcontroladores **ESP** e aplicações externas (atualmente representadas por [SynapSys](https://github.com/isd-iin-els/SynapSys)).
Ele segue o mesmo princípio de blocos do SynapSys: **todo dispositivo gravado com Neurodevice se torna um bloco**.

---

## 1. Estrutura dos Blocos

### **Blocos físicos**

São sensores e atuadores conectados ao sistema, com processamento limitado, mas essenciais para aquisição de dados e interação com o ambiente experimental.

---

## 2. Estrutura de Mensagens (MQTT)

A comunicação no Neurodevice segue um padrão fixo de tópicos MQTT. Todo ESP gravado deve obedecer às convenções abaixo:

### **Tópicos MQTT**

* `cmd/<service_id>`
  Recebe operações de comando enviadas para o bloco.

* `status/<service_id>`
  Publica saídas estruturadas (geralmente em JSON), contendo informações de processamento.

* `stream/<service_id>`
  Publica dados contínuos (números, strings, leituras sensoriais etc.).

* `broadcast/get_active_services`
  Ao receber uma mensagem neste tópico, todos os blocos devem responder com suas identificações via comando `who_am_i`, publicando em `newservice`.

* `newservice`
  Recebe as informações de identificação dos blocos ativos.

---

## 3. Microsserviços via MQTT

Além da definição dos tópicos, o Neurodevice implementa um **padrão de microsserviço baseado em JSON**.
Exemplo de chamada:

```json
{"op": 0}
```

Enviado ao tópico `cmd/<service_id>` para executar a função `who_am_i`.

### **Operações padrão já implementadas**

* **op 0 — `who_am_i`**
  Envia a identificação completa do bloco para o tópico `newservice`.

* **op 1 — `subscribe`**
  Instrui o bloco a se inscrever em um tópico específico.

### **Expansão de operações**

O desenvolvedor pode **criar novas operações** seguindo estas regras:

* Não sobrescrever operações existentes.
* Criar um arquivo baseado no *template* oficial:
  [https://github.com/isd-iin-els/Neurodevices/blob/main/src/templateServico.h](https://github.com/isd-iin-els/Neurodevices/blob/main/src/templateServico.h)
* O template orienta:

  * o que renomear
  * o que remover
  * o que sobrescrever
* Após finalizar o microsserviço:

  * incluir o arquivo no projeto
  * adicionar a linha para registrar a nova função

---

## 4. Recursos Adicionais do Neurodevice

Além da arquitetura de microsserviços, o sistema oferece:

* Portal Web de configuração do ESP
* Página web de teste para aquisição via *websocket*
* Integração automática com broker MQTT

---

# 5. Procedimentos de Conexão e Aquisição de Dados

## **Passo a passo para usar ESP + MQTT + Websocket**

### **1. Clonar o repositório**

```
https://github.com/isd-iin-els/Neurodevices/tree/main
```

### **2. Abrir projeto no VSCode**

### **3. Conectar o ESP via USB**

---

## **4. Gravação inicial do ESP (se ainda não estiver programado)**

1. Fazer upload do projeto Neurodevices pelo VSCode.
2. Conectar um celular à rede Wi-Fi do ESP:

   * `devXXXX` (ex.: `dev3952`)
3. Abrir no navegador:

   ```
   8.8.8.8
   ```
4. Preencher o formulário:

| Campo                 | Valor                      |
| --------------------- | -------------------------- |
| Wi-Fi SSID            | CAMPUS                     |
| Wi-Fi Password        | IINELS_educacional         |
| MQTT Server Host Name | IP da máquina com o broker |
| MQTT Server Port      | 1883                       |

5. Clicar em **Submit**.

---

## **5. Coleta de dados via `directStimulation.html`**

Com a máquina do broker conectada à rede:

1. Abrir `directStimulation.html` no navegador.
2. Preencher:

| Campo                | Valor                                 |
| -------------------- | ------------------------------------- |
| Server address       | IP da máquina do broker               |
| Port                 | Porta websocket do broker (ex.: 1887) |
| Tópico da palmilha   | Número do ESP (ex.: 3952)             |
| Tempo de experimento | Em segundos                           |

3. Clicar em **Connect to MQTT**
4. Iniciar experimento

---

# 6. Observações Importantes

* O broker MQTT deve estar instalado e funcionando.
* As portas necessárias:

  * **1883** para MQTT
  * **1887** para websocket (se configurado)
* Em Windows, **desabilitar o firewall** para permitir a comunicação.

---
