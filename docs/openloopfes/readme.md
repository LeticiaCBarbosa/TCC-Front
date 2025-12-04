# **Uso de Eletroestimulador – (`openLoopFes.h`)**

Antes de iniciar a leitura deste documento, recomendo entender o conceito de **Neurodevices** neste link:
👉 [https://github.com/isd-iin-els/Neurodevices](https://github.com/isd-iin-els/Neurodevices) .

Esse material explica como **tópicos e mensagens** funcionam nos serviços operados via **MQTT**, fundamental para utilizar os comandos de eletroestimulação corretamente.

Também, é importante notar que no arquivo src/main.cpp, o addfunction correlato a openloopfes deve estar descomentado, tendo comentado com o de IMU (que conflita com ele).


## 2. Update Loop

De forma objetiva a principal função necessária aqui é a openLoopFesUpdate. Isso acontece porque no modo de estimulação elétrica, o estimulador está sempre ligado variando de 0 a 100% de PWM. Por isso, quando a função de update é chamada, ela também inicializa, caso não tenha sido inicializada. É importante notar que neste projeto apenas ondas retangulares monofásicas e bifásicas foram consideradas.

## **Padrão de Comando + Exemplo**

Para ativar a estimulação elétrica e atualizar os valores de amplitude, o comando deve conter os seguintes parâmetros:

* **op:** `2`. Operação indicando que o estimulador elétrico será inicializado e/ou terá seu valor atualizado (ver no arquivo ./src/main.cpp).
* **m:** *string com números (floats) separados por vírgula*. No máximo terão 4 números. Isso acontece porque a função foi feita para um estimulador de até 8 canais.
* **t:** *inteiro*.  Largura do pulso de eletroestimulação.
* **p:** *inteiro*.  Período do pulso elétrico.

### Exemplo

Vamos supor que o objetivo seja criar uma aplicação que seja capaz de interagir com o eletroestimulador. Para isso, utilizando os padrões apresentados acima o seguinte json foi enviado para o tópico de comando (`cmd/<service_id>`) do estimulador elétrico:

{"op":2,parameters:{"m":"4,0,0,0","t":"200","p":"20000"}}

Isso significa que o eletroestimulador reeceberá um json indicando que uma onda de 200s de largura de pulso e 50Hz (10⁶/20000) será formada a partir daquele momento. Além disso, os valores de m indicam que o canal 1 será estimulado em 4% do seu PWM, isto é em 4% da aplitude de tensão.

OBS.:
    1 - Não é possível, depois de iniciar a eletroestimulação, realizar uma atualização de largura de pulso e frequencia. Para tornar issoo possíve, o usuário deve reiniciar o microcontrolador.
    2 - A operação 2 só é válida se no arquivo ./src/main.cpp essa operação estiver na seguinte forma: addFunctions("openLoopFesUpdate",OPENLOOPFESUPDATE_PARAMETERS,openLoopFesUpdate,2);
    3 - Para testes rápidos, é possível utilizar a página [web](https://github.com/isd-iin-els/Neurodevices/blob/main/include/directStimulation_new.html)  