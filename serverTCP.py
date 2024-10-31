import io
import socket
from imgen import im_generation

IMG='imageAUAU.jpeg'
TOP='Eis que você precisa fazer'
BOTTOM='um trabalho de redes'

formato='JPEG'

#Na versão do Pillow-10.2.0 o ImageFont não possui mais
#o atributo getsize, usando Pillow-9.5.0 para funcionar
def convert_to_byte_arr(image, format):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()


HOST = ''        
PORT = 50007 
             
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        print("Aguardando conexão de um cliente")
        conn, addr = s.accept()
        with conn:
            print('Conectado em ', addr)
            while True:
                data = conn.recv(3600000)
                if data:
                    partes = data.decode('utf-8').replace("IMACRO ", "").split("\n")
                    IMG=partes[0]
                    TOP=partes[1]
                    BOTTOM=partes[2]
                    img = im_generation.generate_image_macro(IMG, TOP,BOTTOM )
                    formato=IMG.split(".") #determina a extensão do arquivo
                    macroByte=convert_to_byte_arr(img,formato[-1].upper())
                if not data:
                    print("Encerrando conexão")
                    break
                conn.sendall(macroByte)
