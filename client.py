import socket
from threading import Thread
from tkinter import *

#nick = input("Enter your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))
print("Connected with the server...")

class GUI:
  def __init__(self):
    self.Window = Tk()
    self.Window.withdraw()

    self.login = Toplevel()
    self.login.title("Login")
    self.login.resizable(width = False, height = False)
    self.login.configure(width = 400, height = 300)
    self.pls = Label(
      self.login,
      text = "Please login to continue",
      justify = CENTER,
      font = "Helvetica 14 bold"
    )
    self.pls.place(relheight= 0.15, 
    relx = 0.2, 
    rely = 0.07)

    self.labelName = Label(
      self.login,
      text = "Name",
      font = "Helvetica 14"
    )
    self.labelName.place(
      relheight= 0.2,
      relx = 0.1,
      rely = 0.2
    )

    self.entryName = Entry(
      self.login, 
      font = "Helvetica 14"
    )
    self.entryName.place(
      relheight = 0.12,
      relwidth = 0.4, 
      relx = 0.35, 
      rely = 0.25 
    )
    self.entryName.focus()
    self.login_btn = Button(
      self.login,
      text = "Login",
      font = "Helvetica 14",
      command = lambda: self.goAhead(self.entryName.get())
    )
    ''' Since the command argument contains () with the argument of the name
        inside it, it will get called by default when the program is run.
        To avoid this, we use lambda, which is a one-line function.
    '''      
    
    self.login_btn.place(
      relx = 0.4,
      rely = 0.5
    )
    
    self.Window.mainloop()
    
  def goAhead(self, name):
    self.login.destroy()
    self.name = name
    rcv = Thread(target = self.receive)
    rcv.start()
    self.layout()
  
  def layout(self):
    self.Window.deiconify()
  
  def receive(self):
    while True:
      try:
        message = client.recv(2048).decode('utf-8')
        if message == 'NICKNAME':
          client.send(self.name.encode('utf-8'))
        else:
          pass
      except:
        print("An error occurred!")
        client.close()
        break

g = GUI()

'''
def write():
  while True:
    message = '<{}>: {}'.format(nick, input(''))
    client.send(message.encode('utf-8'))
write_thread = Thread(target = write)
write_thread.start()
'''
