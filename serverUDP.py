import socket
import io
from imgen import im_generation

IMG='imageAUAU.jpeg'
TOP='Eis que você precisa fazer'
BOTTOM='um trabalho de redes'
SEG_SIZE=32768
formato='JPEG'

def convert_to_byte_arr(image, format):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()

UDP_IP = ''
UDP_PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        print("Servidor a escuta")
        data, addr = sock.recvfrom(SEG_SIZE+2)
        if "IMACRO" in data.decode('utf-8'):
            print("Servidor recebeu 1 pacote do cliente:   ",addr)
            partes = data.decode('utf-8').replace("IMACRO ", "").split("\n")
            IMG=partes[0]
            TOP=partes[1]
            BOTTOM=partes[2]
            img = im_generation.generate_image_macro(IMG, TOP,BOTTOM )
            formato=IMG.split(".") #para determinar a extensão do arquivo
            macroByte=convert_to_byte_arr(img,formato[-1].upper())
            seg_count=((len(macroByte)+SEG_SIZE-1)//SEG_SIZE)
            seg_count_bytes = seg_count.to_bytes(2, byteorder='big')
            print("O total de pacotes: ",int.from_bytes(seg_count_bytes, 'big'))
            sent = sock.sendto(seg_count_bytes, addr)

            macroByte=[macroByte[i:i+SEG_SIZE] for i in range(0, len(macroByte), SEG_SIZE)]
            
            for i in range(len(macroByte)):
                sock.sendto(i.to_bytes(2, byteorder='big')+macroByte[i], addr)
                print(" Servidor enviou o pacote "+str(i+1)+"para o cliente:   ",addr)
            print("acabou a transferencia")
            #sock.sendto(b'EOF', addr)
        else:
            print("Servidor recebeu 1 pacote Do cliente:   ",addr)