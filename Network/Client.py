
from socket import *

server = '127.0.0.1'
port = 2121

# server = '0.tcp.eu.ngrok.io'
# port = 16602

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((server, port))


def Help():
    print('1 - HELP ---------- Print this list of commands')
    print('2 - LIST ---------- Show files and size of files')
    print('3 - PWD  ---------- Show current working directory')
    print('4 - DWLD ---------- Download a file from server')
    print('5 - CD   ---------- Change directory')
    print('6 - QUIT ---------- Exit')


def List(order):
    clientSocket.send(order.encode())
    response = clientSocket.recv(1024).decode()
    print(response)

def Pwd(order):
    clientSocket.send(order.encode())
    response = clientSocket.recv(1024).decode()
    print(response)

def Cd(order):
    clientSocket.send(order.encode())
    response = clientSocket.recv(1024).decode()
    print(response)


# def Dwld(port,filename):                          #   
#     downloadSocket = socket(AF_INET,SOCK_STREAM)  #
#     downloadSocket.connect((server,int(port)))    #
#     print('downloading file')                     #
#     data = b""                                    #
#     while True:                                   #
#         binaryFile = downloadSocket.recv(1024)    #   alternative dwld 
#         data += binaryFile                        #
#         if not binaryFile:                        #
#             break                                 #
#         with open(filename,'wb') as newFile:      #
#             newFile.write(data)                   #
#         downloadSocket.close()                    #


def Dwld(order):
    downloadPort = clientSocket.recv(1024).decode()
    downloadSocket = socket(AF_INET,SOCK_STREAM)
    downloadSocket.connect((server, int(downloadPort)))

    fileName = order[5:]

    with open(fileName,'wb') as downloadFile:
        info = b""
        while True:
            binaryDownload = downloadSocket.recv(1024)
            info += binaryDownload

            if not binaryDownload:
                break
        
        downloadFile.write(info)
        downloadFile.close()
        downloadSocket.close()

        print('file Downloaded\n')

print('\t\tF - T - P\t C\tL\tI\tE\tN\tT\t\t\n')
Help()

while 1:
    order = input('Enter a order: ')
    
    if order == 'help' or order == 'HELP':
        Help()
    elif order == 'list' or order == 'LIST':
        List(order)
    elif order == 'pwd' or order == 'PWD':
        Pwd(order)
    elif order[:2] == 'cd':
        Cd(order)
    elif order[:4] == 'dwld':
        clientSocket.send(order.encode())
        Dwld(order)
    elif order == 'quit' or order == 'QUIT':
        clientSocket.send(order.encode())
        clientSocket.close()
        print('Finish Ordering Client :)')
        break
    else:
        print('Choose correct order ;)')

        