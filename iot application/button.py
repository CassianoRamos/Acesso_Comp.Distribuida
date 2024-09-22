#import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522
import time
import csv
from datetime import datetime
import requests

# Configuração dos pinos e periféricos
#leitorRFid = SimpleMFRC522()
usuarios = {837196207282: "Fulano", 11: "Beltrano", 634156810886: "Ciclano"}
usuarios_autorizados = {837196207282: "Fulano", 11: "Beltrano"}
acesso_diario = {}
tempo_entrada = {}
numero_tentativas = {}

led_verde = 5
led_vermelho = 3
buzzer = 37
entrada = False
tentativas_invasao = 0

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(led_verde, GPIO.OUT)
#GPIO.setup(led_vermelho, GPIO.OUT)
#GPIO.setup(buzzer, GPIO.OUT)


# Função para enviar o POST request
def send_post_request(mensagem):
    data = {'data': mensagem}
    try:
        response = requests.post('http://localhost:5000', json=data)
        if response.status_code == 201:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Erro ao enviar mensagem: {response.status_code}")
    except Exception as e:
        print(f"Erro na conexão: {e}")

# Função para verificar a tag RFID lida
def verificar_tag(tag):
    global entrada
    if tag in usuarios_autorizados:
        if tag not in acesso_diario:
            print(f"Bem vindo {usuarios_autorizados[tag]}!")
            acesso_diario[tag] = usuarios_autorizados
            entrada = True
            ligar_leds("verde", invasao=False)
            novo_log(tag, usuarios[tag], "Usuário autorizado", "Entrada", None)
            tempo_entrada[tag] = datetime.now()
            send_post_request(f"Entrada de {usuarios[tag]} registrada. Horário: {datetime.now()}")
        elif entrada == True:
            print(f"Volte Sempre {usuarios_autorizados[tag]}!")
            tempo_inicial = tempo_entrada[tag]
            tempo_atual = datetime.now()
            tempo_na_sala = tempo_atual - tempo_inicial
            entrada = False
            novo_log(tag, usuarios[tag], "Usuário autorizado", "Saída", tempo_na_sala)
            send_post_request(f"Saída de {usuarios[tag]} registrada. Horário: {datetime.now()}")
        else:
            print(f"Bem vindo de volta {usuarios_autorizados[tag]}!")
            entrada = True
            ligar_leds("verde", invasao=False)
            novo_log(tag, usuarios[tag], "Usuário autorizado", "Entrada", None)
            send_post_request(f"Entrada de {usuarios[tag]} registrada. Horário: {datetime.now()}")
    elif tag in usuarios:
        print(f"Você não tem acesso a este projeto, {usuarios[tag]}")
        ligar_leds("vermelho", invasao=False)
        if tag not in numero_tentativas:
            numero_tentativas[tag] = (usuarios[tag], 1)
        else:
            nome, tentativas = numero_tentativas[tag]
            tentativas += 1
            numero_tentativas[tag] = (nome, tentativas)
        nome, tentativas = numero_tentativas[tag]
        novo_log(tag, nome, f"Usuário não autorizado - Tentativas: {tentativas}", None, None)
        send_post_request(f"Tentativa não autorizada de {nome}. Horário: {datetime.now()}")
    else:
        print(f"Identificação não encontrada!")
        global tentativas_invasao
        tentativas_invasao += 1
        ligar_leds("vermelho", invasao=True)
        novo_log(tag, f"Tentativas de invasão: {tentativas_invasao}", None, None, None)
        send_post_request(f"Tentativa de invasão detectada! Horário: {datetime.now()}")

# Função para controlar LEDs
def ligar_leds(led, invasao):
    if led == "verde":
        #GPIO.output(led_verde, GPIO.HIGH)
        print("ligar Led verde")
        time.sleep(1)
        print("desligar Led verde")
        #GPIO.output(led_verde, GPIO.LOW)
    elif led == "vermelho":
        for i in range(10 if invasao else 5):
            #GPIO.output(led_vermelho, GPIO.HIGH)
            #GPIO.output(buzzer, GPIO.HIGH)
            print("ligar Led vermelho")
            time.sleep(0.5)
            #GPIO.output(led_vermelho, GPIO.LOW)
            #GPIO.output(buzzer, GPIO.LOW)
            print("desligar Led vermelho")
            time.sleep(0.5)

# Função para registrar logs
def novo_log(log, usuario, autorizacao, entrada_saida, tempo):
    with open('logs.csv', mode='a', newline='', encoding='utf-8') as arquivo_csv:
        dados = csv.writer(arquivo_csv)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dados.writerow([data_hora, log, usuario, autorizacao, entrada_saida, tempo])

# Loop principal de execução
try:
    while True:
        #GPIO.output(led_verde, GPIO.LOW)
        #GPIO.output(led_vermelho, GPIO.LOW)
        
        print("Aguardando leitura da tag...")
        tag = int(input("Digite o ID do usuário: "))
        #tag, text = leitorRFid.read()
        verificar_tag(tag)

      
except KeyboardInterrupt:
    print("Programa interrompido")
finally:
    #GPIO.cleanup()
    print("Fim do programa")
