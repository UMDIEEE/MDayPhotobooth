import socket
import time

server_address = ('10.104.232.214', 12345)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

try:
    # Send data
    while 1:
        message = input("> ")
        print("<< %s" % message)
        sock.sendall(message.encode("utf-8"))
finally:
    print("Closing")
    sock.close()
