# src/serial_reader.py
import serial
import requests
import time
import json
import random
from config import PORTA_SERIAL, BAUD_RATE, URL_API, MODO_SIMULACAO

def ler_dados_simulados():
    """Gera dados aleatórios para testar o sistema sem o hardware físico."""
    return {
        "temperatura": round(random.uniform(20.0, 35.0), 1),
        "umidade": round(random.uniform(40.0, 80.0), 1),
        "pressao": round(random.uniform(1000.0, 1020.0), 1)
    }

def iniciar_leitor():
    ser = None
    
    # Se NÃO estiver em simulação, tenta conectar no Arduino
    if not MODO_SIMULACAO:
        try:
            ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=2)
            print(f"Conectado à porta serial {PORTA_SERIAL}")
        except serial.SerialException as e:
            print(f"Erro ao conectar na porta serial: {e}")
            print("Verifique se o Arduino está conectado. Encerrando...")
            return

    print(f"Iniciando envio de dados para {URL_API}...")
    print(f"Modo Simulação: {'ATIVADO' if MODO_SIMULACAO else 'DESATIVADO'}")
    
    while True:
        try:
            dados = None
            
            if MODO_SIMULACAO:
                dados = ler_dados_simulados()
                time.sleep(5)  # Gera novos dados a cada 5 segundos na simulação
            else:
                # Lê os dados reais do Arduino via USB
                if ser and ser.in_waiting > 0:
                    linha = ser.readline().decode('utf-8').strip()
                    if linha:
                        try:
                            # O Arduino precisa enviar os dados no formato JSON
                            dados = json.loads(linha)
                        except json.JSONDecodeError:
                            print(f"Aviso: Dados recebidos não são um JSON válido: {linha}")
                            continue
            
            # Se conseguiu ler os dados (simulados ou reais), envia para o Flask
            if dados:
                resposta = requests.post(URL_API, json=dados)
                
                if resposta.status_code == 201:
                    id_banco = resposta.json().get('id')
                    print(f"[Sucesso] ID {id_banco} salvo -> Temp: {dados['temperatura']}°C | Umid: {dados['umidade']}%")
                else:
                    print(f"[Erro API] Status: {resposta.status_code} - Resposta: {resposta.text}")
                    
        except requests.exceptions.ConnectionError:
            print("[Erro] Falha ao conectar na API. O servidor Flask está rodando?")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nEncerrando leitor serial...")
            break
        except Exception as e:
            print(f"[Erro Inesperado] {e}")
            time.sleep(2)
            
    if ser:
        ser.close()

if __name__ == '__main__':
    iniciar_leitor()