 
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition,WipeTransition, SlideTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics.texture import Texture
from kivy.graphics import *
import time
import os
import threading
import time
from datetime import datetime
import socket
from requests import get

remoteName = ""
remoteIP = ""

remote_cond = False
remote_listen = True

hostname = socket.gethostname()

# Obtém o endereço IP associado ao nome do host
ip = socket.gethostbyname(hostname)
 
listen_msg = ""
remote_msg = ""
remote_port = 2006
listen_cond = False

def sender():
    global remote_msg, remoteIP, remote_port, remote_cond
    while True:
        try:
            while remote_cond == True:
                
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print(remoteIP)
                remote_socket.connect((remoteIP, remote_port))
                print("conect")
                while True:
                    if(remote_msg != ""):
                        remote_socket.send(bytes(remote_msg,'utf-8'))
                        remote_msg = ""
                        
                        
        except:
            time.sleep(0.5)
            
thread_1 = threading.Thread(target = sender)

def listen(): 
    
    global listen_msg, listen_cond
    
    while listen_cond == True:
        
        try:
            listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            listen_socket.bind(ip,2006)
            listen_socket.listen(10)
            print("binded")
            while True:
                clientsocket, address = listen_socket.accept()
                while True:
                    chat_recv = clientsocket.recv(1024)
                    listen_msg = chat_recv.decode("utf-8")
        except:
            time.sleep(0.5)
            print("binding...")


thread_2 = threading.Thread(target = listen)


def sendMessage():
    servidor_ip = '192.168.100.8'  # Substitua pelo IP do servidor
    servidor_porta = 12345  # Use a mesma porta que o servidor

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((servidor_ip, servidor_porta))
 
    mensagem = 'DAAAAAALE GURI, FUNCIONOU'
    cliente.send(mensagem.encode('utf-8'))  # Envie a mensagem para o servidor

class MenuScreen(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        
    def initiate(self):
        global remoteName, remoteIP,remote_cond
        remoteName =  self.ids.name_id.text 
        remoteIP =  self.ids.ip_id.text 
        chatapp.ChatManager.ids.head_id.text = f"Conectado no IP: {remoteIP}"
        remote_cond = True
        chatapp.sm.current = 'ChatManager'
        Clock.schedule_interval(chatapp.ChatManager.update_recieved, 0.5)

     
class ChatManager(Widget):
    def __init__(self, **kw):
       super().__init__(**kw)
    
    def teste(self):
        global remoteIP,remoteName
  
        
    def send_msg(self):
        global remote_msg
        self.ids.chat_text_id.text = self.ids.chat_text_id.text + '\n' + chatapp.MenuScreen.ids.name_id.text +' : ' +  self.ids.msg_id.text 
        remote_msg = chatapp.MenuScreen.ids.name_id.text + ': ' + self.ids.msg_id.text
        print(remote_msg)


    def update_recieved(self, *args):
        global listen_msg
        if listen_msg != '':
            self.ids.chat_text_id.text = self.ids.chat_text_id.text + '\n' + '[color=#3477eb]' + listen_msg + '[/color]'
            listen_msg = ''

class ChatApp(App):
    def build(self):
        
        self.sm = ScreenManager()
        self.sm = ScreenManager(transition=SlideTransition(direction="down"))
         
        self.MenuScreen = MenuScreen()
        screen = Screen(name="MenuScreen")
        screen.add_widget(self.MenuScreen)
        self.sm.add_widget(screen)
        
        self.ChatManager = ChatManager()
        screen = Screen(name="ChatManager")
        screen.add_widget(self.ChatManager)
        self.sm.add_widget(screen)
    
        return self.sm
if __name__ == '__main__':
    # sendMessage()
    chatapp = ChatApp()		
    thread_1.start()
    thread_2.start()
    threading.Thread(target = chatapp.run())
    remote_cond = False
    listen_cond = False