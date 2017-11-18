import socket
import binascii

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', 5555))
    connection.listen(10)
    while True:
        current_connection, address = connection.accept()
        while True:

            data = current_connection.recv(2048)
            received = binascii.hexlify(data)

            print ("Received data: ",received)

            if data == 'quit\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                break

            elif data == 'stop\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif received[:4] == b'7878':

                strpackage = ' '.join(received[i: i + 2] for i in range(0, len(received), 2))
                strpackage = strpackage.split()


                strpackage = [int(p, 16) for p in strpackage]
                print('Veiculo', strpackage[4]<<8 | strpackage[5])
                print('Motorista', strpackage[6]<<8 | strpackage[7])
                print('Linha ', strpackage[8]<<8 | strpackage[9])
                print('Inicio/Fim %d' % strpackage[10])


                current_connection.send(data)
                break


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
