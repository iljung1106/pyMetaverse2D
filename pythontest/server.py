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

        try:
            data = client_socket.recv(1024)

            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break

            print('Received from ' + addr[0],':',addr[1] , data.decode())

            if data.decode()[0] == '`':
                for i in clients:
                    i.sendall(data) 
            elif data.decode()[0] == '>':
                tmp = data.decode()[1:].split('|')
                clientInfos[tmp[0]] = tmp[1]
                name = tmp[1]
                for i in clients:
                    if i != client_socket:
                        i.sendall(data)              
            elif data.decode()[0] == '~':
                for i in clients:
                    i.sendall(data) 

        except ConnectionResetError as e:
            clients.remove(client_socket)
            del clientInfos[name]
            print('Disconnected by ' + addr[0],':',addr[1])
            tmpdata = "<"
            tmpdata += name + '|' + clientInfos[name]
            tmpdata = tmpdata.encode()
            client_socket.sendall(tmpdata)
            break
             
    client_socket.close() 


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
