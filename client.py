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
    rcv = Thread(target = self.receive)
    rcv.start()
    self.name = name
    self.layout(name)
  
  def layout(self, name):
    self.Window.deiconify()
    self.Window.title("CHATROOM")
    self.Window.resizable(width = False, height = False)
    self.Window.configure(
      width = 450, 
      height = 550, 
      bg = "#17202A"
    )
    
    self.labelHead = Label(
      self.Window,
      bg = "#17202A",
      fg = "#EAECEE",
      text = self.name, 
      font = "Helvetica 15 bold",
      pady = 5
    )
    self.labelHead.place(relwidth = 1)
    
    self.line = Label(
      self.Window, 
      width = 430,
      bg = "#ABB2B9"
    )
    self.line.place(
      relwidth = 1,
      relheight= 0.01,
      rely = 0.06
    )

    self.textCons = Text(
      self.Window, 
      width = 20, 
      height = 2,
      bg = "#17202A",
      fg = "#ABB2B9", 
      font = "Helvetica 14",
      padx = 5, 
      pady = 5
    )

    self.textCons.place(
      relheight = 0.7, 
      relwidth= 0.9, 
      rely = 0.1
    )
    
    self.textCons.config(cursor="arrow")
    scrollBar = Scrollbar(self.textCons)
    scrollBar.place(relheight = 1, relx = 0.95)
    scrollBar.config (
      command = self.textCons.yview
    )
    
    self.labelBottom = Label(
      self.Window,
      height = 80,
      bg = "#17202A",
      fg = "#ABB2B9"
    )
    
    self.labelBottom.place(
      relwidth=1,
      rely=0.8
    )
    
    self.entryMsg = Entry(
      self.labelBottom,
      bg = "#17202A",
      fg = "#ABB2B9",
      font = "Helvetica 13"
    )
    self.entryMsg.place(
      relwidth = 0.75,
      relheight = 0.05,
      rely=0.01,
      relx=0.01
    )
    self.entryMsg.focus()
    
    self.btnMsg = Button(
      self.labelBottom,
      text = "Send",
      font = "Helvetica 10 bold",
      width = 20,
      bg = "#17202A",
      fg = "#ABB2B9",
      command = lambda: self.sendBtn(self.entryMsg.get())
    )
    self.btnMsg.place(
      relwidth = 0.2,
      relheight = 0.04,
      relx = 0.78,
      rely = 0.01
    )

  def sendBtn(self, msg):
    self.textCons.config(state = DISABLED)
    self.msg = msg
    self.entryMsg.delete(0, END)
    snd = Thread(target=self.write)
    snd.start()

  def showMsg(self, msg):
    self.textCons.config(state = NORMAL)
    self.textCons.insert(END, msg+"\n\n")
    self.textCons.config(state = DISABLED)
    self.textCons.see(END)
    
  def receive(self):
    while True:
      #try:
      message = client.recv(2048).decode('utf-8')
      if message == 'NICKNAME':
        print(self.name)
        client.send(self.name.encode('utf-8'))
      else:
        self.showMsg(message)
      """ except:
        print("An error occurred!")
        client.close()
        break """

  def write(self):
    self.textCons.config(state = DISABLED)
    while True:
      msg = (f"{self.name}: {self.msg}")
      client.send(msg.encode("utf-8"))
      self.showMsg(msg)
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
