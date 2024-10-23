import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder

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
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/login.kv')
Builder.load_file(kv_path)

class LoginScreen(Screen):
    def login(self):
        email = self.ids.username.text
        password = self.ids.password.text

        if email == "" or password == "":
            self.show_popup("Login Gagal", "Email atau Password tidak boleh kosong!")
            return
        
        try:
            users = db.child("users").get()

            for user in users.each():
                user_data = user.val()
                if user_data['email'] == email and user_data['password'] == password:
                    username = user_data['username']
                    self.manager.get_screen('main').set_username(username)
                    self.show_popup("Login Berhasil", "Selamat datang!")
                    self.manager.current = 'main'
                    return

            self.show_popup("Login Gagal", "Email atau Password salah.")

        except Exception as e:
            self.show_popup("Login Gagal", f"Terjadi kesalahan: {str(e)}")

    def go_to_resetpw(self):
        self.manager.current = 'resetpw'

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
