
# **Uso de Eletroestimulador – (`openLoopFes.h`)**

Antes de iniciar a leitura deste documento, recomenda-se compreender o conceito de **Neurodevices** no link abaixo:

👉 **[https://github.com/isd-iin-els/Neurodevices](https://github.com/isd-iin-els/Neurodevices)**

Esse material explica como **tópicos e mensagens MQTT** funcionam nos serviços do Neurodevice, conhecimento essencial para utilizar corretamente os comandos de eletroestimulação.

⚠️ **Importante:** no arquivo `src/main.cpp`, a função relacionada a `openLoopFes` precisa estar **descomentada**, enquanto a função de IMU deve permanecer **comentada** (pois ambas entram em conflito).

---

## **2. Update Loop**

A função principal para controle do eletroestimulador é **`openLoopFesUpdate`**.

* No modo de estimulação elétrica, o dispositivo permanece **sempre ativo**, variando entre **0% e 100% de PWM**.
* Quando `openLoopFesUpdate` é chamada pela primeira vez, ela realiza a **inicialização** (caso ainda não tenha ocorrido).
* Neste projeto, foram consideradas apenas **ondas retangulares monofásicas e bifásicas**.

---

## **Padrão de Comando + Exemplo**

Para ativar a estimulação elétrica ou atualizar amplitude e parâmetros, o comando JSON deve conter:

### **Parâmetros**

* **`op: 2`**
  Indica que o eletroestimulador será inicializado e/ou atualizado
  (ver implementação em `./src/main.cpp`).

* **`m:`** *string contendo floats separados por vírgula*
  Representa as amplitudes (0–100%).
  Aceita até **4 valores** (implementação suporta até 8 canais).

* **`t:`** *inteiro*
  Largura de pulso (*pulse width*), em microssegundos.

* **`p:`** *inteiro*
  Período do pulso elétrico, em microssegundos.
  A frequência é calculada por:
  **f = 1.000.000 / p**

---

### **Exemplo de Comando**

Para enviar um comando ao tópico `cmd/<service_id>`, pode-se utilizar o seguinte JSON:

```json
{"op":2, "parameters":{"m":"4,0,0,0", "t":"200", "p":"20000"}}
```

Esse comando significa:

* **Pulse width:** 200 µs
* **Período:** 20.000 µs → **50 Hz**
* **Amplitude:** canal 1 em **4% do PWM**, demais canais desligados
* **Modo:** estimulação iniciada/atualizada

---

## **Observações Importantes**

1. **Não é possível atualizar largura de pulso ou frequência após iniciar a estimulação.**
   Para alterar esses parâmetros, o microcontrolador deve ser **reiniciado**.

2. A operação **`op = 2`** só funcionará se, em `./src/main.cpp`, estiver configurada como:

   ```cpp
   addFunctions("openLoopFesUpdate", OPENLOOPFESUPDATE_PARAMETERS, openLoopFesUpdate, 2);
   ```

3. Para testes rápidos, é possível usar a página web:
   👉 [https://github.com/isd-iin-els/Neurodevices/blob/main/include/directStimulation_new.html](https://github.com/isd-iin-els/Neurodevices/blob/main/include/directStimulation_new.html)


