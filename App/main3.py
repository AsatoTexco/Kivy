 
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

remote_cond = False
remote_listen = True

remote_ip = ""
remote_port = 0

listen_msg = ""
remote_msg = ""


def sender():
    global remote_msg, remote_ip, remote_port, remote_cond
    while True:
        try:
            while remote_cond == True:
                
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect((remote_ip, remote_port))
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
            listen_socket.bind("192.168.100.8",2006)
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

class initialpage(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        
    def initiate(self):
        global remote_ip, remote_port, remote_cond
        remote_ip = self.ids.ip_id.text
        remote_port = int(self.ids.port_id.text)
        remote_cond = True
        theapp.mainscreen.ids.head_id.text = 'Chat aberto com IP: ' + self.ids.ip_id.text + ' na Porta: ' + self.ids.port_id.text
        theapp.screenm.current = 'mainscreen'
        Clock.schedule_interval(theapp.mainscreen.update_recieved, 0.5)
  
  
class mainscreen(Widget):
    def __init__(self, **kwargs):
         super().__init__(**kwargs)

    def send_msg(self):
        global remote_msg
        self.ids.chat_text_id.text = self.ids.chat_text_id.text + '\n' + theapp.initialpage.ids.user_id.text +' : ' +  self.ids.msg_id.text 
        remote_msg = theapp.initialpage.ids.user_id.text + ": " + self.ids.msg_id.text 
         
    def update_recieved(self, *args):
        global listen_msg
        if listen_msg != '':
            self.ids.chat_text_id.text = self.ids.chat_text_id.text + '\n' + '[color=#3477eb]' + listen_msg + '[/color]'
            listen_msg = ''
   
class theapp(App):
    
    def build(self):
        self.screenm = ScreenManager(transition=SlideTransition(direction='up'))
        self.initialpage = initialpage()
        screen = Screen(name="initialpage")
        screen.add_widget(self.initialpage)
        self.screenm.add_widget(screen)
        
        self.mainscreen = mainscreen()
        screen = Screen(name="mainscreen")
        screen.add_widget(self.mainscreen)
        self.screenm.add_widget(screen)
        
        return self.screenm
if __name__ == "__main__":
    theapp = theapp()		
    thread_1.start()
    thread_2.start()
    thread.Thread(target = theapp.run())
    remote_cond = False
    listen_cond = False