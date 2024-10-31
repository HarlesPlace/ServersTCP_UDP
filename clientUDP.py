import socket
from PIL import Image
import io


print("Personalize sua Image Macro conosco!!!")

IMG=input("Qual o endereço da imagem? ")
TOP=input("Digite a frase de cima do seu macro: ")
BOTTOM=input("Digite a frase de baixo do seu macro: ")
SEG_SIZE=32768
personalizado= "IMACRO " +IMG+ "\n"+TOP+"\n"+BOTTOM
print(personalizado)

HOST = '127.0.0.1'
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(2)
    sock.sendto(personalizado.encode('utf-8'), (HOST, PORT))
    print('Cliente enviou:   ', personalizado.encode('utf-8'), "  para o servidor:   ",(HOST, PORT))
    data, addr = sock.recvfrom(2)
    seg_count = int.from_bytes(data, 'big')
    print("Cliente recebeu 1 pacote  do servidor:   ",addr," dizendo a quantidade de pacotes= ", seg_count)
    imacroRebuild=bytearray(SEG_SIZE*seg_count)
    while True:
        try:
            data, addr = sock.recvfrom(SEG_SIZE+2)
            id=int.from_bytes(data[:2],"big")
            print("Cliente recebeu o pacote numero "+str(id+1)+" do servidor:   ",addr)
            print("Conteúdo: "+str(data[:12]))
            imacroRebuild[id*SEG_SIZE:len(data)-2]=data[2:]
            if id+1==seg_count:#corrige tamanho do arquivo
                imacroRebuild=imacroRebuild[:(seg_count-1)*SEG_SIZE+len(data)-2]
                break
        except TimeoutError:
            print("Tempo limite de resposta do servidor")
            break
         
try:
    image=Image.open(io.BytesIO(imacroRebuild))
    print("Abrindo macro, aguarde....")
    image.show()
except:
    print("Opsss, alguns pacotes foram perdidos")

print("Encerrando cliente")
sock.close()