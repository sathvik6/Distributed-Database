import socket
import pickle
import time
import sys

class Data:
    def __init__(self,Name,Email,PhoneNumber,Social_Security):
        self.Name=Name
        self.Email=Email
        self.PhoneNumber=PhoneNumber
        self.Social_Security=Social_Security
name=socket.gethostname()
ip=socket.gethostbyname(name)
port=9876
Head_size=10
try:
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((ip,port))
    message="Client_Socket".encode("utf-8")
    message_length=f"{len(message):<{Head_size}}".encode("utf-8")
    client_socket.send(message_length+message)
except Exception as e:
    print(e)
    print("Unable to Connect to the Server")
    sys.exit()

while True:
    try:
        Name=input("Enter Name :")
        Email=input("Enter Email Id :")
        PhoneNumber=int(input("Enter Phone Number :"))
        Social_Security=int(input("Enter Social Security Number :"))
        Data_send=Data(Name,Email,PhoneNumber,Social_Security)
        Data_sendx=pickle.dumps(Data_send)
        Data_sendx_length=f"{len(Data_sendx):<{Head_size}}".encode("utf-8")
        client_socket.send(Data_sendx_length+Data_sendx)
        
        response_length=int(client_socket.recv(Head_size).strip().decode("utf-8"))
        response=client_socket.recv(response_length).decode("utf-8")
        print(response)
    except Exception as e:
        print("Some Error in Server Connection")
        continue 
