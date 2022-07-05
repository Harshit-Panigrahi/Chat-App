import socket
from threading import Thread

''' SOCK_DGRAM : used to create UDP Sockets
    SOCK_STREAM: used to create TCP sockets
    
    TCP: Transimission Control Protocol
        Tries to resend the packets that were lost during transmission. 
        Adds a sequence number to each packet and reorders them at receiver's end so that the packets do not arrive in wrong order.
        Execution is slower. 
        Examples: HTTP, HTTPS, SMTP, FTP, etc.

    UDP: User Datagram Protocol 
        Doesn't resend the packets that were lost.
        Packets can arrive in any order.
        Faster in execution.
        Examples: DNS, DHCP, etc.  
'''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000
clients = []

server.bind((ip_address, port))
server.listen()

print("Server is running...")

def clientthread(conn, addr):
  conn.send("Welcome to the chatroom".encode('utf-8'))
  while True: 
    try:
      message = conn.recv(2048).decode('utf-8')
      if message:
        message_to_Send = "<" + addr[0] + "> " + message
        print(message_to_Send)
        broadcast(message_to_Send, conn)
      else:
        remove(conn)
    except:
      continue

# Connection is the socket that wants to send the message

def broadcast(msg, connection):
  for client in clients:
    if client != connection:
      try:
        client.send(msg.encode("utf-8"))
      except:
        remove(client)

def remove(connection):
  if connection in clients: 
    clients.remove(connection)

while True:
  conn, addr = server.accept()
  clients.append(conn)
  print(addr[0] + "connected")

  new_thread = Thread(target= clientthread, args=(conn, addr))
  new_thread.start()