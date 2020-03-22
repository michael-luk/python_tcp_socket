# encoding:gbk
import socket
import threading
import time
import sys

conn_dict = {}


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 6565))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    alive_thread = threading.Thread(target=send_alive)
    alive_thread.start()

    while 1:
        conn, addr = s.accept()
        conn_dict[addr] = conn
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def send_alive():
    while 1:
        print('send alive')
        for value in conn_dict.values():
            value.sendall(('alive\n').encode())
        time.sleep(60)


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    conn.send(('welcome\n').encode())
    while 1:
        data = conn.recv(2048)
        print(u'{0} client send data is {1}'.format(addr,
                                                    data.decode(
                                                        'UTF-8')))
        # time.sleep(1)
        if data.startswith('lyexit') or not data:
            print('{0} connection close'.format(addr))
            conn.send(('closed\n').encode())
            del conn_dict[addr]
            break
			
        for value in conn_dict.values():
            value.sendall(data)
    conn.close()


if __name__ == '__main__':
    socket_service()
