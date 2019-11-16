import socket
import dill as pickle
import sys

name=socket.gethostname()
ip= socket.gethostbyname(name)
port=9876
HEADER_LENGTH=10
WORKER_INDEN="Server_Socket".encode("utf-8")
worker_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
worker_socket.connect((ip,port))

worker_length=f"{len(WORKER_INDEN):<{HEADER_LENGTH}}".encode("utf-8")
worker_socket.send(worker_length+WORKER_INDEN)
Entries={}

while True:
    try:
        print("Not Received")
        message_length=int(worker_socket.recv(HEADER_LENGTH).strip().decode("utf-8"))
        message=worker_socket.recv(message_length).decode("utf-8")
        if(message=="ADD"):
            message_length=int(worker_socket.recv(HEADER_LENGTH).strip().decode("utf-8"))
            message=worker_socket.recv(message_length)
            
            message=pickle.loads(message)
            print("Here",type(message))
            Entries[message.return_Social_Security]=message
            print("Here1")
            message="Data added Successfully".encode("utf-8")
            message_length=f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
            worker_socket.send(message_length+message)
            pass
        elif(message=="RETRE"):
            print(message)
            messagex=pickle.dumps(Entries)
            messagex_length=f"{len(messagex):<{HEADER_LENGTH}}".encode("utf-8")
            worker_socket.send(messagex_length+messagex)
            pass
        else:
            print(message)
            pass
    except Exception as e:
        print("Server must have ended the connection")
        print(e)
        worker_socket.close()
        sys.exit()