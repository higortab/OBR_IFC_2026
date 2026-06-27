#!/usr/bin/env pybricks-micropython
#
# Como usar:
#   Abra este arquivo no VS Code com a extensão EV3 MicroPython
#   e faça o upload para o brick. Execute main.py no EV3.
#
# Estrutura de arquivos necessária no EV3:
#   /home/robot/
#       config.py
#       sensors.py
#       motors.py
#       intersection.py
#       obstacles.py
#       line_follow.py
#       main.py
#
# ============================================================

from pybricks.hubs       import EV3Brick
from pybricks.parameters import Button
from pybricks.tools      import wait

# Importa o loop principal
from line_follow import iniciar_segue_linha

# --- Instância do brick para feedback visual/sonoro ---
ev3 = EV3Brick()


def aguardar_botao() -> None:
    """
    Aguarda o pressionamento do botão CENTRAL do EV3 para iniciar.
    Exibe mensagem de pronto na tela.
    """
    ev3.screen.clear()
    ev3.screen.print("OBR 2026")
    ev3.screen.print("Pressione CENTER")
    ev3.screen.print("para iniciar")

    while Button.CENTER not in ev3.buttons.pressed():
        wait(50)

    # Beep de confirmação
    ev3.speaker.beep(frequency=800, duration=200)
    wait(300)
    ev3.screen.clear()
    ev3.screen.print("Iniciando...")
    wait(500)


def main() -> None:
    """Função principal."""
    aguardar_botao()
    iniciar_segue_linha()


# --- Execução ---
if __name__ == '__main__':
    main()