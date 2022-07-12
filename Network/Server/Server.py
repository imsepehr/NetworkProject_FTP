from socket import *
import random
import os

server = '127.0.0.1'
port = 2121 

current_directory = os.getcwd()

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((server, port))
serverSocket.listen()
connection ,address = serverSocket.accept()

def border_msg(msg):
    row = len(msg)
    h = ''.join(['+'] + ['-' *row] + ['+'])
    result= h + '\n'"|"+msg+"|"'\n' + h
    print(result)

print('--------------- Server ready to service ---------------')

def List():
    files = os.listdir()
    sum = 0
    response = ''
    for thing in files:
        sum += os.path.getsize(thing)
        if os.path.isfile(thing):
            response += thing + '\t -----------------\t\t' + str(os.path.getsize(thing)) + ' Bytes\n'
        elif os.path.isdir(thing):
            response += '[]\t' + thing + '\t -----------------\t\t' + str(os.path.getsize(thing)) + ' Bytes\n'
    response += 'SUM of total SIZE : ' + str(sum) + ' Bytes' 
    connection.send(str(response).encode())
    print('List Req')

def Pwd():
    response = os.getcwd()
    if not response:
        response = '/'
    connection.send(str(response).encode())
    print('PWD Req')

def Cd(directory):
    print('CD Req')
    try:
        current = os.getcwd()
        os.chdir(directory)
        if current_directory == os.getcwd()[:len(current_directory)]:
            response = 'directory changed.'
            connection.send(str(response).encode())
        else:
            os.chdir(current)
            print('access to bad path!')
            response = 'you cant access this directory!'
            connection.send(str(response).encode())
    except:
        response = 'Bad Request!'
        print(response)
        connection.send(str(response).encode())


def Dwld(order):
    print('DWLD Req')
    files = os.listdir()
    fileName = order[5:]

    if fileName in files:
        randPort = random.randint(3000,50000)
        dwldSocket = socket(AF_INET,SOCK_STREAM)
        dwldSocket.bind((server,randPort))
        dwldSocket.listen()
        connection.send(str(randPort).encode())
        dwldConnection , dwldAddress = dwldSocket.accept()
        with open(fileName,'rb') as f:
            dwldConnection.send(f.read())
            f.close()
            dwldSocket.close()
    else:
        response = 'Bad Request!'
        connection.send(str(response).encode())
        print(response)

while True:
    border_msg('SERVER is listening....')
    
    order = connection.recv(1024).decode()

    if order == 'help' or order == 'HELP':
        pass
    elif order == 'list' or order == 'LIST':
        List()
    elif order == 'pwd' or order == 'PWD':
        Pwd()
    elif order[:2] == 'cd' or order[:2] == 'CD':
        Cd(order[3:])
    elif order == 'dwld' or order == 'DWLD':
        Dwld(connection,order[5:])
    elif order == 'quit' or order == 'QUIT':
        connection.close()
        print('Finish servicing server :)')
        break

    
