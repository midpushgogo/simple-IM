import socket
import threading
import sys


def receive(s):
    while True:
        try:
            data = s.recv(1024)
        except ConnectionError as e:
            print('the connect is over')
            sys.exit()
        print(data.decode('utf-8'))


def talk(s):  # 作为服务器接受到exit时talk线程无法退出
    while True:
        data = input()
        if data == 'exit':
            s.close()
            sys.exit()
        s.send(data.encode('utf-8'))


def server(name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8999))
    s.listen(5)
    print('waiting for connection')
    while True:
        sock, addr = s.accept()
        print('find a new connect  IP:%s port:%s'%addr)
        sock.send(name.encode('utf-8'))
        object = sock.recv(1024).decode('utf-8')
        print('connect successfully. object name is {}'.format(object))
        t = threading.Thread(target=talk, args=(sock,))
        r = threading.Thread(target=receive, args=(sock,))
        r.start()
        t.start()


def client(name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input('input the IP you want to connect:')
    c=s.connect_ex((ip, 8999))
    while c!=0:
        print('connection failed, error code {}'.format(c))
        ip = input('input the IP you want to connect:')
        c = s.connect_ex((ip, 8999))
    s.send(name.encode('utf-8'))
    object = s.recv(1024).decode('utf-8')
    print('connect successfully. object name is {}'.format(object))
    r = threading.Thread(target=receive, args=(s,))
    t = threading.Thread(target=talk, args=(s,))
    t.start()
    r.start()



if __name__ == '__main__':
    name = input('please input your name:')
    choose = input('connect or listen for connection?(1/2)')
    if choose == '1':
        server(name)
    else:
        client(name)