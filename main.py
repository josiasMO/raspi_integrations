# -*- coding: utf-8 -*-

from time import sleep

from Lcd import Lcd
from Keypad import Keypad
from Buzzer import Buzzer
from Gprs import GPRS


def main():
    lcd = Lcd()
    keypad = Keypad()
    buzzer = Buzzer()
    gprs = GPRS()

    current_state = 0

    passwd = "33"
    codigo_veiculo = "33"
    codigo_motorista = ""
    codigo_linha = ""

    lcd.show_message("Bem vindo ", "ao SysJourney")
    buzzer.beep("welcome")
    sleep(3)
    #lcd.show_message("Pressione", "*/Inicio")

    while True:
        if current_state == 0:
            lcd.show_message("Pressione", "*/Inicio")
            key = keypad.read_key()
            if key == "*":
                current_state = 1
                buzzer.beep("start_journey")

            elif key == "B":
                current_state = 10
                buzzer.beep("func_menu")

            elif key == "C":
                current_state = 0
                buzzer.beep("cancel")

            else:
                lcd.show_message("Opcao ", "Incorreta")
                buzzer.beep("wrong_key")
                sleep(2)

        elif current_state == 1:
            lcd.show_message("Codigo Veiculo: ", str(codigo_veiculo))
            sleep(3)
            lcd.show_message("Pressione", "A/Confirma")
            key = keypad.read_key()
            if key == "A":
                current_state = 2
                buzzer.beep("confirm")

            elif key == "C":
                current_state = 0
                buzzer.beep("cancel")

            else:
                lcd.show_message("Tecla ", "Incorreta")
                buzzer.beep("wrong_key")
                sleep(2)

        elif current_state == 2:
            lcd.show_message("Informe Codigo", "do Motorista: ")
            sleep(3)
            while True:
                lcd.show_message("Cod Motorista: ", codigo_motorista)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                   key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    codigo_motorista += key
                    buzzer.beep("number")

                elif key == "A":
                    current_state = 3
                    buzzer.beep("confirm")
                    break
                elif key == "C":
                    if codigo_motorista == "":
                        lcd.show_message("Operacao Cancelada!!!")
                        codigo_motorista = ""
                        buzzer.beep("cancel")
                        current_state = 1
                        sleep(3)
                        break
                    else: #Remove last char from string
                        codigo_motorista = codigo_motorista[:-1]
                        buzzer.beep("number")

                else:
                    lcd.show_message("Tecla ", "Incorreta")
                    buzzer.beep("wrong_key")
                    sleep(2)

        elif current_state == 3:
            lcd.show_message("Informe Codigo", "da Linha:")
            sleep(3)
            while True:
                lcd.show_message("Cod da Linha: ", codigo_linha)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                    key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    codigo_linha += key
                    buzzer.beep("number")

                elif key == "A":
                    current_state = 4
                    buzzer.beep("confirm")
                    break
                elif key == "C":
                    if codigo_linha == "":
                        lcd.show_message("Operacao Cancelada!!!")
                        codigo_linha = ""
                        current_state = 1
                        sleep(3)
                        buzzer.beep("cancel")
                        break
                    else: #Remove last char from string
                        codigo_linha = codigo_linha[:-1]
                        buzzer.beep("number")

                else:
                    lcd.show_message("Tecla ", "Incorreta")
                    buzzer.beep("wrong_key")
                    sleep(2)

        elif current_state == 4:
            lcd.show_message("Enviando", "Dados")
            ######HERE GOES THE CODE TO SEND THE DATA TO THE SERVER#####
            recv = []
            while True:
                recv = gprs.send([codigo_veiculo,codigo_motorista,codigo_linha])
                if recv:
                    break
                sleep(10)

            lcd.show_message("Dados", "Enviados")
            current_state = 5
            lcd.show_message("Jornada", "Iniciada")
            buzzer.beep("start_journey")
            sleep(5)

        elif current_state == 5:
            lcd.show_message("Jornada", "em Progresso")
            key = keypad.read_key()
            if key == "#":
                lcd.show_message("Encerrando", "Jornada")
                buzzer.beep("end_journey")
                sleep(3)
                ######HERE GOES THE CODE TO SEND THE DATA TO THE SERVER#####
                lcd.show_message("Jornada", "Encerrada")
                current_state = 0
            else:
                lcd.show_message("Tecla ", "Incorreta")
                buzzer.beep("wrong_key")
                sleep(2)

        ######################## MENU FUNCAO ########################
        elif current_state == 10:
            lcd.show_message("Selecionar", "Funcao")
            sleep(3)
            lcd.show_message("1- Cod. Veiculo", "2- Alterar Senha")
            key = keypad.read_key()
            if key == "1":
                current_state = 11
                buzzer.beep("confirm")

            elif key == "2":
                current_state = 21
                buzzer.beep("confirm")

            elif key == "C":
                current_state = 0
                buzzer.beep("cancel")

            else:
                lcd.show_message("Tecla ", "Incorreta")
                buzzer.beep("wrong_key")
                sleep(2)

        ######################## ALTERAR CODIGO DO VEICULO ########################
        elif current_state == 11:
            senha = ""
            while True:
                lcd.show_message("Informe Senha: ", senha)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                    key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    senha += key
                    buzzer.beep("number")

                elif key == "A":
                    buzzer.beep("confirm")

                    if senha == passwd:
                        current_state = 12
                        break
                    else:
                        lcd.show_message("Senha", "Incorreta")
                        buzzer.beep("wrong_key")
                        sleep(2)
                        senha = ""

                elif key == "C":
                    if codigo_veiculo == "":
                        lcd.show_message("Operacao Cancelada!!!")
                        current_state = 10
                        sleep(3)
                        buzzer.beep("cancel")
                        break
                    else: #Remove last char from string
                        senha = senha[:-1]
                        buzzer.beep("number")

                else:
                    lcd.show_message("Tecla", "Incorreta")
                    buzzer.beep("wrong_key")
                    sleep(2)

        elif current_state == 12:
            codigo_veiculo = ""
            lcd.show_message("Alterar Cod.", "Veiculo")
            sleep(3)
            lcd.show_message("Cod. Veiculo")
            while True:
                lcd.show_message("Cod. Veiculo: ", codigo_veiculo)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                    key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    codigo_veiculo += key
                    buzzer.beep("number")

                elif key == "A":
                    current_state = 13
                    buzzer.beep("confirm")
                    break
                elif key == "C":
                    if codigo_veiculo == "":
                        lcd.show_message("Operacao Cancelada!!!")
                        codigo_veiculo = ""
                        current_state = 1
                        sleep(3)
                        buzzer.beep("cancel")
                        break
                    else: #Remove last char from string
                        codigo_veiculo = codigo_veiculo[:-1]
                        buzzer.beep("number")

                else:
                    lcd.show_message("Tecla ", "Incorreta")
                    buzzer.beep("wrong_key")
                    sleep(2)

        elif current_state == 13:
            lcd.show_message("Cod Veiculo", "Alterado")
            sleep(3)
            current_state = 0

        ######################## ALTERAR CODIGO DO VEICULO ########################
        elif current_state == 21:
            senha = ""
            while True:
                lcd.show_message("Informe Senha: ", senha)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                    key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    senha += key
                    buzzer.beep("number")

                elif key == "A":
                    buzzer.beep("confirm")

                    if senha == passwd:
                        current_state = 22
                        break
                    else:
                        lcd.show_message("Senha", "Incorreta")
                        buzzer.beep("wrong_key")
                        sleep(2)
                        senha = ""

                elif key == "C":
                    if codigo_veiculo == "":
                        lcd.show_message("Operacao Cancelada!!!")
                        current_state = 10
                        sleep(3)
                        buzzer.beep("cancel")
                        break
                    else: #Remove last char from string
                        senha = senha[:-1]
                        buzzer.beep("number")

                else:
                    lcd.show_message("Tecla", "Incorreta")
                    buzzer.beep("wrong_key")
                    sleep(2)

        elif current_state == 22:
            senha = ""
            while True:
                lcd.show_message("Nova Senha:", senha)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                    key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    senha += key
                    buzzer.beep("number")

                elif key == "A":
                    passwd = senha
                    current_state = 23
                    buzzer.beep("confirm")
                    break
                elif key == "C":
                    if senha == "":
                        lcd.show_message("Operacao Cancelada!!!")
                        senha = ""
                        current_state = 1
                        sleep(3)
                        buzzer.beep("cancel")
                        break
                    else: #Remove last char from string
                        senha = senha[:-1]
                        buzzer.beep("number")

                else:
                    lcd.show_message("Tecla ", "Incorreta")
                    buzzer.beep("wrong_key")
                    sleep(2)

        elif current_state == 23:
            senha = ""
            while True:
                lcd.show_message("Nova Senha:", senha)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or \
                                key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    senha += key
                    buzzer.beep("number")

                elif key == "A":
                    buzzer.beep("confirm")
                    if senha == passwd:
                        current_state = 0
                        break
                    else:
                        lcd.show_message("Senha", "Incorreta")
                        current_state = 22

                elif key == "C":
                    if senha == "":
                        lcd.show_message("Operacao Cancelada!!!")
                        senha = ""
                        current_state = 1
                        sleep(3)
                        buzzer.beep("cancel")
                        break
                    else:  # Remove last char from string
                        senha = senha[:-1]
                        buzzer.beep("number")

                else:
                    lcd.show_message("Tecla ", "Incorreta")
                    buzzer.beep("wrong_key")
                    sleep(2)


if __name__ == "__main__":
    main()
