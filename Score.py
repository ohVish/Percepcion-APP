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
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.event import EventDispatcher
from kivy.uix.image import Image
from kivy.cache import Cache

# Ficheros y audio
from pathlib import Path
import sounddevice as sd
from scipy.io.wavfile import write
import time
import threading
import os

#opencv
import cv2
import numpy as np

# Obtener la ruta del binario
import sys

# Matlab
import matlab.engine

Config.set('graphics','width',500)
Config.set('graphics','height',600)

filenameCapture = ""

def escribirFichero(filename,a,compas):
    filename = str(filename)
    lista = filename.split('.')
    filename = '.'+lista[1]+'.ly'
    filename = filename.replace('images','generated')
    fichero = open(filename,'w',encoding='utf-8')

    string = '\\language "español"\n\\header{\ntitle = "Prueba"\n}\n{\n\\time '+compas+'\n'+a+'\n}\n\\version "2.18.2"'

    fichero.write(string)
    fichero.close()
    filename = filename.split('/')
    filename = filename[len(filename)-1]
    os.chdir('./resources/generated')
    os.system("docker run --rm -v $(pwd):/app -w /app gpit2286/lilypond lilypond "+filename)
    os.chdir('../..')


class SoundScreenManager(ScreenManager):
    pass

class ImageScreenManager(ScreenManager):
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
            self.sm.current='loadS'
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
            instance.end = False
            emerging = Popup(title='Correcto',content=Label(text='Audio grabado con éxito.'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()
            # Matláh


class ImageScreen(Screen):
    pass

class ImageFileScreen(Screen):
    sm = ObjectProperty(None)
    txt_input = ObjectProperty(None)
    umb = ObjectProperty(None)
    compas = ObjectProperty(None)
    picos = ObjectProperty(None)

    def fileOpen(self):
        if not Path('./resources/images/'+ self.txt_input.text).is_file():
            emerging = Popup(title='Error',content=Label(text='No se encuentra un fichero con ese nombre'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()
        else:
            try:
                umbral = float(self.umb.text)
                picos = int(self.picos.text)
            except:
                emerging = Popup(title='Error',content=Label(text='No se ha introducido datos validos .'),
                                pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
                emerging.open()
            else:
                self.sm.get_screen('IReadS').umbral = umbral
                self.sm.get_screen('IReadS').compas = self.compas.text
                self.sm.get_screen('IReadS').picos = picos
                self.sm.get_screen('IReadS').filename = './resources/images/'+self.txt_input.text
                self.sm.get_screen('IReadS').image.source='./resources/images/'+ self.txt_input.text
                self.sm.get_screen('IReadS').image.reload()
                self.sm.transition.direction = 'left'
                self.sm.current = 'IReadS'


class CaptureScreen(Screen,EventDispatcher):
    filename = ObjectProperty(None)
    sm = ObjectProperty(None)
    umb = ObjectProperty(None)
    compas = ObjectProperty(None)
    picos = ObjectProperty(None)

    def capturing(self):
        try:
            umbral = float(self.umb.text)
            picos = int(self.picos.text)
        except:
            emerging = Popup(title='Error',content=Label(text='No se ha introducido datos validos .'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()
        else:
            video = cv2.VideoCapture(0)
            while True:
                ret,frame = video.read()
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                cv2.imshow('frame',gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # When everything done, release the capture
            cv2.imwrite('./resources/images/'+self.filename.text,gray)
            video.release()
            cv2.destroyAllWindows()
            self.sm.get_screen('IConfirmS').filename = './resources/images/'+self.filename.text
            self.sm.get_screen('IConfirmS').umbral = umbral
            self.sm.get_screen('IConfirmS').picos = picos
            self.sm.get_screen('IConfirmS').compas = self.compas.text
            self.sm.get_screen('IConfirmS').image.reload()
        
class ImageConfirmScreen(Screen):
    image = ObjectProperty(None)
    filename = StringProperty('')
    sm = ObjectProperty(None)
    end = BooleanProperty(False)
    umbral = 0.2
    compas = '2/4'
    good = True
    picos = 15
    
    def run(self):
            self.bind(end=endRecognise)
            t = threading.Thread(target=self.reconocerPartitura)
            t.start()
    
    def reconocerPartitura(self):
        eng = matlab.engine.start_matlab()
        eng.workspace['filename']=str(self.filename)
        eng.workspace['umbral']=self.umbral
        eng.workspace['valorLineas']=self.picos
        self.good = True
        try:
            eng.getPentagramas(nargout=0)
        except:
            print('Excepcion')
            self.good = False
        else:
            string=eng.workspace['string']
            escribirFichero(self.filename,string,self.compas)
        eng.quit()
        self.end=True


class ImageReadScreen(Screen,EventDispatcher):
    end = BooleanProperty(False)
    image = ObjectProperty(None)
    filename = StringProperty('')
    sm = ObjectProperty(None)
    good = True
    umbral = 0.2
    compas = '2/4'
    picos = 15

    def run(self):
            self.bind(end=endRecognise)
            t = threading.Thread(target=self.reconocerPartitura)
            t.start()

    def reconocerPartitura(self):
        eng = matlab.engine.start_matlab()
        eng.workspace['filename']=str(self.filename)
        eng.workspace['umbral']=self.umbral
        eng.workspace['valorLineas']=self.picos
        self.good = True
        try:
            eng.getPentagramas(nargout=0)
        except:
            print('Excepcion')
            self.good = False
        else:
            string=eng.workspace['str']
            escribirFichero(self.filename,string,self.compas)
        eng.quit()
        self.end=True

class ProcessingScreen1(Screen):
    pass

class ProcessingScreen2(Screen):
    pass

class ScoreApp(App):
    def build(self):
        return MainScreen()

def endRecognise(instance,value):
    if value == True:
        instance.end = False
        instance.sm.current='imageS'
        if instance.good == True:
            emerging = Popup(title='Correcto',content=Label(text='Partitura digitalizada con éxito.'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()
        else:
            emerging = Popup(title='Error',content=Label(text='Partitura no digitalizada.'),
                            pos_hint={'center_x':0.5,'center_y':0.5},size_hint=(0.75,0.5))
            emerging.open()


if __name__=='__main__':
    ScoreApp().run()