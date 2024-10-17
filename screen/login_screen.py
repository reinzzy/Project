import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder

# Firebase Configuration
firebase_config = {
    "apiKey": "AIzaSyCMDIZ_s0HG3Ozh_1tccSCaWmXC-0kZo1Y",
    "authDomain": "projectpython-58225.firebaseapp.com",
    "databaseURL": "https://projectpython-58225-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "projectpython-58225",
    "storageBucket": "projectpython-58225.appspot.com",
    "messagingSenderId": "635697293104",
    "appId": "1:635697293104:android:afe47f84df46cc64020af5"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/login.kv')
Builder.load_file(kv_path)

class LoginScreen(Screen):
    def login(self):
        email = self.ids.username.text
        password = self.ids.password.text

        if email == "" or password == "":
            self.show_popup("Login Gagal", "Email atau Password tidak boleh kosong!")
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                self.show_popup("Login Berhasil", "Selamat datang!")
                self.manager.current = 'main'
            except Exception as e:
                error_message = str(e)
                if "EMAIL_NOT_FOUND" in error_message:
                    self.show_popup("Login Gagal", "Akun tidak ditemukan.")
                elif "INVALID_PASSWORD" in error_message:
                    self.show_popup("Login Gagal", "Password salah.")
                else:
                    self.show_popup("Login Gagal", "Terjadi kesalahan saat login.")

    def go_to_signup(self):
        self.manager.current = 'signup'

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message)
        popup_layout.add_widget(popup_label)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        popup_layout.add_widget(ok_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))

        ok_button.bind(on_press=popup.dismiss)

        popup.open()
