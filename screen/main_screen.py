import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/mainscreen.kv')
Builder.load_file(kv_path)

class MainScreen(Screen):
    def set_username(self, username):
        self.ids.username_label.text = f"Welcome, {username}"