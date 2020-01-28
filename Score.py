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

Config.set('graphics','width',500)
Config.set('graphics','height',600)

class MyScreenManager(ScreenManager):
    pass

class MainScreen(TabbedPanel):

    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)

class SoundScreen(Screen):
    pass

class FileScreen(Screen):
    pass

class RecordScreen(Screen):
    pass

class ScoreApp(App):
    def build(self):
        return MainScreen()

if __name__=='__main__':
    ScoreApp().run()