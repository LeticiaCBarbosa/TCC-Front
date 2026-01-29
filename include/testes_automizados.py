"""
testes_automizados.py
Script Python que automatiza os testes usando o MESMO broker MQTT do dashboard
NÃO altera o dashboard, só se conecta ao mesmo broker
"""

import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime

# =========== CONFIGURAÇÕES IDÊNTICAS AO DASHBOARD ===========
BROKER = "192.168.137.1"          # MESMO IP que seu dashboard usa
PORT = 1883                       # MESMA porta (1883 no seu broker real)
DEVICE_ID = "237917650741564"     # MESMO ID do dispositivo
# ============================================================

class TestesAutomatizados:
    def __init__(self):
        self.client = mqtt.Client(client_id=f"python_tester_{int(time.time())}")
        self.latencies = []
        self.respostas_recebidas = []
        
    def conectar(self):
        """Conecta ao MESMO broker MQTT que o dashboard usa"""
        print("🔌 Conectando ao broker MQTT...")
        
        # Conecta (igual ao dashboard faz)
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_start()
        time.sleep(2)
        
        # Se inscreve nos MESMOS tópicos que o dashboard
        self.client.subscribe(f"status/{DEVICE_ID}")
        self.client.subscribe(f"stream/{DEVICE_ID}")
        
        print(f"✅ Conectado ao broker {BROKER}:{PORT}")
        print(f"📡 Inscrito em: status/{DEVICE_ID}")
        print(f"📡 Inscrito em: stream/{DEVICE_ID}")
        
    def on_message(self, client, userdata, msg):
        """Processa mensagens recebidas (callback)"""
        try:
            data = json.loads(msg.payload.decode())
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            print(f"[{timestamp}] 📥 {msg.topic}: {data}")
            
            if msg.topic == f"status/{DEVICE_ID}":
                self.respostas_recebidas.append({
                    "time": time.time(),
                    "data": data,
                    "topic": msg.topic
                })
                
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
    
    # ===== ENVIA COMANDO IDÊNTICO AO DO DASHBOARD =====
    def enviar_comando(self, ch1_value, ton=200, period=20000):
        """
        Envia EXATAMENTE o mesmo comando JSON que seu dashboard envia
        Formato: {"op": 2, "parameters": {"m": "X", "t": "Y", "p": "Z"}}
        """
        payload = {
            "op": 2,
            "parameters": {
                "m": str(ch1_value),  # STRING, igual no dashboard
                "t": str(ton),        # STRING
                "p": str(period)      # STRING
            }
        }
        
        topico = f"cmd/{DEVICE_ID}"
        mensagem_json = json.dumps(payload)
        
        # Marca tempo de envio
        tempo_envio = time.time()
        
        # Publica no MESMO tópico que o dashboard
        self.client.publish(topico, mensagem_json)
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 📤 {topico}: {mensagem_json}")
        
        return tempo_envio, payload
    
    # ===== TESTE 1: FREQUÊNCIA LIMITE =====
    def teste_frequencia_limite(self):
        """Testa em qual frequência o sistema para de responder bem"""
        print("\n" + "="*60)
        print("🧪 TESTE 1: FREQUÊNCIA LIMITE")
        print("="*60)
        
        # Frequências para testar (mensagens por segundo)
        frequencias = [1, 5, 10, 20, 50, 100]
        resultados = {}
        
        for freq_hz in frequencias:
            print(f"\n📊 Testando {freq_hz} Hz...")
            
            self.respostas_recebidas = []  # Limpa respostas
            tempo_inicio = time.time()
            enviadas = 0
            
            # Envia 20 mensagens na frequência especificada
            for i in range(20):
                tempo_envio, _ = self.enviar_comando(
                    ch1_value=50,  # 50% de intensidade
                    ton=200,
                    period=20000
                )
                enviadas += 1
                
                # Aguarda para manter a frequência exata
                if i < 19:  # Não espera na última
                    tempo_espera = (1.0 / freq_hz) - (time.time() - tempo_envio)
                    if tempo_espera > 0:
                        time.sleep(tempo_espera)
            
            # Aguarda respostas (2 segundos de timeout)
            time.sleep(2)
            
            recebidas = len(self.respostas_recebidas)
            taxa_sucesso = (recebidas / enviadas) * 100
            
            print(f"  Enviadas: {enviadas}, Recebidas: {recebidas}")
            print(f"  Taxa de sucesso: {taxa_sucesso:.1f}%")
            
            resultados[freq_hz] = {
                "enviadas": enviadas,
                "recebidas": recebidas,
                "taxa_sucesso": taxa_sucesso,
                "status": "OK" if taxa_sucesso >= 95 else "LIMITE"
            }
            
            if taxa_sucesso < 80:  # Limite atingido
                print(f"  ⚠️ LIMITE ATINGIDO em {freq_hz} Hz")
                break
        
        return resultados
    
    # ===== TESTE 2: LATÊNCIA =====
    def teste_latencia(self, frequencia_hz=10, num_medições=20):
        """Mede latência (tempo entre enviar e receber resposta)"""
        print(f"\n" + "="*60)
        print(f"⏱️ TESTE 2: LATÊNCIA ({frequencia_hz} Hz)")
        print("="*60)
        
        latencias_ms = []
        
        for i in range(num_medições):
            print(f"\n📈 Medição {i+1}/{num_medições}:")
            
            # Limpa respostas anteriores
            self.respostas_recebidas = []
            
            # Envia comando e marca tempo
            tempo_envio, _ = self.enviar_comando(
                ch1_value=30 + (i * 3),  # Varia intensidade
                ton=200,
                period=20000
            )
            
            # Aguarda resposta (timeout de 1 segundo)
            timeout = time.time() + 1.0
            while len(self.respostas_recebidas) == 0 and time.time() < timeout:
                time.sleep(0.01)
            
            if self.respostas_recebidas:
                tempo_resposta = self.respostas_recebidas[0]["time"]
                latencia = (tempo_resposta - tempo_envio) * 1000  # ms
                latencias_ms.append(latencia)
                print(f"  ✅ Resposta em {latencia:.1f} ms")
            else:
                print(f"  ❌ Sem resposta (timeout)")
                latencias_ms.append(999)  # Valor alto para indicar falha
            
            # Aguarda para próxima medição (mantém frequência)
            if i < num_medições - 1:
                tempo_espera = (1.0 / frequencia_hz) - (time.time() - tempo_envio)
                if tempo_espera > 0:
                    time.sleep(tempo_espera)
        
        # Calcula estatísticas
        if latencias_ms:
            latencias_validas = [l for l in latencias_ms if l < 999]
            
            if latencias_validas:
                media = sum(latencias_validas) / len(latencias_validas)
                minima = min(latencias_validas)
                maxima = max(latencias_validas)
                
                print(f"\n📊 RESULTADOS ({frequencia_hz} Hz):")
                print(f"  • Latência média: {media:.1f} ms")
                print(f"  • Mínima: {minima:.1f} ms")
                print(f"  • Máxima: {maxima:.1f} ms")
                print(f"  • Taxa de resposta: {len(latencias_validas)}/{num_medições}")
                
                return {
                    "frequencia": frequencia_hz,
                    "media_ms": media,
                    "min_ms": minima,
                    "max_ms": maxima,
                    "respostas": len(latencias_validas),
                    "total": num_medições
                }
        
        return None
    
    def executar_todos_testes(self):
        """Executa a sequência completa de testes"""
        print("🚀 INICIANDO TESTES AUTOMATIZADOS DO NEURODEVICE")
        print("="*60)
        print("ℹ️  Este script usa o MESMO broker MQTT do dashboard")
        print("ℹ️  O dashboard pode continuar funcionando normalmente")
        print("="*60)
        
        # Configura callback para mensagens
        self.client.on_message = self.on_message
        
        # 1. Conecta ao broker
        self.conectar()
        time.sleep(1)
        
        # 2. Teste de frequência limite
        print("\n1️⃣ EXECUTANDO TESTE DE FREQUÊNCIA LIMITE")
        resultado_freq = self.teste_frequencia_limite()
        
        # 3. Teste de latência (para 10Hz, frequência segura)
        print("\n2️⃣ EXECUTANDO TESTE DE LATÊNCIA")
        resultado_latencia = self.teste_latencia(frequencia_hz=10, num_medições=15)
        
        # 4. Resumo
        print("\n" + "="*60)
        print("📋 RESUMO DOS TESTES")
        print("="*60)
        
        print("\n📊 FREQUÊNCIAS TESTADAS:")
        for freq, dados in resultado_freq.items():
            status = "✅ OK" if dados["status"] == "OK" else "⚠️ LIMITE"
            print(f"  {freq:4d} Hz: {status} ({dados['taxa_sucesso']:.1f}%)")
        
        if resultado_latencia:
            print(f"\n⏱️ LATÊNCIA em 10 Hz:")
            print(f"  • Média: {resultado_latencia['media_ms']:.1f} ms")
            print(f"  • Variação: {resultado_latencia['min_ms']:.1f} a {resultado_latencia['max_ms']:.1f} ms")
            print(f"  • Respostas: {resultado_latencia['respostas']}/{resultado_latencia['total']}")
        
        print("\n✅ Testes concluídos!")
        print("💡 Dica: Verifique também os logs do dashboard para confirmar")

# ===== PONTO DE ENTRADA =====
if __name__ == "__main__":
    tester = TestesAutomatizados()
    
    try:
        tester.executar_todos_testes()
    except KeyboardInterrupt:
        print("\n\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
    finally:
        print("\nFim dos testes automatizados")
        print("O dashboard Neuroestim continua funcionando normalmente! 🎉")