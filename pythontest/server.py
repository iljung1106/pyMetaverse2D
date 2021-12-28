import socket
from _thread import *
from threading import Thread

clients = []
clientInfos = {}
def threaded(client_socket, addr): 
    name = ''
    print('Connected by :', addr[0], ':', addr[1]) 
    global clients
    clients.append(client_socket)
    for i in clientInfos.keys():
        tmpdata = ">"
        tmpdata += i + '|' + clientInfos[i]
        tmpdata = tmpdata.encode()
        client_socket.sendall(tmpdata)
    while True: 
        dobreak = False
        # try:
        if True: #임시
            datas = client_socket.recv(1024)
            datas = datas.decode()
            for data in datas.split('&&'):

                if not data: 
                    break

                # print('Received from ' + addr[0],':',addr[1] , data)

                if data[0] == '`':
                    for i in clients:
                        if i:
                            i.sendall(data.encode()) 
                if data[0] == '<':
                    del clientInfos[name]
                    for i in clients:
                        if i:
                            i.sendall(data.encode()) 
                            start_new_thread(lateSendall, (i, data)) 
                            dobreak = True
                            clients.remove(client_socket)
                            print('remove')
                            client_socket.close() 
                            break
                elif data[0] == '>':
                    tmp = data[1:].split('|')
                    clientInfos[tmp[0]] = tmp[1]
                    name = tmp[0]
                    for i in clients:
                        if i != client_socket:
                            if i:
                                i.sendall(data.encode())              
                elif data[0] == '~':
                    for i in clients:
                        if i and data:
                            i.sendall(data.encode()) 
        if dobreak:
            break

        # except ConnectionResetError as e:
        #     clients.remove(client_socket)
        #     del clientInfos[name]
        #     print('Disconnected by ' + addr[0],':',addr[1])
        #     tmpdata = "<"
        #     tmpdata += name + '|' + clientInfos[name]
        #     tmpdata = tmpdata.encode()
        #     client_socket.sendall(tmpdata)
        #     break
             
    client_socket.close() 


def lateSendall(i, data):
    i.sendall(data.encode())
    print('lateSend')



HOST = '0.0.0.0'
PORT = 25565

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')


while True: 

    print('wait')


    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close()
while 1:
    pass