#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait

# Cria o brick
ev3 = EV3Brick()

# Inicializa os sensores
sensor_esquerdo = ColorSensor(Port.S3)
sensor_meio = ColorSensor(Port.S1)
sensor_direito = ColorSensor(Port.S4)

# Dicionários para armazenar os valores calibrados
calibracao = {
    'esquerdo': {'preto': 0, 'branco': 100, 'medio': 50},
    'meio': {'preto': 0, 'branco': 100, 'medio': 50},
    'direito': {'preto': 0, 'branco': 100, 'medio': 50}
}

def calibrar_sensor(sensor, nome, cor):
    """Função para calibrar um sensor específico"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Calibrando " + nome)
    ev3.screen.draw_text(0, 50, "Coloque no " + cor)
    ev3.screen.draw_text(0, 80, "Pressione qualquer botao")
    
    # Espera o usuário pressionar um botão
    while not ev3.buttons.pressed():
        wait(50)
    
    # Faz várias leituras e tira a média
    valores = []
    for i in range(10):
        valores.append(sensor.reflection())
        wait(50)
    
    media = sum(valores) / len(valores)
    
    # Mostra o valor calibrado
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, nome + " no " + cor + ": " + str(int(media)))
    wait(1000)
    
    return media

def calibrar_todos():
    """Função principal de calibração"""
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "CALIBRACAO")
    ev3.screen.draw_text(0, 40, "Vai calibrar:")
    ev3.screen.draw_text(0, 60, "1-Esquerdo 2-Meio 3-Direito")
    ev3.screen.draw_text(0, 80, "Pressione qualquer botao")
    wait(2000)
    
    # Calibra o sensor esquerdo
    calibracao['esquerdo']['preto'] = calibrar_sensor(sensor_esquerdo, "Esquerdo", "PRETO")
    calibracao['esquerdo']['branco'] = calibrar_sensor(sensor_esquerdo, "Esquerdo", "BRANCO")
    calibracao['esquerdo']['medio'] = (calibracao['esquerdo']['preto'] + calibracao['esquerdo']['branco']) / 2
    
    # Calibra o sensor do meio
    calibracao['meio']['preto'] = calibrar_sensor(sensor_meio, "Meio", "PRETO")
    calibracao['meio']['branco'] = calibrar_sensor(sensor_meio, "Meio", "BRANCO")
    calibracao['meio']['medio'] = (calibracao['meio']['preto'] + calibracao['meio']['branco']) / 2
    
    # Calibra o sensor direito
    calibracao['direito']['preto'] = calibrar_sensor(sensor_direito, "Direito", "PRETO")
    calibracao['direito']['branco'] = calibrar_sensor(sensor_direito, "Direito", "BRANCO")
    calibracao['direito']['medio'] = (calibracao['direito']['preto'] + calibracao['direito']['branco']) / 2
    
    # Mostra os resultados finais
    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "CALIBRACAO FINAL:")
    ev3.screen.draw_text(0, 30, "E: Preto=" + str(int(calibracao['esquerdo']['preto'])) + " Branco=" + str(int(calibracao['esquerdo']['branco'])) + " Media=" + str(int(calibracao['esquerdo']['medio'])))
    ev3.screen.draw_text(0, 50, "M: Preto=" + str(int(calibracao['meio']['preto'])) + " Branco=" + str(int(calibracao['meio']['branco'])) + " Media=" + str(int(calibracao['meio']['medio'])))
    ev3.screen.draw_text(0, 70, "D: Preto=" + str(int(calibracao['direito']['preto'])) + " Branco=" + str(int(calibracao['direito']['branco'])) + " Media=" + str(int(calibracao['direito']['medio'])))
    ev3.screen.draw_text(0, 90, "Salvando calibracao...")
    
    # Salva em um arquivo
    salvar_calibracao(calibracao)
    
    wait(3000)
    return calibracao

def salvar_calibracao(dados):
    """Salva os dados de calibração em um arquivo"""
    with open('calibracao.txt', 'w') as f:
        f.write("esquerdo_preto=" + str(dados['esquerdo']['preto']) + "\n")
        f.write("esquerdo_branco=" + str(dados['esquerdo']['branco']) + "\n")
        f.write("esquerdo_medio=" + str(dados['esquerdo']['medio']) + "\n")
        f.write("meio_preto=" + str(dados['meio']['preto']) + "\n")
        f.write("meio_branco=" + str(dados['meio']['branco']) + "\n")
        f.write("meio_medio=" + str(dados['meio']['medio']) + "\n")
        f.write("direito_preto=" + str(dados['direito']['preto']) + "\n")
        f.write("direito_branco=" + str(dados['direito']['branco']) + "\n")
        f.write("direito_medio=" + str(dados['direito']['medio']) + "\n")

def carregar_calibracao():
    """Carrega os dados de calibração do arquivo"""
    try:
        with open('calibracao.txt', 'r') as f:
            linhas = f.readlines()
            
        dados = {
            'esquerdo': {},
            'meio': {},
            'direito': {}
        }
        
        for linha in linhas:
            partes = linha.strip().split('=')
            chave = partes[0]
            valor = float(partes[1])
            
            if 'esquerdo' in chave:
                sensor = 'esquerdo'
            elif 'meio' in chave:
                sensor = 'meio'
            else:
                sensor = 'direito'
                
            atributo = chave.split('_')[1]
            dados[sensor][atributo] = valor
            
        return dados
    except:
        # Se não encontrar o arquivo, retorna None
        return None

# Se executar este arquivo diretamente, faz a calibração
if __name__ == "__main__":
    calibrar_todos()