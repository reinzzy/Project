import os
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/login.kv')
Builder.load_file(kv_path)

class LoginScreen(Screen):
    def login(self):
        if self.ids.username.text == "admin" and self.ids.password.text == "admin":
            self.show_popup("Login Berhasil", "Selamat datang!")
            self.manager.current = 'main'
        else:
            self.show_popup("Login Gagal", "Username atau password salah!")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message)
        popup_layout.add_widget(popup_label)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        popup_layout.add_widget(ok_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))

        ok_button.bind(on_press=popup.dismiss)

        popup.open()
