#!/usr/bin/env pybricks-micropython
from calibracao import carregar_calibracao

# Carrega a calibração uma vez
DADOS_CALIBRACAO = carregar_calibracao()

def ler_sensor_calibrado(sensor, nome_sensor):
    """
    Lê o valor do sensor e retorna normalizado (0 a 100)
    onde 0 = preto e 100 = branco
    """
    if DADOS_CALIBRACAO is None:
        # Se não tem calibração, usa valores padrão
        return sensor.reflection()
    
    valor_bruto = sensor.reflection()
    
    # Pega os valores calibrados para este sensor
    preto = DADOS_CALIBRACAO[nome_sensor]['preto']
    branco = DADOS_CALIBRACAO[nome_sensor]['branco']
    
    # Normaliza o valor (mapeia de preto-branco para 0-100)
    if branco - preto == 0:
        return 50  # Evita divisão por zero
    
    valor_normalizado = (valor_bruto - preto) / (branco - preto) * 100
    
    # Limita entre 0 e 100
    if valor_normalizado < 0:
        return 0
    if valor_normalizado > 100:
        return 100
    return valor_normalizado

def ler_todos_sensores(sensor_e, sensor_m, sensor_d):
    """Lê todos os sensores já calibrados"""
    esquerdo = ler_sensor_calibrado(sensor_e, 'esquerdo')
    meio = ler_sensor_calibrado(sensor_m, 'meio')
    direito = ler_sensor_calibrado(sensor_d, 'direito')
    
    return esquerdo, meio, direito