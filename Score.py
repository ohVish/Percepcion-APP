# Kivy
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.event import EventDispatcher

# Ficheros y audio
from pathlib import Path
import sounddevice as sd
from scipy.io.wavfile import write
import time
import threading

Config.set('graphics','width',500)
Config.set('graphics','height',600)



class MyScreenManager(ScreenManager):
    pass

class MainScreen(TabbedPanel):

    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
    

class SoundScreen(Screen):
    pass

class LoadingScreen(Screen):
    pass

class FileScreen(Screen):

    txt_input = ObjectProperty(None)

    def fileOpen(self):
        if not Path('./resources/sounds/'+ self.txt_input.text).is_file():
            emerging = Popup(title='Error',content=Label(text='No se encuentra un fichero con ese nombre'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()
        else:
            # Aquí se llamaría al matláh
            print('matlah')
    

class RecordScreen(Screen,EventDispatcher):
    duration = ObjectProperty(None)
    filename = ObjectProperty(None)
    freq = ObjectProperty(None)
    end = BooleanProperty(False)
    sm = ObjectProperty(None)

    def recordFile(self):
        self.bind(end=loadStatus)
        try:
            seconds = int(self.duration.text)  # Duration of recording
            fs = int(self.freq.text) # Sample rate
        except:
            emerging = Popup(title='Error',content=Label(text='No se ha introducido datos validos .'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()
        else:
            t = threading.Thread(target=self.worker,args=(seconds,fs,self.filename.text))
            t.start()
    def worker(self,seconds,fs,filename):
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()
        write('./resources/sounds/'+filename, fs, myrecording)  # Save as WAV file 
        self.end = True

    
def loadStatus(instance,value):
        if value == True:
            instance.sm.current='soundS'
            value = False
            emerging = Popup(title='Correcto',content=Label(text='Audio grabado con éxito.'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()
            # Matláh


class ScoreApp(App):
    def build(self):
        return MainScreen()

if __name__=='__main__':
    ScoreApp().run()