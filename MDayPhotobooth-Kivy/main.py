from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput

from email.utils import parseaddr
import time
import threading
import socket

try:
    # Python 3.x
    from queue import Queue
except ImportError:
    # Python 2.x
    from Queue import Queue

import traceback

DEBUG = False

global TARGET_ADDR, TARGET_PORT
TARGET_ADDR = '10.104.232.214'
TARGET_PORT = 12345

def send_socket(msg, queue = None):
    try:
        server_address = (TARGET_ADDR, TARGET_PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(server_address)

        try:
            # Send data
            print("[SOCK] << %s" % msg)
            sock.sendall(msg.encode("utf-8"))
            
            if queue:
                queue.put(True)
        finally:
            print("[SOCK] Closing")
            sock.close()
    except:
        print("[SOCK] Failed to connect!")
        traceback.print_exc()
        
        if queue:
            queue.put(False)

def send_socket_async(msg):
    q = Queue()
    t = threading.Thread(target=send_socket, args=(msg,q))
    t.start()
    t._kivy_queue = q
    return t

def get_send_socket_ret(t):
    return t._kivy_queue.get()

def show_error():
    if DEBUG:
        debug_str = "\r\n\r\nServer: %s:%d" % (TARGET_ADDR, TARGET_PORT)
    else:
        debug_str = ""
    Popup(title = 'Error occurred!', content=Label(text = 'Could not send command!%s' % debug_str), auto_dismiss=True, size_hint = (.3,.3)).open()

Builder.load_string('''
#:import random random.random
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import SwapTransition kivy.uix.screenmanager.SwapTransition
#:import WipeTransition kivy.uix.screenmanager.WipeTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import RiseInTransition kivy.uix.screenmanager.RiseInTransition
#:import FallOutTransition kivy.uix.screenmanager.FallOutTransition
#:import NoTransition kivy.uix.screenmanager.NoTransition

<BluetoothMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        Label:
            font_size: 42
            text: root.name
        
        Label:
            font_size: 36
            text: 'Please connect your Bluetooth device now.'

<NetworkMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size
    
    Label:
        font_size: 36
        text: 'Target IP:'
        pos_hint: {'x':.27 , 'center_y':.88}
        size_hint: (.45,.07)
    
    TextInput:
        id: ip_text
        font_size: 36
        multiline: False
        pos_hint: {'x':.27 , 'center_y':.77}
        size_hint: (.45,.09)
        text: "(Loading...)"
        disabled: True
    
    Label:
        font_size: 36
        text: 'Target Port:'
        pos_hint: {'x':.27 , 'center_y':.66}
        size_hint: (.45,.07)
    
    TextInput:
        id: port_text
        font_size: 36
        multiline: False
        pos_hint: {'x':.27 , 'center_y':.55}
        size_hint: (.45,.09)
        text: "(Loading...)"
        disabled: True
    
    Button:
        text: 'Confirm'
        id: network_btn
        size_hint: None, None
        pos_hint: {'x':.425 , 'center_y':.15}
        size_hint: (.15,.07)
        on_press: root.on_set_network()
        disabled: True

<StartMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        Label:
            font_size: 36
            text: "Starting up, please wait..."

<filterMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    Label:
        font_size: 36
        text: "Pick a filter!"

    Button:
        text: 'Negative'
        size_hint: None, None
        pos_hint: {'x': .08, 'center_y': .66}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("negative")
        
    Button:
        text: 'Sketch'
        size_hint: None, None
        pos_hint: {'x':.31 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_select_filter("sketch")
       
    Button:
        text: 'Colorswap'
        size_hint: None, None
        pos_hint: {'x':.54 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_select_filter("colorswap")
        
    Button:
        text: 'Cartoon'
        size_hint: None, None
        pos_hint: {'x':.77 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_select_filter("cartoon")
        
    Button:
        text: 'Oilpaint'
        size_hint: None, None
        pos_hint: {'x':.08 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("oilpaint")
        
    Button:
        text: 'Emboss'
        size_hint: None, None
        pos_hint: {'x':.31 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("emboss")
        
    Button:
        text: 'Watercolor'
        size_hint: None, None
        pos_hint: {'x':.54 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("watercolor")
        
    Button:
        text: 'None'
        size_hint: None, None
        pos_hint: {'x':.77 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("none")
    
    Button:
        text: 'Snap'
        size_hint: None, None
        pos_hint: {'x':.425 , 'center_y':.15}
        size_hint: (.15,.07)
        on_press: root.on_take_picture()

<confirmPicMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    Label:
        font_size: 36
        text: "Do you like your picture?"
        
    Button:
        text: 'Yes!'
        size_hint: None, None
        pos_hint: {'x':.275 , 'center_y':.15}
        size_hint: (.15,.07)
        on_press: root.on_confirm()
        
    Button:
        text: 'No - Retake!'
        size_hint: None, None
        pos_hint: {'x':.575 , 'center_y':.15}
        size_hint: (.15,.07)
        on_press: root.on_retake()

<filterMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    Label:
        font_size: 36
        text: "Pick a filter!"

    Button:
        text: 'Negative'
        size_hint: None, None
        pos_hint: {'x': .08, 'center_y': .66}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("negative")
        
    Button:
        text: 'Sketch'
        size_hint: None, None
        pos_hint: {'x':.31 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_select_filter("sketch")
       
    Button:
        text: 'Colorswap'
        size_hint: None, None
        pos_hint: {'x':.54 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_select_filter("colorswap")
        
    Button:
        text: 'Cartoon'
        size_hint: None, None
        pos_hint: {'x':.77 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_select_filter("cartoon")
        
    Button:
        text: 'Oilpaint'
        size_hint: None, None
        pos_hint: {'x':.08 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("oilpaint")
        
    Button:
        text: 'Emboss'
        size_hint: None, None
        pos_hint: {'x':.31 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("emboss")
        
    Button:
        text: 'Watercolor'
        size_hint: None, None
        pos_hint: {'x':.54 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("watercolor")
        
    Button:
        text: 'None'
        size_hint: None, None
        pos_hint: {'x':.77 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_select_filter("none")
    
    Button:
        text: 'Snap'
        size_hint: None, None
        pos_hint: {'x':.425 , 'center_y':.15}
        size_hint: (.15,.07)
        on_press: root.on_take_picture()

<frameMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    Label:
        font_size: 36
        text: "Pick your favorite frame!"

    Button:
        text: '1'
        size_hint: None, None
        pos_hint: {'x': .08, 'center_y': .66}
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(1)
        
    Button:
        text: '2'
        size_hint: None, None
        pos_hint: {'x':.31 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(2)
       
    Button:
        text: '5'
        size_hint: None, None
        pos_hint: {'x':.54 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(5)
        
    Button:
        text: '6'
        size_hint: None, None
        pos_hint: {'x':.77 , 'center_y':.66 }
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(6)
        
    Button:
        text: '3'
        size_hint: None, None
        pos_hint: {'x':.08 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(3)
        
    Button:
        text: '4'
        size_hint: None, None
        pos_hint: {'x':.31 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(4)
        
    Button:
        text: '7'
        size_hint: None, None
        pos_hint: {'x':.54 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(7)
        
    Button:
        text: '8'
        size_hint: None, None
        pos_hint: {'x':.77 , 'center_y':.33}
        size_hint: (.15,.07)
        on_press: root.on_pick_frame(8)
    
    Button:
        text: 'Select'
        size_hint: None, None
        pos_hint: {'x':.425 , 'center_y':.15}
        size_hint: (.15,.07)
        on_press: root.on_select()
        
<emailMenu>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        #Label:
        #    font_size: 42
        #    text: root.name
        
        Label:
            font_size: 36
            text: 'Enter your email below!'
        
        TextInput:
            id: email_text
            multiline: False
        
        Button:
            text: 'Submit'
            on_release: root.on_submit_email()
        
        
<thankYou>:
    hue: random()
    canvas:
        Color:
            hsv: self.hue, .5, .3
        Rectangle:
            size: self.size

    Label:
        font_size: 28
        text: 'Thank you! Please wait while this is being emailed...'

    Button:
        text: 'Reset'
        size_hint: None, None
        pos_hint: {'x':.425 , 'center_y':.15}
        size_hint: (.15,.07)
        on_release: root.manager.current = 'filters'
        
''')

class StartMenu(Screen):
    hue = NumericProperty(0)
    
    def scan_bt(self = None, dt = None):
        self.manager.current = "network"
        #self.manager.current = "bluetooth"
    
    def on_enter(self):
        Clock.schedule_once(self.scan_bt, 1)

class BluetoothMenu(Screen):
    hue = NumericProperty(0)
    counter = 0
    
    def scan_bt(self = None, dt = None):
        print("SCAN")
        if self.counter < 1:
            Clock.schedule_once(self.scan_bt, 1)
        else:
            print(self.manager.screens)
            self.manager.current = "filters"
        self.counter += 1
    
    def on_enter(self):
        print("Hello Bluetooth")
        Clock.schedule_once(self.scan_bt)

class NetworkMenu(Screen):
    hue = NumericProperty(0)
    
    def on_set_network(self):
        global TARGET_ADDR, TARGET_PORT
        ip = self.ids['ip_text'].text
        port = self.ids['port_text'].text
        
        if TARGET_ADDR != ip:
            print("Setting IP: %s" % ip)
            TARGET_ADDR = ip
        
        if str(TARGET_PORT) != port:
            print("Setting port: %s" % port)
            TARGET_PORT = int(port)
        
        self.manager.current = "filters"
    
    def on_enter(self):
        print("Hello Network")
        self.ids['ip_text'].text = TARGET_ADDR
        self.ids['port_text'].text = str(TARGET_PORT)
        
        self.ids['ip_text'].disabled = False
        self.ids['port_text'].disabled = False
        self.ids['network_btn'].disabled = False
        
        #Clock.schedule_once(self.scan_bt)

class filterMenu(Screen):
    hue = NumericProperty(0)
    popup = None
    lbl = None
    
    sel_filter = None
    sel_filter_thread = None
    
    takepic_thread = None
    
    cheese_ctr = 3
    
    def send_filter_cmd(self, dt):
        if not self.sel_filter_thread:
            self.sel_filter_thread = send_socket_async("filter,%s" % self.sel_filter)
            Clock.schedule_once(self.send_filter_cmd, 1)
        else:
            if self.sel_filter_thread.is_alive():
                Clock.schedule_once(self.send_filter_cmd, 1)
            else:
                if not get_send_socket_ret(self.sel_filter_thread):
                    show_error()
                self.sel_filter_thread = None
                self.sel_filter = None
                self.popup.dismiss()
    
    def send_takepic_cmd(self, dt):
        if self.cheese_ctr > 0:
            self.cheese_ctr -= 1
            self.lbl.text = "%d" % self.cheese_ctr
            Clock.schedule_once(self.send_takepic_cmd, 1)
        else:
            if not self.takepic_thread:
                self.takepic_thread = send_socket_async("takepic,")
                Clock.schedule_once(self.send_takepic_cmd, 1)
            else:
                if self.takepic_thread.is_alive():
                    Clock.schedule_once(self.send_takepic_cmd, 1)
                else:
                    if not get_send_socket_ret(self.takepic_thread):
                        show_error()
                    self.takepic_thread = None
                    self.popup.dismiss()
                    self.manager.transition = SlideTransition(direction="left")
                    self.manager.current = 'confirmpic'
    
    def on_select_filter(self, filter):
        print("Selected filter: %s" % filter)
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = 'Selecting filter: %s' % filter)
        pb = ProgressBar(max = 1)
        layout.add_widget(lbl)
        layout.add_widget(pb)
        self.popup = Popup(title = 'Selecting Filter...', content=layout, auto_dismiss=False, size_hint = (.3,.3))
        self.popup.open()
        
        self.sel_filter = filter
        Clock.schedule_once(self.send_filter_cmd, 1)
    
    def on_take_picture(self):
        print("Taking picture!")
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = 'Say cheese!')
        self.lbl = Label(text = '3', font_size = 24)
        pb = ProgressBar(max = 3)
        layout.add_widget(lbl)
        layout.add_widget(self.lbl)
        layout.add_widget(pb)
        self.popup = Popup(title = 'Taking Picture!', content=layout, auto_dismiss=False, size_hint = (.3,.3))
        self.popup.open()
        
        self.cheese_ctr = 3
        
        Clock.schedule_once(self.send_takepic_cmd, 1)

class confirmPicMenu(Screen):
    hue = NumericProperty(0)
    popup = None
    
    confirm_thread = None
    retake_thread = None
    
    def delay_frame_screen(self, dt):
        self.confirm_thread = None
        self.popup.dismiss()
        self.manager.current = 'frames'
    
    def send_confirm_cmd(self, dt):
        if not self.confirm_thread:
            self.confirm_thread = send_socket_async("accept,")
            Clock.schedule_once(self.send_confirm_cmd, 1)
        else:
            if self.confirm_thread.is_alive():
                Clock.schedule_once(self.send_confirm_cmd, 1)
            else:
                if not get_send_socket_ret(self.confirm_thread):
                    show_error()
                Clock.schedule_once(self.delay_frame_screen, 9)
    
    def send_retake_cmd(self, dt):
        if not self.retake_thread:
            self.retake_thread = send_socket_async("retake,")
            Clock.schedule_once(self.send_retake_cmd, 1)
        else:
            if self.retake_thread.is_alive():
                Clock.schedule_once(self.send_retake_cmd, 1)
            else:
                if not get_send_socket_ret(self.retake_thread):
                    show_error()
                self.retake_thread = None
                self.popup.dismiss()
                self.manager.transition = SlideTransition(direction="right")
                self.manager.current = 'filters'
    
    def on_confirm(self):
        print("Confirming picture!")
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = 'Please wait...')
        layout.add_widget(lbl)
        self.popup = Popup(title = 'Confirming Picture!', content=layout, auto_dismiss=False, size_hint = (.3,.3))
        self.popup.open()
        
        Clock.schedule_once(self.send_confirm_cmd, 1)
    
    def on_retake(self):
        print("Retaking photo!")
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = 'Please wait...')
        pb = ProgressBar(max = 3)
        layout.add_widget(lbl)
        layout.add_widget(pb)
        self.popup = Popup(title = 'Let\'s Retake!', content=layout, auto_dismiss=False, size_hint = (.3,.3))
        self.popup.open()
        
        Clock.schedule_once(self.send_retake_cmd, 1)

class frameMenu(Screen):
    hue = NumericProperty(0)
    popup = None
    
    sel_frame = None
    frame_thread = None
    select_thread = None
    
    def send_frame_cmd(self, dt):
        self.popup.dismiss()
    
    def send_frame_cmd(self, dt):
        if not self.frame_thread:
            self.frame_thread = send_socket_async("border,%s" % self.sel_frame)
            Clock.schedule_once(self.send_frame_cmd, 1)
        else:
            if self.frame_thread.is_alive():
                Clock.schedule_once(self.send_frame_cmd, 1)
            else:
                if not get_send_socket_ret(self.frame_thread):
                    show_error()
                self.frame_thread = None
                self.sel_frame = None
                self.popup.dismiss()
    
    def send_select_cmd(self, dt):
        if not self.select_thread:
            self.select_thread = send_socket_async("select,")
            Clock.schedule_once(self.send_select_cmd, 1)
        else:
            if self.select_thread.is_alive():
                Clock.schedule_once(self.send_select_cmd, 1)
            else:
                if not get_send_socket_ret(self.select_thread):
                    show_error()
                self.select_thread = None
                self.popup.dismiss()
                self.manager.current = 'email'
    
    def on_pick_frame(self, frame):
        print("Selected frame: %d" % frame)
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = 'Selecting frame: %d' % frame)
        pb = ProgressBar(max = 1)
        layout.add_widget(lbl)
        layout.add_widget(pb)
        self.popup = Popup(title = 'Selecting Frame...', content=layout, auto_dismiss=False, size_hint = (.3,.3))
        self.popup.open()
        
        self.sel_frame = frame
        
        Clock.schedule_once(self.send_frame_cmd, 1)
    
    def on_select(self):
        print("Selecting frame!")
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = 'Selecting frame...')
        layout.add_widget(lbl)
        self.popup = Popup(title = 'Selecting Frame!', content=layout, auto_dismiss=False, size_hint = (.3,.3))
        self.popup.open()
        
        Clock.schedule_once(self.send_select_cmd, 1)

class thankYou(Screen):
    hue = NumericProperty(0)

class emailMenu(Screen):
    hue = NumericProperty(0)
    popup = None
    
    sel_email = None
    email_thread = None
    
    def send_email_cmd(self, dt):
        if not self.email_thread:
            self.email_thread = send_socket_async("email,%s" % self.sel_email)
            Clock.schedule_once(self.send_email_cmd, 1)
        else:
            if self.email_thread.is_alive():
                Clock.schedule_once(self.send_email_cmd, 1)
            else:
                if not get_send_socket_ret(self.email_thread):
                    show_error()
                self.email_thread = None
                self.sel_email = None
                self.popup.dismiss()
                self.manager.current = 'thankyou'
                self.ids['email_text'].text = ""
    
    def close_popup(self, dt):
        self.popup.dismiss()
    
    def tiny_message(self, msg):
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = msg)
        layout.add_widget(lbl)
        self.popup = Popup(title = 'Oops!', content=layout, auto_dismiss=False, size_hint = (.3,.3))
        self.popup.open()
        
        Clock.schedule_once(self.close_popup, 2)
    
    def on_submit_email(self):
        val = self.ids['email_text'].text
        if (not val) or (" " in val) or ("\t" in val) or (not (parseaddr(val)[1] and ("@" in val) and ("." in val))):
            print("Invalid email!")
            self.tiny_message("Invalid email!")
            return
        print("Submitting email: %s" % val)
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text = 'Selecting email: %s' % val)
        layout.add_widget(lbl)
        self.popup = Popup(title = 'Selecting Email!', content=layout, auto_dismiss=False, size_hint = (.6,.3))
        self.popup.open()
        
        self.sel_email = val
        
        Clock.schedule_once(self.send_email_cmd, 1)

class ScreenManagerApp(App):

    def build(self):
        root = ScreenManager()
        self.transition = SlideTransition(direction="left")
        root.add_widget(StartMenu(name='start'))
        root.add_widget(NetworkMenu(name='network'))
        root.add_widget(BluetoothMenu(name='bluetooth'))
        root.add_widget(filterMenu(name='filters'))
        root.add_widget(confirmPicMenu(name='confirmpic'))
        root.add_widget(frameMenu(name='frames'))
        root.add_widget(emailMenu(name='email'))
        root.add_widget(thankYou(name='thankyou'))
        return root


if __name__ == '__main__':
    ScreenManagerApp().run()

