import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class MainScreen(Screen):
    def set_username(self, username):
        self.ids.username_label.text = f"Welcome, {username}"