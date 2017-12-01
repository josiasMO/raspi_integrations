# -*- coding: utf-8 -*-

from time import sleep
import json
from threading import Thread, Lock, Event
from queue import Queue
import os

from Lcd import Lcd
from Keypad import Keypad
from Buzzer import Buzzer
from Gprs import GPRS
from Rfid import Rfid



######### State Machine Variables ##########
current_state = 0
passwd = "33"
codigo_veiculo = "33"
codigo_motorista = ""
codigo_linha = ""
date_time = []
############################################

######### Instances of the Modules #########
lcd = Lcd()
keypad = Keypad()
buzzer = Buzzer()
gprs = GPRS()
############################################

############ Rfid variables  ###############
CARDS = ["[154, 99, 3, 197, 63]", "[151, 25, 214, 53, 109]"]
KEYCHAINS = ["[213, 1, 9, 136, 85]", "[5, 214, 17, 136, 74]"]

RFID_PRESENT = False
if RFID_PRESENT:
    rfid = Rfid()
lock = Lock()
read_result = ""


############################################

def convert_int(x):
    tmp = int(x)
    c = tmp >> 8
    f = tmp % 256
    return str(c), str(f)

def write_json():
    global current_state, passwd, codigo_motorista, codigo_linha, codigo_veiculo, date_time
    data = {}
    data['vehicle'] = []
    data['vehicle'].append({
        'current_state': current_state,
        'passwd': passwd,
        'codigo_veiculo': codigo_veiculo,
        'codigo_motorista': codigo_motorista,
        'codigo_linha': codigo_linha,
        'date_time': date_time

    })
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

def read_json():
    global current_state, passwd, codigo_motorista, codigo_linha, codigo_veiculo, date_time
    with open('data.txt') as json_file:
        data = json.load(json_file)
        current_state = data['vehicle'][0]['current_state']
        passwd = data['vehicle'][0]['passwd']
        codigo_veiculo = data['vehicle'][0]['codigo_veiculo']
        codigo_motorista = data['vehicle'][0]['codigo_motorista']
        codigo_linha = data['vehicle'][0]['codigo_linha']
        date_time = data['vehicle'][0]['date_time']


def cancel():
    global current_state
    current_state = 0
    buzzer.beep("cancel")
    write_json()

def confirm(buzzer_beep, state=None):
    global current_state
    current_state = state
    buzzer.beep(buzzer_beep)
    write_json()

def wrong_key():
    lcd.show_message("Tecla ", "Incorreta")
    buzzer.beep("wrong_key")
    sleep(2)

def return_state(state=None):
    global current_state
    lcd.show_message("Operacao", "Cancelada!!!")
    buzzer.beep("cancel")
    current_state = state
    write_json()
    sleep(3)


def read_codes(message1, message2, message_ini="Informe Codigo", current_val="", event=False):
    lcd.show_message(message_ini, message1)
    sleep(2)
    value = current_val
    while True:
        lcd.show_message(message2, str(value))
        key = keypad.read_key(event)

        if key == "":
            return None

        elif key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or\
                   key == "5" or key == "6" or key == "7" or key == "8" or key == "9":
            value += str(key)
            buzzer.beep("number")

        elif key == "con":
            return value

        elif key == "can":
            if value == "":
                return -1

            else:  # Remove last char from string
                value = value[:-1]
                buzzer.beep("number")
        else:
            wrong_key()

def read_rfid(event, linha):
    valid = False
    value = ""
    while (not event.is_set()):
        uid = str(rfid.read_rfid(event))
        if (uid in KEYCHAINS) and linha:
            value = KEYCHAINS.index(str(uid)) + 1
            break
        elif (uid in CARDS) and not linha:
            value = CARDS.index(str(uid)) + 1
            break
    return str(value)

def manage_read(linha, message1="", message2="", message_ini="Informe Codigo", current_val=""):
    global read_result
    event = Event()
    que = Queue()

    if RFID_PRESENT:
        rfid_reader = Thread(target=lambda q, e, l: q.put(read_rfid(e, l)), args=(que, event, linha))
        rfid_reader.start()

    keypad_reader = Thread(target=lambda q, e,  m1, m2, m3, cv: q.put(read_codes(m1, m2, m3, cv, e)),
                           args=(que, event, message1, message2, message_ini, current_val,))

    keypad_reader.start()

    while que.empty():
        pass
    read_result = que.get()
    event.set()

def main():
    global current_state, passwd, codigo_motorista, codigo_linha, codigo_veiculo, read_result, date_time

    read_json()

    lcd.show_message("Bem vindo ", "ao SysJourney")
    buzzer.beep("welcome")
    sleep(3)

    while True:

        ########################Inicio########################
        if current_state == 0:
            lcd.show_message("Pressione", "Inicio")
            key = keypad.read_key()
            if key == "ini":
                confirm("start_journey", 1)

            elif key == "fun":
                confirm("func_menu", 10)

            elif key == "can":
                cancel()

            else:
                wrong_key()

        ######################## Confirma Codigo do Veiculo ########################
        elif current_state == 1:
            lcd.show_message("Codigo Veiculo: ", str(codigo_veiculo))
            sleep(3)
            lcd.show_message("Pressione", "Confirma")
            key = keypad.read_key()
            if key == "con":
                confirm("confirm", 2)

            elif key == "can":
                return_state(0)

            else:
                wrong_key()

        ######################## Informa Codigo do Motorista ########################
        elif current_state == 2:
            thread = Thread(target=manage_read,
                            args=(False, "do Motorista: ", "Cod Motorista: ", "Informe Codigo", codigo_motorista))
            thread.start()
            thread.join()
            value = read_result
            read_result = ""

            # value = read_codes("do Motorista: ", "Cod Motorista: ", current_val=codigo_motorista)
            if value == -1:
                codigo_motorista = ""
                return_state(1)
            else:
                codigo_motorista = value
                confirm("confirm", 3)

        ######################## Informa Codigo da Linha ########################
        elif current_state == 3:
            thread = Thread(target=manage_read,
                             args=(True, "da Linha: ", "Cod da Linha: ", "Informe Codigo", codigo_linha))
            thread.start()
            thread.join()
            value = read_result
            read_result = ""
            if value == -1:
                codigo_linha = ""
                return_state(2)
            else:
                codigo_linha = value
                date_time = gprs.get_time()
                confirm("confirm", 4)
        ######################## Envio dos Dados / Jornada Iniciada ########################
        elif current_state == 4:
            lcd.show_message("Enviando", "Dados")
            ######HERE GOES THE CODE TO SEND THE DATA TO THE SERVER#####
            write_json()
            recv = []
            num = 1
            while num<=4:
                v = convert_int(codigo_veiculo)
                m = convert_int(codigo_motorista)
                l = convert_int(codigo_linha)
                data = [v[0], v[1], m[0], m[1], l[0], l[1], '1'] + date_time
                recv = gprs.send(data)
                if recv:
                    lcd.show_message("Dados", "Enviados")
                    lcd.show_message("Jornada", "Iniciada")
                    confirm("start_journey", 5)
                    break
                elif(num == 4):
                    lcd.show_message("Erro", "Envio")
                    buzzer.beep("wrong_key")
                    current_state = 0
                    write_json()
                    break
                else:
                    num+=1
                    sleep(10)

        ######################## Jornada Encerrada / Envio dos Dados ########################
        elif current_state == 5:
            lcd.show_message("Jornada", "em Progresso")
            key = keypad.read_key()
            if key == "fim":
                date_time = gprs.get_time()
                lcd.show_message("Encerrando", "Jornada")
                buzzer.beep("end_journey")
                ######HERE GOES THE CODE TO SEND THE DATA TO THE SERVER#####
                recv = []
                num = 1
                write_json()
                while num<=4:
                    v = convert_int(codigo_veiculo)
                    m = convert_int(codigo_motorista)
                    l = convert_int(codigo_linha)
                    data = [v[0], v[1], m[0], m[1], l[0], l[1], '0'] + date_time
                    recv = gprs.send(data)
                    if recv:
                        lcd.show_message("Jornada", "Encerrada")
                        confirm("end_journey", 0)
                        break
                    elif(num == 4):
                        lcd.show_message("Erro", "Envio")
                        buzzer.beep("wrong_key")
                        current_state = 5
                        write_json()
                        break
                    else:
                        num+=1
                        sleep(10)
            else:
                wrong_key()

        ######################## MENU FUNCAO ########################
        elif current_state == 10:
            lcd.show_message("Selecionar", "Funcao")
            sleep(3)
            lcd.show_message("1- Cod. Veiculo", "2- Alterar Senha")
            key = keypad.read_key()
            if key == "1":
                current_state = 11
                buzzer.beep("confirm")
                write_json()

            elif key == "2":
                current_state = 21
                buzzer.beep("confirm")
                write_json()

            elif key == "0":
                current_state = 31
                buzzer.beep("confirm")
                write_json()

            elif key == "can":
                cancel()
            else:
                wrong_key()

        ######################## ALTERAR CODIGO DO VEICULO ########################
        ######################## Informa Senha Atual ########################
        elif current_state == 11:
            senha = read_codes("", "Informe Senha: ", "")

            if senha == -1:
                lcd.show_message("Operacao", "Cancelada!!!")
                return_state(10)

            elif senha == passwd:
                confirm("confirm", 12)

            else:
                lcd.show_message("Senha", "Incorreta")
                buzzer.beep("wrong_key")
                sleep(2)

        ######################## Informa Codigo da Veiculo ########################
        elif current_state == 12:
            value = read_codes("do Veiculo:", "Cod. Veiculo", current_val=codigo_veiculo)
            if value == -1:
                codigo_veiculo = ""
                return_state(1)
            else:
                codigo_veiculo = value
                confirm("confirm")
                sleep(3)
                lcd.show_message("Cod Veiculo", "Alterado")
                confirm("confirm", 0)

        ######################## ALTERAR SENHA ########################
        ######################## Informa Senha Atual ########################
        elif current_state == 21:
            senha = read_codes("", "Informe Senha: ", "")

            if senha == -1:
                lcd.show_message("Operacao", "Cancelada!!!")
                return_state(10)

            elif senha == passwd:
                confirm("confirm", 22)

            else:
                lcd.show_message("Senha", "Incorreta")
                buzzer.beep("wrong_key")
                sleep(2)

        ######################## Nova Senha ########################
        elif current_state == 22:
            senha = read_codes("", "Nova Senha: ", "")

            if senha == -1:
                lcd.show_message("Operacao", "Cancelada!!!")
                return_state(10)

            else:
                confirm("confirm", 23)

        ######################## Confirma Nova Senha ########################
        elif current_state == 23:
            senha = read_codes("", "Confirme Senha: ", "")

            if senha == -1:
                lcd.show_message("Operacao", "Cancelada!!!")
                return_state(10)

            elif senha == passwd:
                confirm("confirm", 0)

            else:
                lcd.show_message("Senha", "Incorreta")
                return_state(22)


        ######################## Reiniciar Sistema ########################
        elif current_state == 31:
            lcd.show_message("Reiniciar", "Sistema")
            sleep(1)
            senha = read_codes("", "Informe Senha: ", "")

            if senha == -1:
                lcd.show_message("Operacao", "Cancelada!!!")
                return_state(10)

            elif senha == passwd:
                confirm("confirm", 32)

            else:
                lcd.show_message("Senha", "Incorreta")
                buzzer.beep("wrong_key")
                sleep(2)

        ######################## Reiniciando Sistema ########################
        elif current_state == 32:
            lcd.show_message("Reiniciando", "Sistema")
            confirm("confirm", 0)
            os.system('sudo reboot now')


if __name__ == "__main__":
    main()
