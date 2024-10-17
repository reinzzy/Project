import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/profile.kv')
Builder.load_file(kv_path)

class ProfileScreen(Screen):
    def show_logout_confirmation(self):
        popup = LogoutPopup(on_confirm=self.logout)
        popup.open()

    def logout(self):
        print("User telah logout")
        self.manager.current = 'login'

class LogoutPopup(Popup):
    def __init__(self, on_confirm, **kwargs):
        super(LogoutPopup, self).__init__(**kwargs)
        self.on_confirm_action = on_confirm

    def on_confirm(self):
        self.dismiss()
        self.on_confirm_action()
