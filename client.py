import socket
import sys


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6565))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024))
    while 1:
        data = input('please input: ').encode()
        s.send(data)
        print('aa', s.recv(1024))
        if data == 'exit':
            break
    s.close()


if __name__ == '__main__':
    socket_client()