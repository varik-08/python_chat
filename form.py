from tkinter import *
from tkinter import messagebox
import socket
import threading
from _thread import *
import errno
import sys

def login():
    global regStatus
    if regStatus == 0:
        sock.connect(('localhost', 9090))
        nameEmployee = name.get()
        sock.send(nameEmployee.encode('utf8'))
        regStatus = 1

def logout():
    global sock
    global regStatus
    global root
    if regStatus == 1:
        regStatus = 0
        sock.close()
    root.destroy()
    sys.exit()
    
def send_message():
    if regStatus == 1:
        global text
        t = text.get("1.0",END)
        if t != "\n":
            sock.send(t.encode('utf8'))
            text.delete('1.0', END)
        
def writeMessage():
    while True:
        global textChat
        global sock

        try:
            if regStatus == 1:
                data = sock.recv(1024).decode("utf-8")
                if not data:
                    break
                else:
                    if "/exit/" in data:
                        messagebox.showinfo("Бан", "Вас исключили из чата!")
                        logout()
                    textChat.insert(END, data)
        except socket.error as error:
             if error.errno == errno.WSAECONNRESET or error.errno == errno.WSAECONNABORTED :
                 textChat.insert(END, 'Ждем вас снова!')
                        
root = Tk()
root.title("Чат NewLine")
root.geometry("500x500")

regStatus=0
message = StringVar()
name = StringVar()
sock = socket.socket()

#Регистрация
name_label = Label(text="Введите имя:")
name_label.grid(row=0, column=0, sticky="w")
name_entry = Entry(textvariable=name)
name_entry.place(relx=.2, rely=.1, anchor="c")
register_button = Button(text="Войти", command=login)
register_button.place(relx=.5, rely=.1, anchor="c")

#Выйти
register_button = Button(text="Выйти", command=logout)
register_button.place(relx=.7, rely=.1, anchor="c")

#Сообщения с чата
textChat = Text( width = 50, height=12,background='#999232')
textChat.place(relx=.4, rely=.4,  anchor="c")

#Отправка сообщения
text = Text( width=20, height=7,background='#999999')
text.place(relx=.2, rely=.8,  anchor="c") 

message_button = Button(text="Отправить", command=send_message)
message_button.place(relx=.5, rely=.8, anchor="c")

start_new_thread(writeMessage ,()) 
root.mainloop()
