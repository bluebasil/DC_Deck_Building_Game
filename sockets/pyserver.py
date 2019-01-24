import socket

HOST = "localhost"
PORT = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as err:
    print('Bind failed. Error Code : ' .format(err))
s.listen(10)
print("Socket Listening")
conn, addr = s.accept()
while(True):
    conn.send(bytes("Message"+"\r\n",'UTF-8'))
    print("Message sent")
    data = conn.recv(1024)
    print(data.decode(encoding='UTF-8'))
