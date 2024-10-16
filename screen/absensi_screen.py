import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/absensi.kv')
Builder.load_file(kv_path)

class AbsensiScreen(Screen):
    pass