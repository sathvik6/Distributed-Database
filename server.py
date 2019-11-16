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

Entries=[]
Social_Numbers=[]
online_servers=[]
modify_list=threading.Lock()

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((ip,port))
server_socket.listen(10)
def Handle_Client(client_socket):
    while True:
        try:
            data=client_socket.recv(Head_size)
            message_length=int(data.strip().decode("utf-8"))
            message=client_socket.recv(message_length).decode("utf-8")
            if(message=="ADD"):
                data=client_socket.recv(Head_size)
                message_length=int(data.strip().decode("utf-8"))
                messagex=client_socket.recv(message_length)
                obj_actual=pickle.loads(messagex)
                flag=False
                if(obj_actual.return_Social_Security() in Entries):
                    flag=True
                send_subserver=obj_actual
                if(flag):
                    messagex="Entry Already Recorded".encode("utf-8")
                    message_length=f"{len(messagex):<{Head_size}}".encode("utf-8")
                    client_socket.send(message_length+messagex)
                    pass
                else:
                    Entries.append(obj_actual.return_Social_Security())
                    while True:
                        modify_list.acquire()
                        if(len(online_servers)>0):
                            server_socket1=online_servers.pop(0)
                            modify_list.release()
                            break
                        else:
                            pass
                        modify_list.release()
                        time.sleep(0.5)
                    Data_send="ADD".encode("utf-8")
                    Data_sendx_length=f"{len(Data_send):<{Head_size}}".encode("utf-8")
                    server_socket1.send(Data_sendx_length+Data_send)
                    
                    messagex=pickle.dumps(send_subserver)
                    message_length=f"{len(messagex):<{Head_size}}".encode("utf-8")
                    server_socket1.send(message_length+messagex)
                    
                    response_length=int(server_socket1.recv(Head_size).strip().decode("utf-8"))
                    response=server_socket1.recv(response_length).decode("utf-8")
                    
                    response=response.encode("utf-8")
                    response_length=f"{len(response):<{Head_size}}".encode("utf-8")
                    client_socket.send(response_length+response)
                    modify_list.acquire()
                    online_servers.append(server_socket1)
                    modify_list.release()

            elif(message=="RETRE"):
                modify_list.acquire()
                datax=[]
                for i in online_servers:
                    Data_send="RETRE".encode("utf-8")
                    Data_sendx_length=f"{len(Data_send):<{Head_size}}".encode("utf-8")
                    i.send(Data_sendx_length+Data_send)
                    
                    data=i.recv(Head_size)
                    message_length=int(data.strip().decode("utf-8"))
                    message=i.recv(message_length)
                    message=pickle.loads(message)
                    datax.append(message)
                    
                modify_list.release()
                print("HEre")
                message=pickle.dumps(datax)
                message_length=f"{len(message):<{Head_size}}".encode("utf-8")
                client_socket.send(message_length+message)
            else:
                print("Invalid Response")
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
             online_servers.append(random_socket)
         else:
             print("Invalid Response")
    except Exception as e:
        print(e)
        break
