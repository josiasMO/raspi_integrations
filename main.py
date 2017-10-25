from time import sleep

from Lcd import Lcd
from Keypad import Keypad

CODIGO_VEICULO = 666


def main():
    lcd = Lcd()
    keypad = Keypad()

    current_state = 0

    codigo_motorista = ""
    codigo_linha = ""

    lcd.show_message("Bem vindo", "Pressione */Inicio")
    while True:
        if current_state == 0:
            key = keypad.read_key()
            if key == "*":
                current_state = 1
            else:
                lcd.show_message("Opcao Incorreta", "Pressione */Inicio")

        elif current_state == 1:
            lcd.show_message("Codigo do Veiculo: "+str(CODIGO_VEICULO) , "Pressione A/Confirma")
            key = keypad.read_key()
            if key == "A":
                current_state = 1
            # else:

        elif current_state == 2:
            while True:
                lcd.show_message("Informe Codigo do Motorista: ", codigo_motorista)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                   key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    codigo_motorista += key
                    # lcd.show_message("Informe Codigo do Motorista: ", codigo_motorista)

                elif key == "A":
                    current_state = 3
                    break
                elif key == "C":
                    lcd.show_message("Operacao Cancelada!!!")
                    codigo_motorista = ""
                    sleep(3)
                    break
                else:
                    lcd.show_message("Tecla incorreta!!!")
                    sleep(3)

        elif current_state == 3:
            while True:
                lcd.show_message("Informe Codigo da Linha: ", codigo_linha)
                key = keypad.read_key()

                if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                    key == "5" or key == "6" or key == "7" or key == "8" or key == "9":

                    codigo_linha += key
                    # lcd.show_message("Informe Codigo da Motorista: ", codigo_motorista)

                elif key == "A":
                    current_state = 4
                    break
                elif key == "C":
                    lcd.show_message("Operacao Cancelada!!!")
                    codigo_linha = ""
                    sleep(3)
                    break
                else:
                    lcd.show_message("Tecla incorreta!!!")
                    sleep(3)




if __name__ == "__main__":
    main()