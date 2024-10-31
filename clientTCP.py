import socket
from PIL import Image
import io

print("Personalize sua Image Macro conosco!!!")

IMG=input("Qual o endereço da imagem? ")
TOP=input("Digite a frase de cima do seu macro: ")
BOTTOM=input("Digite a frase de baixo do seu macro: ")

personalizado= "IMACRO " +IMG+ "\n"+TOP+"\n"+BOTTOM
print(personalizado)

HOST = '127.0.0.1'    
PORT = 50007      

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(personalizado.encode('utf-8'))
    data = s.recv(3600000)
    
    #print(data)
#print('Received', repr(data))

image=Image.open(io.BytesIO(data))
print("Abrindo macro, aguarde....")
image.show()
print("Encerrando cliente")
s.close()