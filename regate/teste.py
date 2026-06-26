# teste.py
# Para rodar: python teste.py
#
# IMPORTANTE: coloque este arquivo na mesma pasta que mapa.py

import sys
sys.stdout.reconfigure(encoding='utf-8')

import sys
import types
import fake_pybricks as fp

class FakeMotorGarra:
    log = []
    def run_angle(self, velocidade, graus):
        FakeMotorGarra.log.append(graus)

class FakePort:
    A = "A"; B = "B"; C = "C"; D = "D"
    S1 = "S1"; S2 = "S2"; S3 = "S3"; S4 = "S4"

def _mod(name, **attrs):
    m = types.ModuleType(name)
    m.__dict__.update(attrs)
    sys.modules[name] = m

_mod('pybricks')
_mod('pybricks.hubs',       EV3Brick=object)
_mod('pybricks.ev3devices', Motor=lambda port: FakeMotorGarra(), ColorSensor=object, UltrasonicSensor=object)
_mod('pybricks.parameters', Port=FakePort, Color=fp.Color)
_mod('pybricks.robotics',   DriveBase=object)
_mod('pybricks.tools',      wait=fp.wait)

# Agora podemos importar nossos arquivos normalmente
from mapa import Mapa
from movimento import Movimento
from navegacao import Navegacao

# ============================================================
# UTILITÁRIOS
# ============================================================

passou = 0
falhou = 0

def checar(nome, resultado, esperado):
    global passou, falhou
    if resultado == esperado:
        print(f"  [OK] {nome}")
        passou += 1
    else:
        print(f"  [FALHOU] {nome}")
        print(f"     esperado: {esperado}")
        print(f"     recebi:   {resultado}")
        falhou += 1

def titulo(texto):
    print(f"\n{'='*50}")
    print(f"  {texto}")
    print('='*50)

# ============================================================
# TESTE 1 — MAPA: posição e direção
# ============================================================

titulo("TESTE 1 — Posição e direção")

m = Mapa()
checar("começa em (0,0)",        (m.x, m.y), (0, 0))
checar("começa olhando leste",   m.direcao,  1)
checar("(0,0) já está visitado", m.ja_visitado(), True)

m.mover()
checar("andou pra leste -> (1,0)", (m.x, m.y), (1, 0))

m.mover()
checar("andou mais -> (2,0)",      (m.x, m.y), (2, 0))

m.virar_direita()
checar("virou direita -> sul (2)", m.direcao, 2)

m.mover()
checar("andou pro sul -> (2,1)",   (m.x, m.y), (2, 1))

m.virar_esquerda()
m.virar_esquerda()
checar("virou 2x esquerda -> norte (0)", m.direcao, 0)

m.mover()
checar("andou pro norte -> (2,0)", (m.x, m.y), (2, 0))

# ============================================================
# TESTE 2 — MAPA: visitados
# ============================================================

titulo("TESTE 2 — Lugares visitados")

m2 = Mapa()
checar("(0,0) visitado no início",    m2.ja_visitado(), True)

m2.mover()
checar("(1,0) visitado após andar",   m2.ja_visitado(), True)

m2.virar_direita()
m2.mover()
checar("(1,1) visitado após virar",   m2.ja_visitado(), True)

# volta para (1,0) — já visitado
m2.virar_direita()
m2.virar_direita()
m2.mover()
checar("(1,0) ainda marcado como visitado", m2.ja_visitado(), True)

# ============================================================
# TESTE 3 — MAPA: bolinhas
# ============================================================

titulo("TESTE 3 — Bolinhas")

m3 = Mapa()
m3.registrar_bolinha("cinza")
checar("registrou bolinha cinza em (0,0)", m3.bolinhas["cinza"], [(0, 0)])

m3.mover()
m3.registrar_bolinha("preta")
checar("registrou bolinha preta em (1,0)", m3.bolinhas["preta"], [(1, 0)])

# não duplica
m3.registrar_bolinha("preta")
checar("não duplica bolinha",  len(m3.bolinhas["preta"]), 1)

m3.remover_bolinha("preta", (1, 0))
checar("removeu bolinha preta", m3.bolinhas["preta"], [])

# ============================================================
# TESTE 4 — MAPA: zonas
# ============================================================

titulo("TESTE 4 — Zonas verde e vermelha")

m4 = Mapa()
m4.definir_zona_verde()
checar("zona verde em (0,0)", m4.zona_verde, (0, 0))

m4.mover()
m4.mover()
m4.virar_direita()
m4.mover()
m4.definir_zona_vermelha()
checar("zona vermelha em (2,1)", m4.zona_vermelha, (2, 1))

# ============================================================
# TESTE 5 — NAVEGAÇÃO: verificar() com cores
# ============================================================

titulo("TESTE 5 — Sensor de cor (verificar)")

robot5  = fp.FakeDrive()
# Simula: cinza, preta, verde, vermelha, nenhuma
cores5  = [fp.Color.GRAY, fp.Color.BLACK, fp.Color.GREEN, fp.Color.RED, None]
ultra5  = fp.FakeUltrasonic([500] * 20)
mapa5   = Mapa()
mov5    = Movimento(robot5)
nav5    = Navegacao(robot5, ultra5, fp.FakeColorSensor(cores5), mapa5, mov5)

nav5.verificar()  # cinza em (0,0)
checar("detectou cinza",  mapa5.bolinhas["cinza"], [(0, 0)])

mapa5.mover()
nav5.verificar()  # preta em (1,0)
checar("detectou preta",  mapa5.bolinhas["preta"], [(1, 0)])

mapa5.mover()
nav5.verificar()  # verde em (2,0)
checar("detectou verde",  mapa5.zona_verde, (2, 0))

mapa5.mover()
nav5.verificar()  # vermelha em (3,0)
checar("detectou vermelha", mapa5.zona_vermelha, (3, 0))

mapa5.mover()
nav5.verificar()  # nenhuma cor — não muda nada
checar("cor None não muda bolinhas", len(mapa5.bolinhas["cinza"]), 1)

# ============================================================
# TESTE 6 — NAVEGAÇÃO: zigzag atualiza direção no mapa
# ============================================================

titulo("TESTE 6 — Zigzag atualiza mapa")

robot6 = fp.FakeDrive()
# Parede depois de 4 leituras longe
ultra6 = fp.FakeUltrasonic([500, 500, 500, 500, 80, 500, 500, 500, 500, 80])
cores6 = fp.FakeColorSensor([None] * 20)
mapa6  = Mapa()
mov6   = Movimento(robot6)
nav6   = Navegacao(robot6, ultra6, cores6, mapa6, mov6)

direcao_antes = mapa6.direcao
nav6.zigzag(linhas=2)
direcao_depois = mapa6.direcao

# Após 2 linhas de zigzag a direção deve ter mudado e voltado
# (linha par: 2 viradas direita; linha ímpar: 2 viradas esquerda)
checar("zigzag atualizou direção no mapa (deve ser 1)", mapa6.direcao, 1)

# ============================================================
# RESULTADO FINAL
# ============================================================

print(f"\n{'='*50}")
print(f"  RESULTADO: {passou} passou  |  {falhou} falhou")
print('='*50)

if falhou == 0:
    print("\n  :-) Tudo certo! O código está funcionando.\n")
else:
    print(f"\n  (!)  Tem {falhou} problema(s) pra corrigir.\n")

# ============================================================
# TESTE 7 — RESGATE: garra (fechar e abrir)
# ============================================================

from resgate import Resgate

titulo("TESTE 7 — Garra (fechar e abrir)")

mapa7 = Mapa()
res7  = Resgate(fp.FakeDrive(), fp.FakeUltrasonic([500]*20), fp.FakeColorSensor([None]*20), mapa7, Movimento(fp.FakeDrive()))

FakeMotorGarra.log.clear()
res7.fechar_garra()
checar("fechar garra faz 2 movimentos (girar + voltar)", len(FakeMotorGarra.log), 2)
checar("primeiro movimento é positivo (fecha)", FakeMotorGarra.log[0] > 0, True)
checar("segundo movimento é negativo (volta sensor)", FakeMotorGarra.log[1] < 0, True)

FakeMotorGarra.log.clear()
res7.abrir_garra()
checar("abrir garra faz 2 movimentos (girar + voltar)", len(FakeMotorGarra.log), 2)
checar("primeiro movimento é positivo (abre)", FakeMotorGarra.log[0] > 0, True)
checar("segundo movimento é negativo (volta)", FakeMotorGarra.log[1] < 0, True)

# ============================================================
# TESTE 8 — RESGATE: pegar bolinha lê a cor antes de fechar
# ============================================================

titulo("TESTE 8 — Pegar bolinha (lê cor com S1)")

# Mapa com uma bolinha cinza em (2, 0)
mapa8 = Mapa()
mapa8.bolinhas["cinza"].append((2, 0))
mapa8.zona_verde    = (0, 3)
mapa8.zona_vermelha = (4, 3)

# Sensor de cor retorna CINZA quando chegar perto da bolinha
cores8 = fp.FakeColorSensor([fp.Color.GRAY] * 20)
ultra8 = fp.FakeUltrasonic([500, 500, 30])  # para na 3a leitura
robot8 = fp.FakeDrive()
mov8   = Movimento(robot8)
res8   = Resgate(robot8, ultra8, cores8, mapa8, mov8)

cor_lida = res8.pegar_bolinha((2, 0))
checar("identificou bolinha cinza pelo sensor S1", cor_lida, "cinza")
checar("removeu bolinha cinza do mapa após pegar", mapa8.bolinhas["cinza"], [])

# ============================================================
# TESTE 9 — RESGATE: entregar na zona certa
# ============================================================

titulo("TESTE 9 — Entregar na zona certa")

mapa9 = Mapa()
mapa9.zona_verde    = (0, 0)  # mesma posição do robô, não precisa andar
mapa9.zona_vermelha = (0, 0)

# [500]*5 longe, depois 50 = chegou na zona
ultra9 = fp.FakeUltrasonic([500, 500, 500, 500, 500, 50])
cores9 = fp.FakeColorSensor([None] * 20)
robot9 = fp.FakeDrive()
mov9   = Movimento(robot9)
res9   = Resgate(robot9, ultra9, cores9, mapa9, mov9)

res9.entregar("cinza")
checar("entregou bolinha cinza (zona verde)", res9.entregues, 1)

ultra9.i = 0  # reseta o sensor para a próxima entrega
res9.entregar("preta")
checar("entregou bolinha preta (zona vermelha)", res9.entregues, 2)

# ============================================================
# TESTE 10 — RESGATE: conta entregas corretamente
# ============================================================

titulo("TESTE 10 — Contagem de entregas")

mapa10 = Mapa()
mapa10.zona_verde    = (0, 0)  # mesma posição do robô, não precisa andar
mapa10.zona_vermelha = (0, 0)

# repete o padrão [longe, longe, longe, perto] para cada entrega
ultra10 = fp.FakeUltrasonic([500, 500, 500, 50, 500, 500, 500, 50, 500, 500, 500, 50])
robot10 = fp.FakeDrive()
mov10   = Movimento(robot10)
res10   = Resgate(robot10, ultra10, fp.FakeColorSensor([None]*20), mapa10, mov10)

checar("começa com 0 entregas",     res10.entregues,      0)
checar("total de bolinhas é 3",     res10.total_bolinhas, 3)
checar("missão não completa ainda", res10.entregues < res10.total_bolinhas, True)

res10.entregar("cinza")
res10.entregar("preta")
res10.entregar("cinza")
checar("após 3 entregas missão completa", res10.entregues >= res10.total_bolinhas, True)

# ============================================================
# RESULTADO FINAL (atualizado)
# ============================================================

print(f"\n{'='*50}")
print(f"  RESULTADO FINAL: {passou} passou  |  {falhou} falhou")
print('='*50)

if falhou == 0:
    print("\n  :-) Tudo certo! O código está funcionando.\n")
else:
    print(f"\n  (!)  Tem {falhou} problema(s) pra corrigir.\n") 