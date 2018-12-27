import socket
import sys
from _thread import *
import errno
import threading
import datetime
from tkinter import *
from tkinter import messagebox
import select
 
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(10)
server_start = 0

clients = set()
clientsNames = set()
clients_lock = threading.Lock()

def listener(client, address):
    with clients_lock:
        clients.add(client)
    try:
        client.send('Добро пожаловать в чат NewLine\n'.encode('utf8'))
        name = client.recv(1024).decode("utf-8")
        with clients_lock:
            clientsNames.add(name)
        for c in clients:
            data = str(datetime.datetime.now().strftime('%H:%M:%S')) + " Присоединился клиент: " + name + "\n\n" + "Активные пользователи:" + "\n"
            c.sendall(data.encode('utf8'))
            data = ""
            for cl in clientsNames:
                data += cl + "\n"
            c.sendall(data.encode('utf8'))    
            data = "\n"
            c.sendall(data.encode('utf8'))
            
        print('Активные пользователи:')
        for c in clientsNames:
            print(c)


        client.setblocking(0)
        
        while True:
            ready = select.select([client], [], [], 1.0)
            if ready[0]:
                data = client.recv(1024).decode("utf-8")
                if not data:
                    break
                else:
                    data = str(datetime.datetime.now().strftime('%H:%M:%S')) + " " + name + " : " + data    
                    print (repr(data))
                    with clients_lock:
                        for c in clients:
                            c.sendall(data.encode('utf8'))
                       
            testExists = 0
            with clients_lock:
                for c in clientsNames:
                    if c == name:
                        testExists = 1
            if testExists == 0:
                with clients_lock:
                    for c in clients:
                        data = "\n" + str(datetime.datetime.now().strftime('%H:%M:%S')) + " Заблокирован клиент: " + name + "\n\n" + "Активные пользователи:" + "\n"
                        c.sendall(data.encode('utf8'))
                        data = ""
                        for cl in clientsNames:
                            data += cl + "\n"
                        c.sendall(data.encode('utf8'))
                        data = "\n"
                        c.sendall(data.encode('utf8'))
                    data = "/exit/"
                    client.sendall(data.encode('utf8'))
                    clients.remove(client)
                    
                    print('Активные пользователи:')
                    for c in clientsNames:
                        print(c)
                    client.close()
                    return
                
                    
                        
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET or error.errno == errno.WSAECONNABORTED :
            print('Отключился : ' + name)
            with clients_lock:
                clients.remove(client)
                clientsNames.remove(name)
                for c in clients:
                    data = str(datetime.datetime.now().strftime('%H:%M:%S')) + " Отключился клиент: " + name + "\n\n" + "Активные пользователи:" + "\n"
                    c.sendall(data.encode('utf8'))
                    data = ""
                    for cl in clientsNames:
                        data += cl + "\n"
                    c.sendall(data.encode('utf8'))
                    data = "\n"
                    c.sendall(data.encode('utf8'))
                    
                print('Активные пользователи:')
                for c in clientsNames:
                    print(c)
                client.close()

def newConnect():
    while True:
        conn, addr = sock.accept()
        print ('Присоеденился ' + str(addr))
        start_new_thread(listener,  (conn, addr,))

def startServer():
    global server_start
    server_start = 1
    start_new_thread(newConnect,  ())

def deleteClient():
    global text
    t = text.get("1.0",END)
    if server_start == 1 and t != "\n":
        with clients_lock:
            t = t.replace('\r','').replace('\n','')
            testExists = 0
            for c in clientsNames:
                if c == t:
                    testExists = 1
            if testExists == 1:             
                clientsNames.remove(t)
        text.delete('1.0', END)
    

root = Tk()
root.title("Сервер чата NewLine")
root.geometry("500x100")

#Кнопка старта сервера
register_button = Button(text="Старт сервера", command=startServer)
register_button.place(relx=.1, rely=.1, anchor="c")

#Отключить клиента
text = Text( width=20, height=1,background='#999999')
text.place(relx=.2, rely=.8,  anchor="c")
message_button = Button(text="Удалить", command=deleteClient)
message_button.place(relx=.5, rely=.8, anchor="c")

root.mainloop()

sock.close()
