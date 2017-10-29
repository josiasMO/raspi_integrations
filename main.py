from time import sleep

from Lcd import Lcd
from Keypad import Keypad
from Buzzer import Buzzer

CODIGO_VEICULO = 666


def main():
    lcd = Lcd()
    keypad = Keypad()
    buzzer = Buzzer()

    current_state = 0

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
            else:
                lcd.show_message("Opcao ", "Incorreta")
                lcd.show_message("Pressione", "*/Inicio")

        elif current_state == 1:
            lcd.show_message("Codigo Veiculo: ", str(CODIGO_VEICULO))
            sleep(3)
            lcd.show_message("Pressione", "A/Confirma")
            key = keypad.read_key()
            if key == "A":
                current_state = 2
                buzzer.beep("confirm")
            # else:

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
                    lcd.show_message("Operacao Cancelada!!!")
                    codigo_motorista = ""
                    buzzer.beep("cancel")
                    sleep(3)
                    break
                else:
                    lcd.show_message("Tecla incorreta!!!")
                    buzzer.beep("wrong_key")
                    sleep(3)

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
                    lcd.show_message("Operacao Cancelada!!!")
                    codigo_linha = ""
                    sleep(3)
                    buzzer.beep("cancel")
                    break
                else:
                    lcd.show_message("Tecla incorreta!!!")
                    buzzer.beep("wrong_key")
                    sleep(3)
        elif current_state == 4:
            lcd.show_message("Enviando", "Dados")
            ######HERE GOES THE CODE TO SEND THE DATA TO THE SERVER#####
            sleep(3)
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


if __name__ == "__main__":
    main()