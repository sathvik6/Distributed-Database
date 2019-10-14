import socket 
import dill as pickle 
from threading import Thread
import sys
import threading 
import time 

name=socket.gethostname()
ip=socket.gethostbyname(name)
port=9876
Head_size=10

Entries={}
Social_Numbers=[]
Server_Sockets=[]


server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((ip,port))
server_socket.listen(10)
def Handle_Client(client_socket):
    while True:
        try:
            data=client_socket.recv(Head_size)
            message_length=int(data.strip().decode("utf-8"))
            message=client_socket.recv(message_length)
            obj_actual=pickle.loads(message)
            print(obj_actual)
            flag=False
            if(obj_actual.return_Social_Security() in Entries):
                flag=True
            if(flag):
                message="Entry Already Recorded".encode("utf-8")
            else:
                message="New Entry Recorded".encode("utf-8")
                Entries[obj_actual.return_Social_Security()]=obj_actual
            message_length=f"{len(message):<{Head_size}}".encode("utf-8")
            client_socket.send(message_length+message)
        except Exception as e:
            print(e)
            break

while True:
    try:
         random_socket,address=server_socket.accept()
         data=random_socket.recv(Head_size)
         message_length=int(data.strip().decode("utf-8"))
         message=random_socket.recv(message_length).decode("utf-8")
         
         if(message=="Client_Socket"):
             print("Client_Socket")
             Client_Thread=Thread(target=Handle_Client,args=(random_socket,))
             Client_Thread.start()
         elif(message=="Server_Socket"):
             print("Server_Socket")
             pass
         else:
             print("Invalid Response")
    except Exception as e:
        print(e)
        break